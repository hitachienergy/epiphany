require 'spec_helper'
require 'net/ssh'
require 'ruby_utils' # adds squish to String
require 'multi_json'

postgresql_host = '127.0.0.1'
postgresql_default_port = 5432

# Here we set the needed variables from ENV variables which are set in the Rakefile
# where we order the postgres hosts:
# pg_primary_node_host: primary node host.
# pg_primary_node_ip: primary node ip.
# pg_last_node_host: last standby node host (if present)
primary_node_host = ENV['pg_primary_node_host']
primary_node_ip = ENV['pg_primary_node_ip']
last_node_host = 'none'
last_node_host = ENV['pg_last_node_host'] if ENV['pg_last_node_host']

config_docs = {}
%w[logging postgresql].each do |kind|
  config_docs[kind.to_sym] = readDataYaml("configuration/#{kind}")
end

ELASTICSEARCH = { # must be global until we introduce modules
  host: listInventoryHosts('logging')[0],
  api_port: 9200
}

unless ELASTICSEARCH[:host].nil?
  # Configurable passwords for ES users were introduced in v0.10.0.
  # For testing upgrades, we use the default password for now but we're going to switch to TLS auth.
  ELASTICSEARCH[:admin_password] = config_docs[:logging]['specification']['admin_password'] || 'admin'
end

replicated =           countInventoryHosts('postgresql') > 1
replication_user =     config_docs[:postgresql]['specification']['extensions']['replication']['replication_user_name']
replication_password = config_docs[:postgresql]['specification']['extensions']['replication']['replication_user_password']
max_wal_senders =      config_docs[:postgresql]['specification']['config_file']['parameter_groups'].detect do |i|
  i['name'] == 'REPLICATION'
end ['subgroups'].detect { |i| i['name'] == 'Sending Server(s)' }['parameters'].detect { |i| i['name'] == 'max_wal_senders' }['value']
pgaudit_enabled = config_docs[:postgresql]['specification']['extensions']['pgaudit']['enabled']

spec_doc = if upgradeRun?
             readYaml(getRoleDirPath('postgresql') + 'vars/main.yml')[0]
           else
             config_docs[:postgresql]
           end

# In PG 10 there was 'wal_keep_segments'
wal_keep_size = spec_doc['specification']['config_file']['parameter_groups'].detect { |i| i['name'] == 'REPLICATION' }\
  ['subgroups'].detect { |i| i['name'] == 'Sending Server(s)' }['parameters'].detect { |i| i['name'] == 'wal_keep_size' }['value']
# Setting added in Epiphany v1.2
password_encryption = 'md5'

pg_user = 'serverspec_testuser'
pg_pass = 'testpass'

pg_config_file_booleans = { "true": '(?:on|true|yes|1)', "false": '(?:off|false|no|0)' }

def queryForCreating
  describe 'Check if it is possible to create a test schema' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c 'CREATE SCHEMA serverspec_test;'\"") do
      its(:stdout) { should match(/^CREATE SCHEMA$/) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Check if it is possible to create a test table' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c 'CREATE TABLE serverspec_test.test (col varchar(20));'\"") do
      its(:stdout) { should match(/^CREATE TABLE$/) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Check if it is possible to insert values into the test table' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c \\\"INSERT INTO serverspec_test.test (col) values ('SUCCESS');\\\"\"") do
      its(:stdout) { should match(/^INSERT 0 1$/) }
      its(:exit_status) { should eq 0 }
    end
  end
end

def queryForSelecting
  describe 'Check if it is possible to select values from the test table' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c 'SELECT * from serverspec_test.test;'\"") do
      its(:stdout) { should match(/\bSUCCESS\b/) }
      its(:exit_status) { should eq 0 }
    end
  end
end

def queryForAlteringTable
  describe 'Alter table with multiline command to verify multiline messages support' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c psql <<SQL
    ALTER TABLE serverspec_test.test
    ADD COLUMN id int,
    ADD COLUMN name text,
    ADD COLUMN city text,
    ADD COLUMN description text;
SQL") do
      its(:stdout) { should match(/^ALTER TABLE$/) }
      its(:exit_status) { should eq 0 }
    end
  end
end

def queryForDropping
  describe 'Check if it is possible to drop the test table' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c 'DROP TABLE serverspec_test.test;'\"") do
      its(:stdout) { should match(/^DROP TABLE$/) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Check if it is possible to drop the test schema' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c 'DROP SCHEMA serverspec_test CASCADE;'\"") do
      its(:stdout) { should match(/^DROP SCHEMA$/) }
      its(:exit_status) { should eq 0 }
    end
  end
end

# Running the 'systemctl is-active' command returns the result 'unknown'.
# https://bugzilla.redhat.com/show_bug.cgi?id=1073481
# Must first run the 'systemctl status' command to be able to view the service status withe the 'is-active' command.

describe 'Check PostgreSQL service status' do
  if os[:family] == 'redhat'
    describe command('systemctl status postgresql-13 > /dev/null') do
      its(:exit_status) { should eq 0 }
    end
  elsif os[:family] == 'ubuntu'
    describe command('systemctl status postgresql > /dev/null') do
      its(:exit_status) { should eq 0 }
    end
  end
end

describe 'Check if PostgreSQL service is running' do
  if os[:family] == 'redhat'
    describe service('postgresql-13') do
      it { should be_enabled }
      it { should be_running }
    end
  elsif os[:family] == 'ubuntu'
    describe service('postgresql') do
      it { should be_enabled }
      it { should be_running }
    end
  end
end

if os[:family] == 'redhat'
  describe 'Check if only one PostgreSQL service is enabled' do
    describe command("systemctl list-unit-files --type service --state enabled | grep -c 'postgresql-[0-9]'") do
      it 'is expected to eq 1' do
        expect(subject.stdout.to_i).to eq 1
      end
      its(:exit_status) { should eq 0 }
    end
  end
end

if replicated
  describe 'Check if repmgr service is running' do
    if os[:family] == 'redhat'
      describe service('repmgr13') do
        it { should be_enabled }
        it { should be_running }
      end
    elsif os[:family] == 'ubuntu'
      describe service('repmgrd') do
        it { should be_enabled }
        it { should be_running }
      end
    end
  end

  if os[:family] == 'redhat'
    describe 'Check if only one repmgr service is enabled' do
      describe command("systemctl list-unit-files --type service --state enabled | grep -c 'repmgr[0-9]'") do
        it 'is expected to eq 1' do
          expect(subject.stdout.to_i).to eq 1
        end
        its(:exit_status) { should eq 0 }
      end
    end
  end

  if os[:family] == 'ubuntu'
    describe 'Check if repmgr service uses correct config file' do
      describe command('systemctl status repmgrd') do
        regexp = %r{ /etc/repmgr\.conf }
        it "is expected to match #{regexp.inspect}" do
          # force_encoding used to work around https://github.com/sj26/rspec_junit_formatter/issues/67
          expect(subject.stdout.force_encoding('UTF-8')).to match regexp
        end
        its(:exit_status) { should eq 0 }
      end
    end
  end
end

if os[:family] == 'redhat'
  describe 'Check PostgreSQL directories and config files' do
    let(:disable_sudo) { false }
    describe file('/var/lib/pgsql/13/data') do
      it { should exist }
      it { should be_a_directory }
    end
    describe file('/var/lib/pgsql/13/data/pg_hba.conf') do
      it { should exist }
      it { should be_a_file }
      it { should be_readable }
    end
    describe file('/var/lib/pgsql/13/data/postgresql.conf') do
      it { should exist }
      it { should be_a_file }
      it { should be_readable }
    end
    describe file('/var/lib/pgsql/13/data/postgresql-epiphany.conf') do
      it { should exist }
      it { should be_a_file }
      it { should be_readable }
    end
  end
elsif os[:family] == 'ubuntu'
  describe 'Check PostgreSQL directories and config files' do
    let(:disable_sudo) { false }
    describe file('/etc/postgresql/13/main') do
      it { should exist }
      it { should be_a_directory }
    end
    describe file('/etc/postgresql/13/main/pg_hba.conf') do
      it { should exist }
      it { should be_a_file }
      it { should be_readable }
    end
    describe file('/etc/postgresql/13/main/postgresql.conf') do
      it { should exist }
      it { should be_a_file }
      it { should be_readable }
    end
    describe file('/etc/postgresql/13/main/postgresql-epiphany.conf') do
      it { should exist }
      it { should be_a_file }
      it { should be_readable }
    end
  end
end

describe 'Check if the ports are open' do
  let(:disable_sudo) { false }
  describe port(postgresql_default_port) do
    it { should be_listening }
  end
end

if os[:family] == 'ubuntu'
  describe 'Check if PostgreSQL is ready' do
    let(:disable_sudo) { false }
    describe command('su - postgres -c "pg_isready"') do
      its(:stdout) { should match(/postgresql:#{postgresql_default_port} - accepting connections/) }
      its(:exit_status) { should eq 0 }
    end
  end
end

describe 'Check if it is possible to connect to PostgreSQL database' do
  let(:disable_sudo) { false }
  describe command("su - postgres -c \"psql -t -c 'SELECT 2+2;'\"") do
    its(:stdout) { should match(/4/) }
    its(:exit_status) { should eq 0 }
  end
end

unless replicated
  queryForCreating
  queryForSelecting
  queryForAlteringTable
end

if replicated
  describe 'Display information about each registered node in the replication cluster' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c 'repmgr cluster show'") do
      its(:stdout) { should match(/primary.*\*.*running/) }
      its(:stdout) { should match(/standby.*running/) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Check repmgrd is running on each node in the cluster' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c 'repmgr service status'") do
      its(:stdout) { should_not match(/not running/) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Run health checks on a node from a replication perspective' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c 'repmgr node check'") do
      its(:stdout) { should_not match %r{ CRITICAL } }
      its(:stdout) { should_not match %r{ WARNING } }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Check hot_standby setting in postgresql-epiphany.conf file' do
    let(:disable_sudo) { false }
    if os[:family] == 'redhat'
      describe command("grep -Eio '^hot_standby\s*=[^#]*' /var/lib/pgsql/13/data/postgresql-epiphany.conf") do
        its(:exit_status) { should eq 0 }
        its(:stdout) { should match(/^hot_standby\s*=\s*#{pg_config_file_booleans[:true]}/i) }
      end
    elsif os[:family] == 'ubuntu'
      describe command("grep -Eio '^hot_standby\s*=[^#]*' /etc/postgresql/13/main/postgresql-epiphany.conf") do
        its(:exit_status) { should eq 0 }
        its(:stdout) { should match(/^hot_standby\s*=\s*#{pg_config_file_booleans[:true]}/i) }
      end
    end
  end

  if primary_node_host.include? host_inventory['hostname']
    if os[:family] == 'redhat'
      describe 'Check PostgreSQL config files for master node' do
        let(:disable_sudo) { false }
        describe command('cat /var/lib/pgsql/13/data/postgresql-epiphany.conf | grep wal_level') do
          its(:stdout) { should match(/^wal_level = replica/) }
          its(:exit_status) { should eq 0 }
        end
        describe command('cat /var/lib/pgsql/13/data/postgresql-epiphany.conf | grep max_wal_senders') do
          its(:stdout) { should match(/^max_wal_senders = #{max_wal_senders}/) }
          its(:exit_status) { should eq 0 }
        end
        describe command('cat /var/lib/pgsql/13/data/postgresql-epiphany.conf | grep wal_keep_size') do
          its(:stdout) { should match(/^wal_keep_size = #{wal_keep_size}/) }
          its(:exit_status) { should eq 0 }
        end
        describe command("su - postgres -c \"psql -t -c '\\du'\" | grep #{replication_user}") do
          its(:stdout) { should match(/#{replication_user}/) }
          its(:stdout) { should match(/Replication/) }
          its(:exit_status) { should eq 0 }
        end
        describe command("cat /var/lib/pgsql/13/data/pg_hba.conf | grep replication | grep #{password_encryption}") do
          its(:stdout) { should match(/#{replication_user}/) }
          its(:stdout) { should match(/replication/) }
          its(:exit_status) { should eq 0 }
        end
      end
    elsif os[:family] == 'ubuntu'
      describe 'Check PostgreSQL config files for master node' do
        let(:disable_sudo) { false }
        describe command('cat /etc/postgresql/13/main/postgresql-epiphany.conf | grep wal_level') do
          its(:stdout) { should match(/^wal_level = replica/) }
          its(:exit_status) { should eq 0 }
        end
        describe command('cat /etc/postgresql/13/main/postgresql-epiphany.conf | grep max_wal_senders') do
          its(:stdout) { should match(/^max_wal_senders = #{max_wal_senders}/) }
          its(:exit_status) { should eq 0 }
        end
        describe command('cat /etc/postgresql/13/main/postgresql-epiphany.conf | grep wal_keep_size') do
          its(:stdout) { should match(/^wal_keep_size = #{wal_keep_size}/) }
          its(:exit_status) { should eq 0 }
        end
        describe command("su - postgres -c \"psql -t -c '\\du'\" | grep #{replication_user}") do
          its(:stdout) { should match(/#{replication_user}/) }
          its(:stdout) { should match(/Replication/) }
          its(:exit_status) { should eq 0 }
        end
        describe command("cat /etc/postgresql/13/main/pg_hba.conf | grep replication | grep #{password_encryption}") do
          its(:stdout) { should match(/#{replication_user}/) }
          its(:stdout) { should match(/replication/) }
          its(:exit_status) { should eq 0 }
        end
      end
    end

    describe 'Check the status of master node' do
      let(:disable_sudo) { false }
      describe command("su - postgres -c \"psql -t -c 'SELECT usename, state from pg_stat_replication;'\"") do
        its(:stdout) { should match(/\bstreaming\b/) }
        its(:stdout) { should match(/\b#{replication_user}\b/) }
        its(:exit_status) { should eq 0 }
      end
    end

    describe 'Check recovery status of master node' do
      let(:disable_sudo) { false }
      describe command("su - postgres -c \"psql -t -c 'SELECT pg_is_in_recovery();'\"") do
        its(:stdout) { should match(/\bf\b/) }
        its(:exit_status) { should eq 0 }
      end
    end

    queryForCreating
    queryForSelecting
    queryForAlteringTable

  elsif host_inventory['hostname'] != primary_node_host
    if os[:family] == 'redhat'
      describe 'Check PostgreSQL files for replica nodes' do
        let(:disable_sudo) { false }
        describe file('/var/lib/pgsql/.pgpass') do
          it { should exist }
          it { should be_readable }
          its(:content) { should match(/#{replication_user}:#{replication_password}/) }
        end
      end
    elsif os[:family] == 'ubuntu'
      describe 'Check PostgreSQL files for replica nodes' do
        let(:disable_sudo) { false }
        describe file('/var/lib/postgresql/.pgpass') do
          it { should exist }
          it { should be_readable }
          its(:content) { should match(/#{replication_user}:#{replication_password}/) }
        end
      end
    end

    describe 'Check the state of replica nodes' do
      let(:disable_sudo) { false }
      describe command("su - postgres -c \"psql -t -c 'SELECT status, conninfo FROM pg_stat_wal_receiver;'\"") do
        its(:stdout) { should match(/\bstreaming\b/) }
        its(:stdout) { should match(/\buser=#{replication_user}\b/) }
        its(:exit_status) { should eq 0 }
      end
    end

    describe 'Check recovery status of replica node' do
      let(:disable_sudo) { false }
      describe command("su - postgres -c \"psql -t -c 'SELECT pg_is_in_recovery();'\"") do
        its(:stdout) { should match(/\bt\b/) }
        its(:exit_status) { should eq 0 }
      end
    end

    queryForSelecting

  end
end

### Cleaning up

queryForDropping unless replicated

if replicated && (last_node_host.include? host_inventory['hostname'])
  ssh_options = Specinfra.backend.get_config(:ssh_options)
  describe 'Clean up' do
    it 'Delegate drop table query to master node' do
      Net::SSH.start(primary_node_ip, ENV['user'], ssh_options) do |ssh|
        result = ssh.exec!("sudo su - postgres -c \"psql -t -c 'DROP TABLE serverspec_test.test;'\" 2>&1")
        expect(result).to match 'DROP TABLE'
      end
    end
    it 'Delegate drop schema query to master node' do
      Net::SSH.start(primary_node_ip, ENV['user'], ssh_options) do |ssh|
        result = ssh.exec!("sudo su - postgres -c \"psql -t -c 'DROP SCHEMA serverspec_test CASCADE;'\" 2>&1")
        expect(result).to match 'DROP SCHEMA'
      end
    end
  end
end

### Tests for PGAudit

if pgaudit_enabled && countInventoryHosts('logging') > 0 && (!replicated || (replicated && (last_node_host.include? host_inventory['hostname'])))

  def get_elasticsearch_query(message_pattern:, size: 20, with_sort: true)
    query_template = {
      _source: ['message', '@timestamp'],
      query: {
        query_string: {
          query: 'log.file.path:(\\/var\\/log\\/postgresql\\/postgresql\\-13\\-main.log OR \\/var\\/log\\/postgresql\\/postgresql.log)'\
                 " AND message:#{message_pattern} AND message:\"LOG:  AUDIT\" AND @timestamp:[now-30m TO now]"
        }
      },
      size: size
    }
    sort_clause = {
      sort: { '@timestamp': { unmapped_type: 'date' } }
    }
    query_template.merge!(sort_clause) if with_sort
    # convert hash to json
    MultiJson.dump(query_template, pretty: true)
  end

  def get_query_command_with_retries(json_query:, min_doc_hits:, retries: 600, elasticsearch: ELASTICSEARCH)
    command = <<~COMMAND
      for i in {1..#{retries}}; do
        if curl -k -s -u admin:#{elasticsearch[:admin_password]} 'https://#{elasticsearch[:host]}:#{elasticsearch[:api_port]}/_search?pretty=true' -H 'Content-Type: application/json' -d '#{json_query}'
           | jq --exit-status '. | select(.hits.total.value >= #{min_doc_hits})'; then
          echo 'READY'; break;
        else
          echo 'WAITING'; sleep 1;
        fi;
      done
    COMMAND
    # convert to one-liner
    command.squish
  end

  describe 'Check if Elasticsearch logs contain queries from PostrgeSQL database' do
    query = get_elasticsearch_query(message_pattern: "serverspec_test* AND NOT #{pg_user}")
    command = get_query_command_with_retries(json_query: query, min_doc_hits: 6)
    describe command(command) do
      its(:stdout) { should match(/CREATE SCHEMA serverspec_test/) }
      its(:stdout) { should match(/CREATE TABLE serverspec_test\.test/) }
      its(:stdout) { should match(/INSERT INTO serverspec_test\.test/) }
      its(:stdout) { should match(/DROP TABLE serverspec_test\.test/) }
      its(:stdout) { should match(/DROP SCHEMA serverspec_test/) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Check support for multiline messages' do
    query = get_elasticsearch_query(message_pattern: '"ADD COLUMN city text"')
    describe command("curl -k -u admin:#{ELASTICSEARCH[:admin_password]} 'https://#{ELASTICSEARCH[:host]}:#{ELASTICSEARCH[:api_port]}/_search?pretty=true' -H 'Content-Type: application/json' -d '#{query.squish}'") do
      its(:stdout) do
        should match(/ALTER TABLE serverspec_test\.test.*\\n\\t.*ADD COLUMN id.*\\n\\t.*ADD COLUMN name.*\\n\\t.*ADD COLUMN city.*\\n\\t.*ADD COLUMN description/)
      end
      its(:exit_status) { should eq 0 }
    end
  end

end

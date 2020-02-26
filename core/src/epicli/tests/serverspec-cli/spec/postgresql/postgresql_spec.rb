require 'spec_helper'
require 'net/ssh'

postgresql_default_port = 5432
replicated = readDataYaml("configuration/postgresql")["specification"]["replication"]["enable"]
replication_user = readDataYaml("configuration/postgresql")["specification"]["replication"]["user"]
replication_password = readDataYaml("configuration/postgresql")["specification"]["replication"]["password"]
max_wal_senders = readDataYaml("configuration/postgresql")["specification"]["replication"]["max_wal_senders"]
wal_keep_segments = readDataYaml("configuration/postgresql")["specification"]["replication"]["wal_keep_segments"]


def queryForCreating
  describe 'Checking if it is possible to create a test schema' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c 'CREATE SCHEMA serverspec_test;'\"") do
      its(:stdout) { should match /^CREATE SCHEMA$/ }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to create a test table' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c 'CREATE TABLE serverspec_test.test (col varchar(20));'\"") do
      its(:stdout) { should match /^CREATE TABLE$/ }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to insert values into the test table' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c \\\"INSERT INTO serverspec_test.test (col) values ('SUCCESS');\\\"\"") do
      its(:stdout) { should match /^INSERT 0 1$/ }
      its(:exit_status) { should eq 0 }
    end
  end
end

def queryForSelecting
  describe 'Checking if it is possible to select values from the test table' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c 'SELECT * from serverspec_test.test;'\"") do
      its(:stdout) { should match /\bSUCCESS\b/ }
      its(:exit_status) { should eq 0 }
    end
  end
end

def queryForDropping
  describe 'Checking if it is possible to drop the test table' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c 'DROP TABLE serverspec_test.test;'\"") do
      its(:stdout) { should match /^DROP TABLE$/ }
      its(:exit_status) { should eq 0 }
    end
  end
  
  describe 'Checking if it is possible to drop the test schema' do
    let(:disable_sudo) { false }
    describe command("su - postgres -c \"psql -t -c 'DROP SCHEMA serverspec_test;'\"") do
      its(:stdout) { should match /^DROP SCHEMA$/ }
      its(:exit_status) { should eq 0 }
    end
  end
end

# Running the 'systemctl is-active' command returns the result 'unknown'.
# https://bugzilla.redhat.com/show_bug.cgi?id=1073481
# Must first run the 'systemctl status' command to be able to view the service status withe the 'is-active' command.

describe 'Checking PostgreSQL service status' do
  describe command("systemctl status postgresql > /dev/null") do
    its(:exit_status) { should eq 0 }
  end
end

describe 'Checking if PostgreSQL service is running' do
  describe service('postgresql') do
    it { should be_enabled }
    it { should be_running }
  end
end

if os[:family] == 'redhat'
  describe 'Checking PostgreSQL directories and config files' do
    let(:disable_sudo) { false }
    describe file('/var/opt/rh/rh-postgresql10/lib/pgsql/data') do
      it { should exist }
      it { should be_a_directory }
    end
    describe file("/var/opt/rh/rh-postgresql10/lib/pgsql/data/pg_hba.conf") do
      it { should exist }
      it { should be_a_file }
      it { should be_readable }
     end
    describe file("/var/opt/rh/rh-postgresql10/lib/pgsql/data/postgresql.conf") do
      it { should exist }
      it { should be_a_file }
      it { should be_readable }
    end
  end
elsif os[:family] == 'ubuntu'
  describe 'Checking PostgreSQL directories and config files' do
    let(:disable_sudo) { false }
    describe file('/etc/postgresql/10/main') do
      it { should exist }
      it { should be_a_directory }
    end
    describe file("/etc/postgresql/10/main/pg_hba.conf") do
      it { should exist }
      it { should be_a_file }
      it { should be_readable }
     end
    describe file("/etc/postgresql/10/main/postgresql.conf") do
      it { should exist }
      it { should be_a_file }
      it { should be_readable }
    end
  end
end

describe 'Checking if the ports are open' do
  let(:disable_sudo) { false }
  describe port(postgresql_default_port) do
    it { should be_listening }
  end
end 

describe 'Checking if PostgreSQL is ready' do
  describe command("pg_isready") do
    its(:stdout) { should match /postgresql:#{postgresql_default_port} - accepting connections/ }
    its(:exit_status) { should eq 0 }
  end
end

describe 'Checking if it is possible to connect to PostgreSQL database' do
  let(:disable_sudo) { false }
  describe command("su - postgres -c \"psql -t -c 'SELECT 2+2;'\"") do
    its(:stdout) { should match /4/ }
    its(:exit_status) { should eq 0 }
  end
end

if !replicated
  queryForCreating
  queryForSelecting
  queryForDropping
end   

if replicated
  nodes =  listInventoryHosts("postgresql")
  master = nodes[0]
  master_ip = listInventoryIPs("postgresql")[0]
  slave = nodes[1]
 
  if master.include? host_inventory['hostname']
    if os[:family] == 'redhat'
      describe 'Checking PostgreSQL config files for master' do
        let(:disable_sudo) { false }
        describe command("cat /var/opt/rh/rh-postgresql10/lib/pgsql/data/postgresql.conf | grep wal_level") do
          its(:stdout) { should match /^wal_level = replica/ }
          its(:exit_status) { should eq 0 }
        end
        describe command("cat /var/opt/rh/rh-postgresql10/lib/pgsql/data/postgresql.conf | grep max_wal_senders") do
          its(:stdout) { should match /^max_wal_senders = #{max_wal_senders}/ }
          its(:exit_status) { should eq 0 }
        end
        describe command("cat /var/opt/rh/rh-postgresql10/lib/pgsql/data/postgresql.conf | grep wal_keep_segments") do
          its(:stdout) { should match /^wal_keep_segments = #{wal_keep_segments}/ }
          its(:exit_status) { should eq 0 }
        end
        describe command("su - postgres -c \"psql -t -c '\\du'\" | grep #{replication_user}") do
          its(:stdout) { should match /#{replication_user}/ }
          its(:stdout) { should match /Replication/ }
          its(:exit_status) { should eq 0 }
        end
        describe command("cat /var/opt/rh/rh-postgresql10/lib/pgsql/data/pg_hba.conf | grep replication | grep md5") do
          its(:stdout) { should match /#{replication_user}/ }
          its(:stdout) { should match /replication/ }
          its(:exit_status) { should eq 0 }
        end
      end
    elsif os[:family] == 'ubuntu'
      describe 'Checking PostgreSQL config files for master' do
        let(:disable_sudo) { false }
        describe command("cat /etc/postgresql/10/main/postgresql.conf | grep wal_level") do
          its(:stdout) { should match /^wal_level = replica/ }
          its(:exit_status) { should eq 0 }
        end
        describe command("cat /etc/postgresql/10/main/postgresql.conf | grep max_wal_senders") do
          its(:stdout) { should match /^max_wal_senders = #{max_wal_senders}/ }
          its(:exit_status) { should eq 0 }
        end
        describe command("cat /etc/postgresql/10/main/postgresql.conf | grep wal_keep_segments") do
          its(:stdout) { should match /^wal_keep_segments = #{wal_keep_segments}/ }
          its(:exit_status) { should eq 0 }
        end
        describe command("su - postgres -c \"psql -t -c '\\du'\" | grep #{replication_user}") do
          its(:stdout) { should match /#{replication_user}/ }
          its(:stdout) { should match /Replication/ }
          its(:exit_status) { should eq 0 }
        end
        describe command("cat /etc/postgresql/10/main/pg_hba.conf | grep replication | grep md5") do
          its(:stdout) { should match /#{replication_user}/ }
          its(:stdout) { should match /replication/ }
          its(:exit_status) { should eq 0 }
        end
      end
    end

    describe 'Checking the status of master node' do
      let(:disable_sudo) { false }
      describe command("su - postgres -c \"psql -t -c 'SELECT usename, state from pg_stat_replication;'\"") do
        its(:stdout) { should match /\bstreaming\b/ }
        its(:stdout) { should match /\b#{replication_user}\b/ }
        its(:exit_status) { should eq 0 }
      end
    end

    queryForCreating
    queryForSelecting
    
  elsif slave.include? host_inventory['hostname']
    if os[:family] == 'redhat'
      describe 'Checking PostgreSQL config files for slave' do
        let(:disable_sudo) { false }
        describe command("cat /var/opt/rh/rh-postgresql10/lib/pgsql/data/postgresql.conf | grep hot_standby") do
          its(:stdout) { should match /^hot_standby = on/ }
          its(:exit_status) { should eq 0 }
        end
        describe file('/var/lib/pgsql/.pgpass') do
          it { should exist }
          it { should be_readable }
          its(:content) { should match /#{replication_user}:#{replication_password}/ }
        end
      end
    elsif os[:family] == 'ubuntu'
      describe 'Checking PostgreSQL config files for slave' do
        let(:disable_sudo) { false }
        describe command("cat /etc/postgresql/10/main/postgresql.conf | grep hot_standby") do
          its(:stdout) { should match /^hot_standby = on/ }
          its(:exit_status) { should eq 0 }
        end
        describe file('/var/lib/postgresql/.pgpass') do
          it { should exist }
          it { should be_readable }
          its(:content) { should match /#{replication_user}:#{replication_password}/ }
        end
      end
    end

    describe 'Checking the state of replica nodes' do
      let(:disable_sudo) { false }
      describe command("su - postgres -c \"psql -t -c 'SELECT status, conninfo  from pg_stat_wal_receiver;'\"") do
        its(:stdout) { should match /\bstreaming\b/ }
        its(:stdout) { should match /\buser=#{replication_user}\b/ }
        its(:exit_status) { should eq 0 }
      end
    end

    queryForSelecting

    describe 'Clean up' do
      it "Delegate drop table query to master" do
        Net::SSH.start(master_ip, ENV['user'], keys: [ENV['keypath']], :keys_only => TRUE) do|ssh|
          result = ssh.exec!("sudo su - postgres -c \"psql -t -c 'DROP TABLE serverspec_test.test;'\"")
          expect(result).to match 'DROP TABLE'
        end
      end
      it "Delegate drop schema query to master" do
        Net::SSH.start(master_ip, ENV['user'], keys: [ENV['keypath']], :keys_only => TRUE) do|ssh|
          result = ssh.exec!("sudo su - postgres -c \"psql -t -c 'DROP SCHEMA serverspec_test;'\"")
          expect(result).to match 'DROP SCHEMA'
        end
      end          
    end
    
  end
end

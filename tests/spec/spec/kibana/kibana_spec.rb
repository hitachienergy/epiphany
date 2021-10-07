require 'spec_helper'

# Configurable passwords for ES users were introduced in v0.10.0.
# For testing upgrades, we use the default password for now but it should be read from kibana.yml (remote host).
es_kibanaserver_user_password  = readDataYaml("configuration/logging")["specification"]["kibanaserver_password"] || "kibanaserver"
es_kibanaserver_user_is_active = readDataYaml("configuration/logging")["specification"]["kibanaserver_user_active"]
es_kibanaserver_user_is_active = true if es_kibanaserver_user_is_active.nil?

es_api_port         = 9200
kibana_default_port = 5601

describe 'Check if Kibana package is installed' do
  describe package('opendistroforelasticsearch-kibana') do
    it { should be_installed }
  end
end

describe 'Check if Kibana service is running' do
  describe service('kibana') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Check if Kibana user exists' do
  describe group('kibana') do
    it { should exist }
  end
  describe user('kibana') do
    it { should exist }
    it { should belong_to_group 'kibana' }
  end
end

describe 'Check Kibana directories and config files' do
  describe file('/etc/kibana') do
    it { should exist }
    it { should be_a_directory }
  end
  describe file("/etc/kibana/kibana.yml") do
    it { should exist }
    it { should be_a_file }
  end
  describe file('/etc/logrotate.d/kibana') do
    it { should exist }
    it { should be_a_file }
  end
end

describe 'Check if non-empty Kibana log file exists' do
  describe command('find /var/log/kibana -maxdepth 1 -name kibana.log* -size +0 -type f | wc -l') do
    its(:exit_status) { should eq 0 }
    its('stdout.to_i') { should > 0 }
  end
end

if es_kibanaserver_user_is_active
  listInventoryHosts("logging").each do |val|
    describe 'Check the connection to the Elasticsearch hosts' do
      let(:disable_sudo) { false }
      describe command("curl -k -u kibanaserver:#{es_kibanaserver_user_password} -o /dev/null -s -w '%{http_code}' https://#{val}:#{es_api_port}") do
        it "is expected to be equal" do
          expect(subject.stdout.to_i).to eq 200
        end
      end
    end
  end

  listInventoryHosts("kibana").each do |val|
    describe 'Check Kibana app HTTP status code' do
      let(:disable_sudo) { false }
      describe command("curl -u kibanaserver:#{es_kibanaserver_user_password} -o /dev/null -s -w '%{http_code}' http://#{val}:#{kibana_default_port}/app/kibana") do
        it "is expected to be equal" do
          expect(subject.stdout.to_i).to eq 200
        end
      end
    end
  end
end

listInventoryHosts("kibana").each do |val|
  describe 'Check Kibana health' do
    let(:disable_sudo) { false }
    describe command("curl http://#{val}:#{kibana_default_port}/api/status") do
      its(:stdout_as_json) { should include('status' => include('overall' => include('state' => 'green'))) }
      its(:exit_status) { should eq 0 }
    end
  end
end

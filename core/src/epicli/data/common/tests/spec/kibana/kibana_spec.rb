require 'spec_helper'

elasticsearch_admin_password = readDataYaml("configuration/logging")["specification"]["admin_password"]
elasticsearch_api_port = 9200
kibana_default_port = 5601
kibanaserver_password = readDataYaml("configuration/logging")["specification"]["kibanaserver_password"]

describe 'Checking if Kibana package is installed' do
  describe package('opendistroforelasticsearch-kibana') do
    it { should be_installed }
  end
end

describe 'Checking if Kibana service is running' do
  describe service('kibana') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if Kibana user exists' do
  describe group('kibana') do
    it { should exist }
  end
  describe user('kibana') do
    it { should exist }
    it { should belong_to_group 'kibana' }
  end
end

describe 'Checking Kibana directories and config files' do
  describe file('/etc/kibana') do
    it { should exist }
    it { should be_a_directory }
  end
  describe file("/etc/kibana/kibana.yml") do
    it { should exist }
    it { should be_a_file }
  end
end

describe 'Checking if Kibana log file exists and is not empty' do
  describe file('/var/log/kibana/kibana.log') do
    it { should exist }
    it { should be_a_file }
    its(:size) { should > 0 }
  end
  describe file('/etc/logrotate.d/kibana') do
    it { should exist }
    it { should be_a_file }
  end
end

listInventoryHosts("logging").each do |val|
  describe 'Checking the connection to the Elasticsearch hosts' do
    let(:disable_sudo) { false }
    describe command("curl -k -u admin:#{elasticsearch_admin_password} -o /dev/null -s -w '%{http_code}' https://#{val}:#{elasticsearch_api_port}") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq 200
      end
    end
  end
end

listInventoryHosts("kibana").each do |val|
  describe 'Checking Kibana app HTTP status code' do
    let(:disable_sudo) { false }
    describe command("curl -u admin:#{kibanaserver_password} -o /dev/null -s -w '%{http_code}' http://#{val}:#{kibana_default_port}/app/kibana") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq 200
      end
    end
  end
end

listInventoryHosts("kibana").each do |val|
  describe 'Checking Kibana health' do
    let(:disable_sudo) { false }
    describe command("curl http://#{val}:#{kibana_default_port}/api/status") do
      its(:stdout_as_json) { should include('status' => include('overall' => include('state' => 'green'))) }
      its(:exit_status) { should eq 0 }
    end
  end
end

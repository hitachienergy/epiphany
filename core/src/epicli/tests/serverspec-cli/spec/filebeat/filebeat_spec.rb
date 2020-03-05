require 'spec_helper'

elasticsearch_api_port = 9200
kibana_api_port = 5601

describe 'Checking if Filebeat package is installed' do
  describe package('filebeat') do
    it { should be_installed }
  end
end

describe 'Checking if Filebeat service is running' do
  describe service('filebeat') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking Filebeat directories and config files' do
  let(:disable_sudo) { false }
  describe file('/etc/filebeat') do
    it { should exist }
    it { should be_a_directory }
  end
  describe file("/etc/filebeat/filebeat.yml") do
    it { should exist }
    it { should be_a_file }
  end
end

if hostInGroups?("kubernetes_master") || hostInGroups?("kubernetes_node")
  describe 'Checking extra configuration for master/worker roles - setting Filebeat to be started after Docker' do
    describe file("/etc/systemd/system/filebeat.service.d/extra-dependencies.conf") do
      it { should exist }
      it { should be_a_file }
      its(:content) { should match /After=docker\.service/ }
    end
  end
end

listInventoryHosts("logging").each do |val|
  describe 'Checking the connection to the Elasticsearch hosts' do
    let(:disable_sudo) { false }
    describe command("curl -k -u admin:admin -o /dev/null -s -w '%{http_code}' https://#{val}:#{elasticsearch_api_port}") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq 200
      end
    end
  end
end

listInventoryHosts("kibana").each do |val|
  describe 'Checking the connection to the Kibana endpoint' do
    let(:disable_sudo) { false }
    describe command("curl -u admin:admin -o /dev/null -s -w '%{http_code}' http://#{val}:#{kibana_api_port}/app/kibana") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq 200
      end
    end
  end
end

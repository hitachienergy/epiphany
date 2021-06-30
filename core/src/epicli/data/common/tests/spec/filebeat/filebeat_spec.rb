require 'spec_helper'

# Skip tests if there is no 'logging' component
if countInventoryHosts("logging") < 1
  puts 'Skipping Filebeat tests since "logging" component not found in inventory.'
  exit 0
end

# Configurable passwords for ES users were introduced in v0.10.0.
# For testing upgrades, we use default passwords for now but they should be read from filebeat.yml (remote host).
es_logstash_user_password  = readDataYaml("configuration/logging")["specification"]["logstash_password"] || "logstash"
es_logstash_user_is_active = readDataYaml("configuration/logging")["specification"]["logstash_user_active"]
es_logstash_user_is_active = true if es_logstash_user_is_active.nil?

es_kibanaserver_user_password  = readDataYaml("configuration/logging")["specification"]["kibanaserver_password"] || "kibanaserver"
es_kibanaserver_user_is_active = readDataYaml("configuration/logging")["specification"]["kibanaserver_user_active"]
es_kibanaserver_user_is_active = true if es_kibanaserver_user_is_active.nil?

es_api_port     = 9200
kibana_api_port = 5601

describe 'Check if filebeat package is installed' do
  describe package('filebeat') do
    it { should be_installed }
  end
end

describe 'Check if filebeat service is running' do
  describe service('filebeat') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Check Filebeat directories and config files' do
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
  describe 'Check extra configuration for master/worker roles - setting Filebeat to be started after Docker' do
    describe file("/etc/systemd/system/filebeat.service.d/extra-dependencies.conf") do
      it { should exist }
      it { should be_a_file }
      its(:content) { should match /After=docker\.service/ }
    end
  end
end

if es_logstash_user_is_active
  listInventoryHosts("logging").each do |val|
    describe 'Check the connection to the Elasticsearch hosts' do
      let(:disable_sudo) { false }
      describe command("curl -k -u logstash:#{es_logstash_user_password} -o /dev/null -s -w '%{http_code}' https://#{val}:#{es_api_port}") do
        it "is expected to be equal" do
          expect(subject.stdout.to_i).to eq 200
        end
      end
    end
  end
end

# This test is for optional (manual) command 'filebeat setup --dashboards' (loads Kibana dashboards)
if es_kibanaserver_user_is_active
  listInventoryHosts("kibana").each do |val|
    describe 'Check the connection to the Kibana endpoint' do
      let(:disable_sudo) { false }
      describe command("curl -u kibanaserver:#{es_kibanaserver_user_password} -o /dev/null -s -w '%{http_code}' http://#{val}:#{kibana_api_port}/app/kibana") do
        it "is expected to be equal" do
          expect(subject.stdout.to_i).to eq 200
        end
      end
    end
  end
end

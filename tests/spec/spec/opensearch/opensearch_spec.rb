require 'spec_helper'
# Configurable passwords for ES users were introduced in v0.10.0.
# For testing upgrades, we use the default password for now but we're going to switch to TLS auth.
es_admin_password = readDataYaml('configuration/opensearch')['specification']['admin_password'] || 'admin'
es_rest_api_port  = 9200
es_transport_port = 9300

describe 'Check if opensearch service is running' do
  describe service('opensearch') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Check if opensearch user exists' do
  describe group('opensearch') do
    it { should exist }
  end
  describe user('opensearch') do
    it { should exist }
    it { should belong_to_group 'opensearch' }
  end
end

describe 'Check Elasticsearch directories and config files' do
  let(:disable_sudo) { false }
  describe file('/usr/share/opensearch') do
    it { should exist }
    it { should be_a_directory }
  end
  describe file('/usr/share/opensearch/config/opensearch.yml') do
    it { should exist }
    it { should be_a_file }
  end
end
describe 'Check if the ports are open' do
  let(:disable_sudo) { false }
  describe port(es_rest_api_port) do
    it { should be_listening }
  end
  describe port(es_transport_port) do
    it { should be_listening }
  end
end

listInventoryHosts('opensearch').each do |val|
  describe 'Check Elasticsearch nodes status codes' do
    let(:disable_sudo) { false }
    describe command("curl -k -u admin:#{es_admin_password} -o /dev/null -s -w '%{http_code}' https://#{val}:#{es_rest_api_port}") do
      it 'is expected to be equal' do
        expect(subject.stdout.to_i).to eq 200
      end
    end
  end
  describe 'Check OpenSearch health' do
    let(:disable_sudo) { false }
    describe command("curl -k -u admin:#{es_admin_password} https://#{val}:#{es_rest_api_port}/_cluster/health?pretty=true") do
      its(:stdout_as_json) { should include('status' => /green|yellow/) }
      its(:stdout_as_json) { should include('number_of_nodes' => countInventoryHosts('opensearch')) }
      its(:exit_status) { should eq 0 }
    end
  end
end

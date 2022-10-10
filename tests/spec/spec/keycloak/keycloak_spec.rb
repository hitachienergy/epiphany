require 'spec_helper'
require 'securerandom'

config_spec =  readDataYaml('configuration/keycloak')['specification']
chart_values = config_spec['chart_values']
service_port = chart_values['service']['httpsNodePort']
service_replicas = chart_values['replicas']
service_namespace = config_spec['namespace']
chart_fullname = chart_values['fullnameOverride']
service_name = "#{chart_fullname}-http"
http_settings = chart_values.fetch('http', {})  # optional setting
url_relative_path = http_settings.fetch('relativePath', '/auth').chomp('/')

describe 'Check if service is present' do
  describe command("kubectl get services --namespace=#{service_namespace}") do
    its(:stdout) { should match(/#{service_name}/) }
  end
end

describe 'Check if port is open' do
  describe port(service_port) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end

describe 'Check status - all pods should be running' do
  describe command("kubectl get pods --namespace=#{service_namespace} --field-selector=status.phase=Running | grep #{chart_fullname} | wc -l") do
    it 'is expected to be equal' do
      expect(subject.stdout.to_i).to eq service_replicas
    end
    its(:exit_status) { should eq 0 }
  end
end

describe 'Check service URL' do
  describe command("curl -o /dev/null -s -w '%{http_code}' -k https://#{host_inventory['hostname']}:#{service_port}#{url_relative_path}/") do
    it 'is expected to be equal' do
      expect(subject.stdout.to_i).to eq 200
    end
  end
end

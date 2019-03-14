require 'spec_helper'

grafana_host = 'localhost'
grafana_port = 3000

describe 'Checking if Grafana user exists' do
  describe group('grafana') do
    it { should exist }
  end
  describe user('grafana') do
    it { should exist }
    it { should belong_to_group 'grafana' }
  end
end

describe 'Checking Grafana directories and files' do
  let(:disable_sudo) { false }
  describe file('/var/lib/grafana') do
    it { should exist }
    it { should be_a_directory }
    it { should be_owned_by 'grafana' }
    it { should be_grouped_into 'grafana' }
  end
  describe file('/var/log/grafana') do
    it { should exist }
    it { should be_a_directory }
    it { should be_owned_by 'grafana' }
    it { should be_grouped_into 'grafana' }
  end
  describe file('/etc/grafana') do
    it { should exist }
    it { should be_a_directory }
    it { should be_owned_by 'root' }
    it { should be_grouped_into 'root' }
  end
  describe file("/etc/grafana/grafana.ini") do
    it { should exist }
    it { should be_a_file }
    it { should be_readable }
  end
end

describe 'Checking self signed SSL certificates' do
  let(:disable_sudo) { false }
  describe x509_private_key("/etc/grafana/ssl/grafana_key.key") do
    it { should be_valid }
    it { should have_matching_certificate('/etc/grafana/ssl/grafana_cert.pem') }
  end
  describe x509_certificate("/etc/grafana/ssl/grafana_cert.pem") do
    it { should be_certificate }
    it { should be_valid }
  end
end

describe 'Checking if Grafana package is installed' do
  describe package('grafana') do
    it { should be_installed }
  end
end

describe 'Checking if Grafana service is running' do
  describe service('grafana-server') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if the ports are open' do
  describe port(grafana_port) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end 

describe 'Checking Grafana health' do
  describe command("curl -o /dev/null -s -w '%{http_code}' -k https://#{grafana_host}:#{grafana_port}/login") do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq 200
    end
  end
  describe command("curl -k https://#{grafana_host}:#{grafana_port}/api/health") do
    its(:stdout_as_json) { should include('database' => 'ok') }
  end
end

describe 'Checking if Prometheus datasource exists' do
  let(:disable_sudo) { false }
  describe command("curl -k -u $(grep 'admin_user' /etc/grafana/grafana.ini | awk '{print $3}'):$(grep 'admin_password' /etc/grafana/grafana.ini | awk '{print $3}') \
  https://#{grafana_host}:#{grafana_port}/api/datasources/name/Prometheus") do
    its(:stdout_as_json) { should include('name' => 'Prometheus') }
    its(:stdout_as_json) { should include('type' => 'prometheus') }
  end
end

describe 'Checking Prometheus datasource availability' do
  let(:disable_sudo) { false }
  describe command("curl -k -o /dev/null -s -w '%{http_code}' -u $(grep 'admin_user' /etc/grafana/grafana.ini | awk '{print $3}'):$(grep 'admin_password' /etc/grafana/grafana.ini | awk '{print $3}') \
  https://#{grafana_host}:#{grafana_port}/api/datasources/proxy/1/api/v1/query?query=2%2B2") do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq 200
    end
  end
  describe command("curl -k -u $(grep 'admin_user' /etc/grafana/grafana.ini | awk '{print $3}'):$(grep 'admin_password' /etc/grafana/grafana.ini | awk '{print $3}') \
  https://#{grafana_host}:#{grafana_port}/api/datasources/proxy/1/api/v1/query?query=2%2B2") do
    its(:stdout_as_json) { should include('status' => 'success') }
  end
end

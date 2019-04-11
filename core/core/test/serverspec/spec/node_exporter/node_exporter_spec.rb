require 'spec_helper'

node_exporter_host = 'localhost'
node_exporter_port = 9100

describe 'Checking if Node Exporter user exists' do
  describe group('node_exporter') do
    it { should exist }
  end
  describe user('node_exporter') do
    it { should exist }
    it { should belong_to_group 'node_exporter' }
    it { should have_login_shell '/usr/sbin/nologin' }
  end
end

describe 'Checking Node Exporter directories and files' do
  let(:disable_sudo) { false }
  describe file('/opt/node_exporter') do
    it { should exist }
    it { should be_a_directory }
  end
  describe file("/opt/node_exporter/node_exporter") do
    it { should exist }
    it { should be_a_file }
    it { should be_executable }
  end
end

describe 'Checking if Node Exporter service is running' do
  describe service('prometheus-node-exporter') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if the ports are open' do
  describe port(node_exporter_port) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end 

describe 'Checking Node Exporter HTTP status code' do
  describe command("curl -o /dev/null -s -w '%{http_code}' #{node_exporter_host}:#{node_exporter_port}") do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq 200
    end
  end
end

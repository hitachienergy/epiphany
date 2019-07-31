require 'spec_helper'

kibana_default_port = 5601

describe 'Checking if Kibana package is installed' do
  describe package('kibana-oss') do
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

if count_inventory_roles("elasticsearch") > 0
  describe 'Checking the connection to the Elasticsearch host' do
    let(:disable_sudo) { false }
    describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP '(?<=elasticsearch.url: \\\").*(?=\\\")' /etc/kibana/kibana.yml)") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq 200
      end
    end
  end
end

describe 'Checking Kibana app HTTP status code' do
  let(:disable_sudo) { false }
  describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP '(?<=server.host: \\\").*(?=\\\")' /etc/kibana/kibana.yml):#{kibana_default_port}/app/kibana") do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq 200
    end
  end
end

describe 'Checking Kibana health' do
  let(:disable_sudo) { false }
  describe command("curl $(grep -oP '(?<=server.host: \\\").*(?=\\\")' /etc/kibana/kibana.yml):#{kibana_default_port}/api/status") do
    its(:stdout_as_json) { should include('status' => include('overall' => include('state' => 'green'))) }
    its(:exit_status) { should eq 0 }
  end
end

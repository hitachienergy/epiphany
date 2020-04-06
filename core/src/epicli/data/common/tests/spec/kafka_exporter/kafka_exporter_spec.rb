require 'spec_helper'

kafka_exporter_host = 'localhost'
kafka_exporter_web_listen_port = 9308

describe 'Checking if Kafka exporter process is running' do
  describe process('kafka_exporter') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if Kafka exporter user exists' do
  describe group('kafka_exporter') do
    it { should exist }
  end
  describe user('kafka_exporter') do
    it { should exist }
    it { should belong_to_group 'kafka_exporter' }
    it { should have_home_directory '/home/kafka_exporter' }
    it { should have_login_shell '/usr/sbin/nologin' }
  end
  describe file('/opt/kafka_exporter') do
    it { should exist }
    it { should be_grouped_into 'kafka_exporter' }
  end
end

describe 'Checking if the ports are open' do
  describe port(kafka_exporter_web_listen_port) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end 

describe 'Checking if it is possible to collect the metrics' do
  describe command("curl -s #{kafka_exporter_host}:#{kafka_exporter_web_listen_port}/metrics | grep -i kafka") do
    its(:stdout) { should match /kafka/ }
    its(:exit_status) { should eq 0 }
  end
end

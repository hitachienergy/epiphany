require 'spec_helper'

describe 'Checking if kafka_exporter process is up' do
  describe process('kafka_exporter') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking user configuration' do
  describe group('kafka_exporter') do
    it { should exist }
  end
  describe user('kafka_exporter') do
    it { should exist }
    it { should belong_to_group 'kafka_exporter' }
    it { should have_home_directory '/home/kafka_exporter' }
    it { should have_login_shell '/sbin/nologin' }
  end
end

describe file('/opt/kafka_exporter') do
  it { should exist }
  it { should be_grouped_into 'kafka_exporter' }
end

describe 'Checking if the ports are open' do
  describe port(9308) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end 

describe 'Collecting the metrics' do
  describe command('curl -s localhost:9308/metrics | grep -i kafka') do
    its(:stdout) { should match /kafka/ }
    its(:exit_status) { should eq 0 }
  end
end

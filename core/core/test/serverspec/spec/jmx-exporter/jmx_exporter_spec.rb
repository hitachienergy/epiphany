require 'spec_helper'

describe 'Checking user configuration' do
  describe group('jmx-exporter') do
    it { should exist }
  end
  describe user('jmx-exporter') do
    it { should exist }
    it { should belong_to_group 'jmx-exporter' }
    it { should have_home_directory '/home/jmx-exporter' }
    it { should have_login_shell '/sbin/nologin' }
  end
end

describe file('/opt/jmx-exporter') do
  it { should exist }
  it { should be_grouped_into 'jmx-exporter' }
end

describe 'Checking if the ports are open' do
  describe port(7071) do  #kafka
    let(:disable_sudo) { false }
    it { should be_listening }
  end
  describe port(7072) do  #zookeeper
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end 

describe 'Collecting the metrics from kafka' do
  describe command('curl -s localhost:7071 | grep -i kafka') do
    its(:stdout) { should match /kafka/ }
    its(:exit_status) { should eq 0 }
  end
end

describe 'Collecting the metrics from zookeeper' do
  describe command('curl -s localhost:7072 | grep -i zookeeper') do
    its(:stdout) { should match /zookeeper/ }
    its(:exit_status) { should eq 0 }
  end
end


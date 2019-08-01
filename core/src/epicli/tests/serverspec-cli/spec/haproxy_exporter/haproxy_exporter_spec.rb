require 'spec_helper'

haproxy_exporter_host = 'localhost'
haproxy_exporter_port = 9101

describe 'Checking if HAProxy Exporter user exists' do
  describe group('haproxy_exporter') do
    it { should exist }
  end
  describe user('haproxy_exporter') do
    it { should exist }
    it { should belong_to_group 'haproxy_exporter' }
    it { should have_home_directory '/home/haproxy_exporter' }
    it { should have_login_shell '/usr/sbin/nologin' }
  end
  describe file('/opt/haproxy_exporter') do
    it { should exist }
    it { should be_grouped_into 'haproxy_exporter' }
  end
end

describe 'Checking if HAProxy Exporter service is running' do
  describe service('prometheus-haproxy-exporter') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if the ports are open' do
  describe port(haproxy_exporter_port) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end 

describe 'Checking if it is possible to collect the metrics from HAProxy' do
  describe command("curl -s #{haproxy_exporter_host}:#{haproxy_exporter_port}/metrics | grep -i haproxy") do
    its(:stdout) { should match /haproxy_up 1/ }
    its(:stdout) { should_not match /haproxy_up 0/ }
    its(:exit_status) { should eq 0 }
  end
end

require 'spec_helper'
require_relative 'zookeeper_helpers'

kafka_host = 'localhost'
kafka_port = 9092
zookeeper_host = 'localhost'
zookeeper_client_port = 2181
zookeeper_peer_port = 2888
zookeeper_leader_port = 3888
zookeeper_admin_server_port = get_zookeeper_admin_server_port

describe 'Check if ZooKeeper service is running' do
  describe service('zookeeper') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Check if the ports are open' do

  # check port for client connections
  describe port(zookeeper_client_port) do
    let(:disable_sudo) { false } # required for RHEL
    it { should be_listening }
  end

  # check port for follower connections to the leader
  describe command("if /opt/zookeeper/bin/zkServer.sh status | grep 'Mode: leader'; then netstat -tunl | grep #{zookeeper_peer_port}; else echo 'not leader'; fi") do
    let(:disable_sudo) { false }
    its(:stdout) { should match /#{zookeeper_peer_port}|not leader/ }
    its(:exit_status) { should eq 0 }
  end

  # check port for leader election
  describe command("if /opt/zookeeper/bin/zkServer.sh status | grep 'Mode: standalone'; then echo 'standalone'; else netstat -tunl | grep #{zookeeper_leader_port}; fi") do
    let(:disable_sudo) { false }
    its(:stdout) { should match /#{zookeeper_leader_port}|standalone/ }
    its(:exit_status) { should eq 0 }
  end

  # check port for AdminServer
  describe port(zookeeper_admin_server_port) do
    let(:disable_sudo) { false } # required for RHEL
    it { should be_listening }
  end
end

describe 'Check if ZooKeeper user exists' do
  describe group('zookeeper') do
    it { should exist }
  end
  describe user('zookeeper') do
    it { should exist }
    it { should belong_to_group 'zookeeper' }
    it { should have_home_directory '/home/zookeeper' }
    it { should have_login_shell '/usr/sbin/nologin' }
  end
  describe file('/opt/zookeeper') do
    it { should exist }
    it { should be_directory }
  end
end

describe 'Check if ZooKeeper is healthy' do
  describe command("curl http://localhost:#{zookeeper_admin_server_port}/commands/stat") do
    its(:stdout_as_json) { should include('error' => nil) }
  end
  describe command("curl http://localhost:#{zookeeper_admin_server_port}/commands/ruok") do
    its(:stdout_as_json) { should include('error' => nil) }
  end
end

describe 'Check ZooKeeper status' do
  describe command('/opt/zookeeper/bin/zkServer.sh status 2>&1') do
    let(:disable_sudo) { false }
    let(:sudo_options) { '-u zookeeper' }
    its(:stdout) { should match /Mode: leader|Mode: follower|Mode: standalone/ }
    its(:stdout) { should_not match /Error contacting service. It is probably not running./ }
  end
end

describe 'Check ZooKeeper client' do
  describe command("echo 'quit' | /opt/zookeeper/bin/zkCli.sh -server #{zookeeper_host}:#{zookeeper_client_port}") do
    let(:disable_sudo) { false }
    let(:sudo_options) { '-u zookeeper' }
    its(:stdout) { should match /Welcome to ZooKeeper!/ }
    its(:exit_status) { should eq 0 }
  end
end

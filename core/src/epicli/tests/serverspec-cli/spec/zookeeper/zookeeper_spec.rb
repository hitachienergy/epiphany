require 'spec_helper'

kafka_host = 'localhost'
kafka_port = 9092
zookeeper_host = 'localhost'
zookeeper_client_port = 2181
zookeeper_peer_port = 2888
zookeeper_leader_port = 3888

describe 'Checking if ZooKeeper service is running' do
  describe service('zookeeper') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if the ports are open' do

  # checking port for client connections
  describe port(zookeeper_client_port) do 
    let(:disable_sudo) { false }  
    it { should be_listening }
  end
 
  # checking port for follower connections to the leader
  describe command("if /opt/zookeeper/bin/zkServer.sh status | grep 'Mode: leader'; then netstat -tunl | grep #{zookeeper_peer_port}; else echo 'not leader'; fi") do
    its(:stdout) { should match /#{zookeeper_peer_port}|not leader/ }
    its(:exit_status) { should eq 0 }
  end

  # checking port for leader election
  describe command("if /opt/zookeeper/bin/zkServer.sh status | grep 'Mode: standalone'; then echo 'standalone'; else netstat -tunl | grep #{zookeeper_leader_port}; fi") do
    its(:stdout) { should match /#{zookeeper_leader_port}|standalone/ }
    its(:exit_status) { should eq 0 }
  end
end  

describe 'Checking if ZooKeeper user exists' do
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

describe 'Checking if ZooKeeper is healthy' do
  describe command("echo 'stat' | curl -s telnet://#{zookeeper_host}:#{zookeeper_client_port}") do
    its(:stdout) { should match /Zookeeper version/ }
  end
  describe command("echo 'ruok' | curl -s telnet://#{zookeeper_host}:#{zookeeper_client_port}") do
    its(:stdout) { should match /imok/ }
  end
end

describe 'Checking ZooKeeper status' do
  describe command('/opt/zookeeper/bin/zkServer.sh status 2>&1') do
    its(:stdout) { should match /Mode: leader|Mode: follower|Mode: standalone/ }
    its(:stdout) { should_not match /Error contacting service. It is probably not running./ }
  end
end  

describe 'Checking if it is possible to list down and count all the active brokers' do
  describe command("echo 'ls /brokers/ids' | /opt/zookeeper/bin/zkCli.sh -server #{zookeeper_host}:#{zookeeper_client_port}") do
    its(:stdout) { should match /Welcome to ZooKeeper!/ }
    its(:stdout) { should match /\[(\d+(\,\s)?)+\]/ } # pattern: [0, 1, 2, 3 ...]
    its(:exit_status) { should eq 0 }
  end
  describe command("echo 'dump' | curl -s telnet://#{zookeeper_host}:#{zookeeper_client_port} | grep brokers") do
    its(:stdout) { should match /\/brokers\/ids\/\d+/ } # pattern: /brokers/ids/0
    its(:exit_status) { should eq 0 }
  end  
  describe command("echo 'dump' | curl -s telnet://#{zookeeper_host}:#{zookeeper_client_port} | grep -c brokers") do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq countInventoryHosts("kafka")  
    end  
  end
end

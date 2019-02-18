require 'spec_helper'

describe 'Checking if zookeeper service is up' do
  describe service('zookeeper') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if the ports are open' do
  describe port(2181) do            #2181 for client connections
    let(:disable_sudo) { false }  
    it { should be_listening }
  end

  # These ports are not always open. Depends on configuration.
  # describe port(2888) do          #2888 for follower connections
  #   let(:disable_sudo) { false }
  #   it { should be_listening }
  # end
  # describe port(3888) do          #3888 for inter nodes connections
  #   let(:disable_sudo) { false }
  #   it { should be_listening }
  # end

  #checking port 2888
  describe command('if /opt/zookeeper/bin/zkServer.sh status | grep "Mode: leader"; then netstat -tunl | grep 2888; else echo "not leader"; fi') do
    its(:stdout) { should match /2888|not leader/ }
    its(:exit_status) { should eq 0 }
  end

  #checking port 3888
  describe command('if /opt/zookeeper/bin/zkServer.sh status | grep "Mode: standalone"; then echo "standalone"; else netstat -tunl | grep 3888; fi') do
    its(:stdout) { should match /3888|standalone/ }
    its(:exit_status) { should eq 0 }
  end
end  


describe 'Checking user configuration' do
  describe group('zookeeper') do
    it { should exist }
  end
  describe user('zookeeper') do
    it { should exist }
    it { should belong_to_group 'zookeeper' }
    it { should have_home_directory '/home/zookeeper' }
    it { should have_login_shell '/sbin/nologin' }
  end
  describe file('/opt/zookeeper') do
    it { should exist }
    it { should be_directory }
  end
end

describe 'Checking if zookeeper is healthy' do
  describe command("echo stat | nc -q 2 localhost 2181") do
    its(:stdout) { should match /Zookeeper version/ }
    its(:exit_status) { should eq 0 }
  end
  describe command("echo ruok | nc -q 2 localhost 2181") do
    its(:stdout) { should match /imok/ }
    its(:exit_status) { should eq 0 }
  end
end

describe 'Checking zookeeper status' do
  describe command('/opt/zookeeper/bin/zkServer.sh status 2>&1') do
    its(:stdout) { should match /Mode: leader|Mode: follower|Mode: standalone/ }
    its(:stdout) { should_not match /Error contacting service. It is probably not running./ }
  end
end  

describe 'Listing down all the active brokers' do
  describe command('echo "ls /brokers/ids" | /opt/zookeeper/bin/zkCli.sh -server localhost:2181') do
    its(:stdout) { should match /Welcome to ZooKeeper!/ }
    its(:stdout) { should match /\[(\d+(\,\s)?)+\]/ } # pattern: [0, 1, 2, 3 ...]
    its(:exit_status) { should eq 0 }
  describe command("echo dump | nc -q 2 localhost 2181 | grep brokers") do
    its(:stdout) { should match /\/brokers\/ids\/\d+/ } # pattern: /brokers/ids/0
    its(:exit_status) { should eq 0 }
    end  
  end
end


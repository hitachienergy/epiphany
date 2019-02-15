require 'spec_helper'

describe 'Checking if kafka service is up' do
  describe service('kafka') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking user configuration' do
  describe group('kafka') do
    it { should exist }
  end
  describe user('kafka') do
    it { should exist }
    it { should belong_to_group 'kafka' }
    it { should have_home_directory '/home/kafka' }
    it { should have_login_shell '/sbin/nologin' }
  end
end

describe 'Checking if the ports are open' do
  describe port(9092) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end  

describe 'Listing down all the active brokers' do
  describe command('/opt/kafka/bin/zookeeper-shell.sh localhost:2181 <<< "ls /brokers/ids"') do
    its(:stdout) { should match /Welcome to ZooKeeper!/ }
    its(:stdout) { should match /\[(\d+(\,\s)?)+\]/ }  # pattern: [0, 1, 2, 3 ...]
    its(:exit_status) { should eq 0 }
  end
end

describe 'Checking if the number of kafka brokers is the same as indicated in the inventory file' do
  describe command('echo dump | nc localhost 2181 | grep -c brokers | tr -d "\n"') do
    it "is expected to be equal" do
    expect(subject.stdout.to_i).to eq count_inventory_roles("kafka")
    end
  end
end


describe 'Creating topic, producing and consuming messages' do

  kafka_brokers_count = count_inventory_roles("kafka")
  timestamp = DateTime.now.to_time.to_i.to_s
  topic_name = 'topic' + timestamp
  partitions = kafka_brokers_count*3
  message = 'test message 1'
  message2 = 'test message 2'
  message3 = 'test message 3'

  describe 'Creating topic' do
    describe command("/opt/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor #{kafka_brokers_count} \
    --partitions #{partitions} --topic #{topic_name}") do
      its(:stdout) { should match /Created topic "#{topic_name}"./ }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Starting consumer process' do
    describe command("/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic #{topic_name} >> /tmp/#{topic_name}.txt 2>&1 &") do
      its(:exit_status) { should eq 0 }
    end
  end


  describe 'Waiting 5 sec for consumer process to be started' do 
    describe command('sleep 5') do
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Sending message 1 from producer' do 
    describe command("echo '#{message}' | /opt/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic #{topic_name}") do
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Sending message 2 from producer' do 
    describe command("echo '#{message2}' | /opt/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic #{topic_name}") do
      its(:exit_status) { should eq 0 }
    end
  end
  
  describe 'Sending message 3 from producer' do 
    describe command("echo '#{message3}' | /opt/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic #{topic_name}") do
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Verifying consumer output' do 
    describe command("cat /tmp/#{topic_name}.txt") do
      its(:stdout) { should match /#{message}/ }
      its(:stdout) { should match /#{message2}/ }
      its(:stdout) { should match /#{message3}/ }
    end
  end

  describe 'Listing down the topics available in kafka' do
    describe command('/opt/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181') do
      its(:stdout) { should match /#{topic_name}/ }
    end
  end  

  describe 'Cleaning up' do
    describe command("rm /tmp/#{topic_name}.txt") do  # delete temp txt file containing output
      its(:exit_status) { should eq 0 }
    end
    describe file("/tmp/#{topic_name}.txt") do
      it { should_not exist }
    end
    describe command("kill -9 $(ps aux | grep -i 'kafka.tools.ConsoleConsumer' | grep '#{topic_name}' | grep -v 'grep' | awk '{print $2}')") do  # stop consumer process
    its(:exit_status) { should eq 0 }
  end
  end  
end

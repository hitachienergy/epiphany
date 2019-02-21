require 'spec_helper'

kafka_host = 'localhost'
kafka_port = 9092
zookeeper_host = 'localhost'
zookeeper_client_port = 2181

describe 'Checking if Kafka service is running' do
  describe service('kafka') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if Kafka user exists' do
  describe group('kafka') do
    it { should exist }
  end
  describe user('kafka') do
    it { should exist }
    it { should belong_to_group 'kafka' }
    it { should have_home_directory '/home/kafka' }
    it { should have_login_shell '/usr/sbin/nologin' }
  end
end

describe 'Checking if the ports are open' do
  describe port(kafka_port) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end  

describe 'Listing down all the active brokers' do
  describe command("echo 'ls /brokers/ids' | /opt/kafka/bin/zookeeper-shell.sh #{zookeeper_host}:#{zookeeper_client_port}") do
    its(:stdout) { should match /Welcome to ZooKeeper!/ }
    its(:stdout) { should match /\[(\d+(\,\s)?)+\]/ }  # pattern: [0, 1, 2, 3 ...]
    its(:exit_status) { should eq 0 }
  end
end

describe 'Checking if the number of Kafka brokers is the same as indicated in the inventory file' do
  describe command("echo 'dump' | curl -s telnet://#{zookeeper_host}:#{zookeeper_client_port} | grep -c brokers") do
    it "is expected to be equal" do
    expect(subject.stdout.to_i).to eq count_inventory_roles("kafka")
    end
  end
end

describe 'Checking the possibility of creating a topic, producing and consuming messages' do

  kafka_brokers_count = count_inventory_roles("kafka")
  timestamp = DateTime.now.to_time.to_i.to_s
  topic_name = 'topic' + timestamp
  partitions = kafka_brokers_count*3
  message = 'test message'

  describe 'Checking if the topic was created' do
    describe command("/opt/kafka/bin/kafka-topics.sh --create --zookeeper #{zookeeper_host}:#{zookeeper_client_port} --replication-factor #{kafka_brokers_count} \
    --partitions #{partitions} --topic #{topic_name}") do
      its(:stdout) { should match /Created topic "#{topic_name}"./ }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Starting consumer process' do
    describe command("/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server #{kafka_host}:#{kafka_port} --topic #{topic_name} --consumer-property group.id=TESTGROUP \
    >> /tmp/#{topic_name}.txt 2>&1 &") do
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if consumer process is ready' do 
    describe command("for i in {1..10}; do if /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server #{kafka_host}:#{kafka_port} --group TESTGROUP --describe \
      | grep #{topic_name}; then echo 'READY'; break; else echo 'WAITING'; sleep 0.5; fi; done;") do
      its(:stdout) { should match /#{topic_name}/ }
      its(:stdout) { should match /\bREADY\b/ }
    end
  end

  10.times do |i|
    describe "Sending message #{i+1} from producer" do 
      describe command("echo '#{message} #{i+1}' | /opt/kafka/bin/kafka-console-producer.sh --broker-list #{kafka_host}:#{kafka_port} --topic #{topic_name}") do
        its(:exit_status) { should eq 0 }
      end
    end
    describe 'Checking if the consumer output contains the message that was produced' do 
      describe command("cat /tmp/#{topic_name}.txt") do
        its(:stdout) { should match /^#{message} #{i+1}$/ }
      end
    end
  end

  describe 'Checking if the created topic is on the list with all available topics in Kafka' do
    describe command("/opt/kafka/bin/kafka-topics.sh --list --zookeeper #{zookeeper_host}:#{zookeeper_client_port}") do
      its(:stdout) { should match /#{topic_name}/ }
    end
  end  

  describe 'Cleaning up' do
    describe command("/opt/kafka/bin/kafka-topics.sh --delete --zookeeper #{zookeeper_host}:#{zookeeper_client_port} --topic #{topic_name}") do
      its(:stdout) { should match /Topic #{topic_name} is marked for deletion./ }
      its(:exit_status) { should eq 0 }
    end
    describe command("rm /tmp/#{topic_name}.txt") do
      its(:exit_status) { should eq 0 }
    end
    describe file("/tmp/#{topic_name}.txt") do
      it { should_not exist }
    end
    describe command("kill -9 $(ps aux | grep -i 'kafka.tools.ConsoleConsumer' | grep '#{topic_name}' | grep -v 'grep' | awk '{print $2}')") do
      its(:exit_status) { should eq 0 }
    end
  end  
end

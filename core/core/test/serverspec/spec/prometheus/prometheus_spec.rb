require 'spec_helper'

prometheus_host = 'localhost'
prometheus_port = 9090

describe 'Checking if Prometheus user exists' do
  describe group('prometheus') do
    it { should exist }
  end
  describe user('prometheus') do
    it { should exist }
    it { should belong_to_group 'prometheus' }
    it { should have_login_shell '/usr/sbin/nologin' }
  end
end

describe 'Checking Prometheus directories and files' do
  let(:disable_sudo) { false }
  describe file('/var/lib/prometheus') do
    it { should exist }
    it { should be_a_directory }
    it { should be_owned_by 'prometheus' }
    it { should be_grouped_into 'prometheus' }
  end
  describe file('/etc/prometheus') do
    it { should exist }
    it { should be_a_directory }
    it { should be_owned_by 'root' }
    it { should be_grouped_into 'prometheus' }
  end
  describe file("/etc/prometheus/prometheus.yml") do
    it { should exist }
    it { should be_a_file }
    it { should be_readable }
  end
end

describe 'Checking if Prometheus service is running' do
  describe service('prometheus') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if the ports are open' do
  describe port(prometheus_port) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end 

describe 'Checking Prometheus health' do
  describe command("curl -o /dev/null -s -w '%{http_code}' #{prometheus_host}:#{prometheus_port}/graph") do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq 200
    end
  end
  describe command("curl #{prometheus_host}:#{prometheus_port}/-/ready") do
    its(:stdout) { should match /^Prometheus is Ready.$/ }
  end
  describe command("curl #{prometheus_host}:#{prometheus_port}/-/healthy") do
    its(:stdout) { should match /^Prometheus is Healthy.$/ }
  end
end

describe 'Checking if Prometheus is serving metrics about itself' do
    describe command("curl -o /dev/null -s -w '%{http_code}' #{prometheus_host}:#{prometheus_port}/metrics") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq 200
      end
    end
    describe command("curl #{prometheus_host}:#{prometheus_port}/metrics") do
      its(:stdout) { should_not match /^$/ }
    end
  end


describe 'Checking configuration files for Node exporter' do
    listInventoryHosts("node_exporter").each do |val|
        describe command("ls /etc/prometheus/file_sd") do
        let(:disable_sudo) { false }
        its(:stdout) { should match /node-#{val}.yml/ }
        end
    end
end 

describe 'Checking connection to Node exporter hosts' do
    listInventoryHosts("node_exporter").each do |val|
        let(:disable_sudo) { false }
        describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP \"(?<=targets: \\\[\').*(?=\'\\\])\" /etc/prometheus/file_sd/node-#{val}.yml)") do
          it "is expected to be equal" do
            expect(subject.stdout.to_i).to eq 200
          end
        end
    end
end 

describe 'Checking configuration files for HAProxy Exporter' do
    listInventoryHosts("haproxy_exporter").each do |val|
        describe command("ls /etc/prometheus/file_sd") do
        let(:disable_sudo) { false }
        its(:stdout) { should match /haproxy-#{val}.yml/ }
        end
    end
end 

describe 'Checking connection to HAProxy Exporter' do
    listInventoryHosts("haproxy_exporter").each do |val|
        let(:disable_sudo) { false }
        describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP \"(?<=targets: \\\[\\\").*(?=\\\"\\\])\" /etc/prometheus/file_sd/haproxy-#{val}.yml)") do
          it "is expected to be equal" do
            expect(subject.stdout.to_i).to eq 200
          end
        end
    end
end 

describe 'Checking configuration files for JMX exporter' do
    listInventoryHosts("jmx-exporter").each do |val|
        describe command("ls /etc/prometheus/file_sd") do
        let(:disable_sudo) { false }
        its(:stdout) { should match /kafka-jmx-#{val}.yml/ }
        its(:stdout) { should match /zookeeper-jmx-#{val}.yml/ }
        end
    end
end 

describe 'Checking connection to JMX exporter hosts' do
    listInventoryHosts("jmx-exporter").each do |val|
        let(:disable_sudo) { false }
        describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP \"(?<=targets: \\\[\').*(?=\'\\\])\" /etc/prometheus/file_sd/kafka-jmx-#{val}.yml)") do
          it "is expected to be equal" do
            expect(subject.stdout.to_i).to eq 200
          end
        end
        describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP \"(?<=targets: \\\[\').*(?=\'\\\])\" /etc/prometheus/file_sd/zookeeper-jmx-#{val}.yml)") do
        it "is expected to be equal" do
          expect(subject.stdout.to_i).to eq 200
        end
      end
    end
end 

describe 'Checking configuration files for Kafka Exporter hosts' do
    listInventoryHosts("kafka-exporter").each do |val|
        describe command("ls /etc/prometheus/file_sd") do
        let(:disable_sudo) { false }
        its(:stdout) { should match /kafka-exporter-#{val}.yml/ }
        end
    end
end 

describe 'Checking connection to Kafka Exporter hosts' do
    listInventoryHosts("kafka-exporter").each do |val|
        let(:disable_sudo) { false }
        describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP \"(?<=targets: \\\[\').*(?=\'\\\])\" /etc/prometheus/file_sd/kafka-exporter-#{val}.yml)") do
          it "is expected to be equal" do
            expect(subject.stdout.to_i).to eq 200
          end
        end
    end
end 


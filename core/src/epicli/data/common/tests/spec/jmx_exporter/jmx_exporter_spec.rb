require 'spec_helper'

jmx_exporter_host = 'localhost'
jmx_exporter_port_for_kafka = 7071
jmx_exporter_port_for_zookeeper = 7072

describe 'Checking if JMX Exporter user exists' do
  describe group('jmx-exporter') do
    it { should exist }
  end
  describe user('jmx-exporter') do
    it { should exist }
    it { should belong_to_group 'jmx-exporter' }
    it { should have_home_directory '/home/jmx-exporter' }
    it { should have_login_shell '/usr/sbin/nologin' }
  end
  describe file('/opt/jmx-exporter') do
    it { should exist }
    it { should be_grouped_into 'jmx-exporter' }
  end
end

describe 'Checking if the ports are open' do
  describe port(jmx_exporter_port_for_kafka) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
  describe port(jmx_exporter_port_for_zookeeper) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end 

describe 'Checking if it is possible to collect the metrics from Kafka' do
  describe command("curl -s #{jmx_exporter_host}:#{jmx_exporter_port_for_kafka} | grep -i ^kafka") do
    its(:stdout) { should match /kafka/ }
    its(:exit_status) { should eq 0 }
  end
end

if countInventoryHosts("kafka") == 1
  describe 'Checking if it is possible to collect any jvm metrics' do
    describe command("curl -s #{jmx_exporter_host}:#{jmx_exporter_port_for_zookeeper} | grep -i ^jvm_memory") do
      its(:exit_status) { should eq 0 }
    end
  end
elsif countInventoryHosts("kafka") > 1
  describe 'Checking if it is possible to collect the metrics from ZooKeeper' do
    describe command("curl -s #{jmx_exporter_host}:#{jmx_exporter_port_for_zookeeper} | grep -i ^zookeeper") do
      its(:stdout) { should match /zookeeper/ }
      its(:exit_status) { should eq 0 }
    end
  end
end

require 'spec_helper'
require 'securerandom'

rabbitmq_host = 'localhost'
rabbitmq_port = 5672

if readDataYaml["rabbitmq"] && readDataYaml["rabbitmq"]["amqp_port"]
  rabbitmq_port = readDataYaml["rabbitmq"]["amqp_port"]
end

rabbitmq_node_port = rabbitmq_port + 20000
rabbitmq_api_port = 15672

clustered = false

user = 'testuser'
pass = SecureRandom.hex


if readDataYaml["rabbitmq"] && readDataYaml["rabbitmq"]["cluster"] && readDataYaml["rabbitmq"]["cluster"]["is_clustered"] && 
  readDataYaml["rabbitmq"]["cluster"]["is_clustered"] == true
    clustered = true
end

describe 'Checking if RabbitMQ package is installed' do
  describe package('rabbitmq-server') do
    it { should be_installed }
  end
end

describe 'Checking if RabbitMQ user exists' do
  describe group('rabbitmq') do
    it { should exist }
  end
  describe user('rabbitmq') do
    it { should exist }
    it { should belong_to_group 'rabbitmq' }
  end
end

describe 'Checking if RabbitMQ service is running' do
  describe service('rabbitmq-server') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if the ports are open' do
  let(:disable_sudo) { false }
  describe port(rabbitmq_port) do
    it { should be_listening }
  end
  describe port(rabbitmq_node_port) do
    it { should be_listening }
  end
end  

describe 'Checking RabbitMQ ping' do
  describe command("rabbitmqctl ping") do
    let(:disable_sudo) { false }
    its(:stdout) { should match /^Ping succeeded$/ }
    its(:exit_status) { should eq 0 }
  end
end  

describe 'Checking the health of the target nodes' do
  let(:disable_sudo) { false }
  if clustered == true
    listInventoryHosts("rabbitmq").each do |val|
      describe command("rabbitmqctl node_health_check -n rabbit@#{val}") do
        its(:stdout) { should match /^Health check passed$/ }
        its(:exit_status) { should eq 0 }
      end
    end
  else
    describe command("rabbitmqctl node_health_check -n rabbit@#{host_inventory['hostname']}") do
      its(:stdout) { should match /^Health check passed$/ }
      its(:exit_status) { should eq 0 }
    end
  end
end

describe 'Checking the RabbitMQ status/cluster status' do
  let(:disable_sudo) { false }
  describe command("rabbitmqctl status") do
    its(:exit_status) { should eq 0 }
  end
  if clustered
    listInventoryHosts("rabbitmq").each do |val|
      describe command("rabbitmqctl cluster_status | awk '/running_nodes/,/}/'") do
        its(:stdout) { should match /rabbit@#{val}/ }
        its(:exit_status) { should eq 0 }
      end
    end
  else
    describe command("rabbitmqctl cluster_status | awk '/running_nodes/,/}/'") do
      its(:stdout) { should match /rabbit@#{host_inventory['hostname']}/ }
      its(:exit_status) { should eq 0 }
    end
  end
end

describe 'Checking if it is possible to create the test user' do
  describe command("rabbitmqctl add_user #{user} #{pass} && rabbitmqctl set_user_tags #{user} administrator \
  && rabbitmqctl set_permissions -p / #{user} \".*\" \".*\" \".*\"") do
    let(:disable_sudo) { false }
    its(:stdout) { should match /Adding user "#{user}"/ }
    its(:stdout) { should match /Setting tags for user "#{user}" to \[administrator\]/ } 
    its(:stdout) { should match /Setting permissions for user "#{user}"/ }
    its(:exit_status) { should eq 0 }
  end
end

# Tests to be run only when RabbitMQ plugins section is enabled

plugins = []

if readDataYaml["rabbitmq"] && readDataYaml["rabbitmq"]["plugins"]
  plugins = readDataYaml["rabbitmq"]["plugins"]
end

describe 'Checking if RabbitMQ plugins are enabled' do
  plugins.each do |val|
    describe command("rabbitmq-plugins list -e") do
      let(:disable_sudo) { false }
      its(:stdout) { should match /\b#{val}\b/ }
      its(:exit_status) { should eq 0 }
    end
  end
end 

# Tests to be run only when RabbitMQ Management Plugin is enabled

if plugins.include? "rabbitmq_management"

  describe 'Checking if the port for RabbitMQ Management Plugin is open' do
    let(:disable_sudo) { false }
    describe port(rabbitmq_api_port) do
      it { should be_listening }
    end
  end  
 
  describe 'Checking nodes health using RabbitMQ API' do
    let(:disable_sudo) { false }
    if clustered
      listInventoryHosts("rabbitmq").each do |val|
        describe command("curl -o /dev/null -s -w '%{http_code}' -u #{user}:#{pass} #{rabbitmq_host}:#{rabbitmq_api_port}/api/healthchecks/node/rabbit@#{val}") do
          it "is expected to be equal" do
            expect(subject.stdout.to_i).to eq 200
          end
        end
        describe command("curl -u #{user}:#{pass} #{rabbitmq_host}:#{rabbitmq_api_port}/api/healthchecks/node/rabbit@#{val}") do
          its(:stdout_as_json) { should include('status' => /ok/) }
          its(:stdout_as_json) { should_not include('status' => /failed/) }
          its(:exit_status) { should eq 0 }
        end
      end
    else
      describe command("curl -o /dev/null -s -w '%{http_code}' -u #{user}:#{pass} #{rabbitmq_host}:#{rabbitmq_api_port}/api/healthchecks/node/rabbit@#{host_inventory['hostname']}") do
        it "is expected to be equal" do
          expect(subject.stdout.to_i).to eq 200
        end
      end
      describe command("curl -u #{user}:#{pass} #{rabbitmq_host}:#{rabbitmq_api_port}/api/aliveness-test/%2F") do
        its(:stdout_as_json) { should include('status' => /ok/) }
        its(:stdout_as_json) { should_not include('status' => /failed/) }
        its(:exit_status) { should eq 0 }
      end
    end
  end
end

describe 'Cleaning up' do
  describe command("rabbitmqctl delete_user #{user}") do
    let(:disable_sudo) { false }
    its(:stdout) { should match /Deleting user "#{user}"/ }
    its(:exit_status) { should eq 0 }
  end
end


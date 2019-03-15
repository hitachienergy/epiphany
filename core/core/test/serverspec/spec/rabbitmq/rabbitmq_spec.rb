require 'spec_helper'

rabbitmq_host = 'localhost'
rabbitmq_port = 5672

if readDataYaml["rabbitmq"].has_key? "amqp_port"
  rabbitmq_port = readDataYaml["rabbitmq"]["amqp_port"]
end

# describe 'Checking if RabbitMQ package is installed' do
#   describe package('rabbitmq-server') do
#     it { should be_installed }
#   end
# end

# describe 'Checking if RabbitMQ user exists' do
#   describe group('rabbitmq') do
#     it { should exist }
#   end
#   describe user('rabbitmq') do
#     it { should exist }
#     it { should belong_to_group 'rabbitmq' }
#     it { should have_login_shell '/usr/sbin/nologin' }
#   end
# end

# describe 'Checking if RabbitMQ service is running' do
#   describe service('rabbitmq-server') do
#     it { should be_enabled }
#     it { should be_running }
#   end
# end

# describe 'Checking if the ports are open' do
#   describe port(rabbitmq_port) do
#     let(:disable_sudo) { false }
#     it { should be_listening }
#   end
# end  

describe 'Checking RabbitMQ status' do
  describe command("rabbitmq-diagnostics ping") do
    let(:disable_sudo) { false }
    its(:stdout) { should match /^Ping succeeded$/ }
    its(:exit_status) { should eq 0 }
  end
end  


# curl -u guest:guest localhost:15672/api/healthchecks/nod
# enable rabbitmq_management


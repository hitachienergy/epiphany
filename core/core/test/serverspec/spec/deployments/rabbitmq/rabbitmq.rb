require 'spec_helper'
require 'securerandom'

def callRabbitMQDeploymentTests

  rabbitmq_amqp_port = 5672
  rabbitmq_http_port = 15672
  service_namespace = 'default'
  service_name = ''
  user = 'testuser'
  pass = SecureRandom.hex

  rabbitmq_deployment_array_index = readDataYaml["kubernetes"]["deployments"].index {|h| h["name"] == "rabbitmq" }
  service_port = readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"service","port")
  service_management_port = readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"service","management_port")
  service_replicas = readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"service","replicas")

  if readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"rabbitmq","amqp_port")
    rabbitmq_amqp_port = readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"rabbitmq","amqp_port")
  end

  if readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"service","namespace")
    service_namespace = readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"service","namespace")
  end

  if readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"service","name")
    service_name = readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"service","name")
  else service_name = 'rabbit-' + service_namespace
  end

  if readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"rabbitmq","plugins")
    plugins = readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"rabbitmq","plugins")
  end

  describe 'Checking if RabbitMQ service is running' do
    describe command("kubectl get services --namespace=#{service_namespace}") do
      its(:stdout) { should match /#{service_name}/ }
    end
  end

  describe 'Checking if the ports are open' do
    describe port(service_port) do
      let(:disable_sudo) { false }
      it { should be_listening }
    end
    describe command("kubectl describe service #{service_name} --namespace=#{service_namespace} | grep TargetPort") do
      its(:stdout) { should match /#{rabbitmq_amqp_port}/ }
    end
  end  

  describe 'Checking the status of RabbitMQ pods - all pods should be running' do
    describe command("kubectl get pods --namespace=#{service_namespace} --field-selector=status.phase=Running | grep #{service_name} | wc -l") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq service_replicas
      end
      its(:exit_status) { should eq 0 }
    end
  end  

  describe 'Checking RabbitMQ ping' do
    service_replicas.times do |i|
      describe command("kubectl exec --namespace=#{service_namespace} #{service_name}-#{i} -- rabbitmqctl ping") do
        its(:stdout) { should match /^Ping succeeded$/ }
        its(:exit_status) { should eq 0 }
      end
    end
  end  

  describe 'Checking the health of target nodes' do
    service_replicas.times do |i|
      describe command("kubectl exec --namespace=#{service_namespace} #{service_name}-#{i} -- rabbitmqctl node_health_check") do
        its(:stdout) { should match /^Health check passed$/ }
        its(:exit_status) { should eq 0 }
      end
    end
  end

  describe 'Checking the status of RabbitMQ nodes' do
    service_replicas.times do |i|
      describe command("kubectl exec --namespace=#{service_namespace} #{service_name}-#{i} -- rabbitmqctl status") do
        its(:exit_status) { should eq 0 }
      end
      describe command("kubectl exec --namespace=#{service_namespace} #{service_name}-#{i} -- rabbitmqctl cluster_status \
      | awk '/running_nodes/,/}/' | grep -o rabbit@ | wc -l") do
        it "is expected to be equal" do
          expect(subject.stdout.to_i).to eq service_replicas
        end
        its(:exit_status) { should eq 0 }
      end
    end
  end

  describe 'Checking if it is possible to create a test user on each replica' do
    service_replicas.times do |i|
      describe command("kubectl exec --namespace=#{service_namespace} #{service_name}-#{i} -- bash -c \"rabbitmqctl add_user #{user}#{i} #{pass} \
      && rabbitmqctl set_user_tags #{user}#{i} administrator && rabbitmqctl set_permissions -p / #{user}#{i} '.*' '.*' '.*'\"") do
        its(:stdout) { should match /Adding user "#{user}#{i}"/ }
        its(:stdout) { should match /Setting tags for user "#{user}#{i}" to \[administrator\]/ } 
        its(:stdout) { should match /Setting permissions for user "#{user}#{i}"/ }
        its(:exit_status) { should eq 0 }
      end
    end
  end

  # # Tests to be run only when RabbitMQ plugins section is enabled

  plugins = []

  if readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"rabbitmq","plugins")
    plugins = readDataYaml.dig("kubernetes","deployments","#{rabbitmq_deployment_array_index}".to_i,"rabbitmq","plugins")
  end

  describe 'Checking if RabbitMQ plugins are enabled' do
    service_replicas.times do |i|
      plugins.each do |plugin|
        describe command("kubectl exec --namespace=#{service_namespace} #{service_name}-#{i} -- rabbitmq-plugins list -e") do
          its(:stdout) { should match /\b#{plugin}\b/ }
          its(:exit_status) { should eq 0 }
        end
      end
    end
  end 

  # Tests to be run only when RabbitMQ Management Plugin is enabled

  if plugins.include? "rabbitmq_management"

    describe 'Checking if the port for RabbitMQ Management Plugin is open' do
      describe port(service_management_port) do
        let(:disable_sudo) { false }
        it { should be_listening }
      end
      describe command("kubectl describe service #{service_name} --namespace=#{service_namespace} | grep TargetPort") do
        its(:stdout) { should match /#{rabbitmq_http_port}/ }
      end
    end  
  
    describe 'Checking node health using RabbitMQ API' do
      service_replicas.times do |i|
        describe command("curl -o /dev/null -s -w '%{http_code}' -u #{user}#{i}:#{pass} \
        #{host_inventory['hostname']}:#{service_management_port}/api/healthchecks/node/rabbit@$(kubectl describe pods rabbitmq-cluster-#{i} \
        --namespace=#{service_namespace} | grep ^IP: | awk '{print $2}')") do
          it "is expected to be equal" do
            expect(subject.stdout.to_i).to eq 200
          end
        end
        describe command("curl -u #{user}#{i}:#{pass} \
        #{host_inventory['hostname']}:#{service_management_port}/api/healthchecks/node/rabbit@$(kubectl describe pods rabbitmq-cluster-#{i} \
        --namespace=#{service_namespace} | grep ^IP: | awk '{print $2}')") do
          its(:stdout_as_json) { should include('status' => /ok/) }
          its(:stdout_as_json) { should_not include('status' => /failed/) }
          its(:exit_status) { should eq 0 }
        end
        describe command("curl -u #{user}#{i}:#{pass} #{host_inventory['hostname']}:#{service_management_port}/api/aliveness-test/%2F") do
          its(:stdout_as_json) { should include('status' => /ok/) }
          its(:stdout_as_json) { should_not include('status' => /failed/) }
          its(:exit_status) { should eq 0 }
        end
      end
    end
  end 

  describe 'Cleaning up' do
    service_replicas.times do |i|
      describe command("kubectl exec --namespace=#{service_namespace} #{service_name}-#{i} -- rabbitmqctl delete_user #{user}#{i}") do
        its(:stdout) { should match /Deleting user "#{user}#{i}"/ }
        its(:exit_status) { should eq 0 }
      end
    end
  end

end 

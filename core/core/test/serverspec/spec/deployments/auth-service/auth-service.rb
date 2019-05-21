require 'spec_helper'
require 'securerandom'

def callAuthServiceDeploymentTests

  auth_service_array_index = readDataYaml["kubernetes"]["deployments"].index {|h| h["name"] == "auth-service" }
  service_namespace = 'default'
  service_name = ''
  service_port = readDataYaml.dig("kubernetes","deployments","#{auth_service_array_index}".to_i,"service","port")
  service_replicas = readDataYaml.dig("kubernetes","deployments","#{auth_service_array_index}".to_i,"service","replicas")
  service_admin_user = readDataYaml.dig("kubernetes","deployments","#{auth_service_array_index}".to_i,"service","admin_user")
  service_admin_password = readDataYaml.dig("kubernetes","deployments","#{auth_service_array_index}".to_i,"service","admin_password")

  if readDataYaml.dig("kubernetes","deployments","#{auth_service_array_index}".to_i,"service","namespace")
    service_namespace = readDataYaml.dig("kubernetes","deployments","#{auth_service_array_index}".to_i,"service","namespace")
  end

  if readDataYaml.dig("kubernetes","deployments","#{auth_service_array_index}".to_i,"service","name")
    service_name = readDataYaml.dig("kubernetes","deployments","#{auth_service_array_index}".to_i,"service","name")
  else service_name = 'as-' + service_namespace
  end

  describe 'Checking if auth-service is running' do
    describe command("kubectl get services --namespace=#{service_namespace}") do
      its(:stdout) { should match /#{service_name}/ }
    end
  end

  describe 'Checking if the ports are open' do
    describe port(service_port) do
      let(:disable_sudo) { false }
      it { should be_listening }
    end
  end  

  describe 'Checking the status of auth-service pods - all pods should be running' do
    describe command("kubectl get pods --namespace=#{service_namespace} --field-selector=status.phase=Running | grep #{service_name} | wc -l") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq service_replicas
      end
      its(:exit_status) { should eq 0 }
    end
  end  

  describe 'Checking the auth-service API connection' do
    describe command("curl -o /dev/null -s -w '%{http_code}' -k https://#{host_inventory['hostname']}:#{service_port}/auth/") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq 200
      end
    end
    describe command("curl -k -d \"client_id=admin-cli\" -d \"username=#{service_admin_user}\" -d \"password=#{service_admin_password}\" \
    -d \"grant_type=password\" https://#{host_inventory['hostname']}:#{service_port}/auth/realms/master/protocol/openid-connect/token") do
      its(:stdout) { should_not match /^$/ }
      its(:exit_status) { should eq 0 }
    end
  end
end 

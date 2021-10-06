require 'spec_helper'
require 'securerandom'

def callAuthServiceDeploymentTests

  service_port = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'auth-service'}["service"]["port"]
  service_replicas = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'auth-service'}["service"]["replicas"]
  service_namespace = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'auth-service'}["service"]["namespace"]
  service_name = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'auth-service'}["service"]["name"]
  service_admin_user = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'auth-service'}["service"]["admin_user"]
  service_admin_password = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'auth-service'}["service"]["admin_password"]


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
      its(:stdout) { should match /access_token/ }
      its(:exit_status) { should eq 0 }
    end
  end
end 

require 'spec_helper'

def callPgpoolDeploymentTests

  service_port = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'pgpool'}["service"]["port"]
  service_replicas = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'pgpool'}["replicas"]
  service_namespace = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'pgpool'}["namespace"]
  service_name = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'pgpool'}["service"]["name"]

  describe 'Checking if Pgpool service is running' do
    describe command("kubectl get services --namespace=#{service_namespace}") do
      its(:stdout) { should match /#{service_name}/ }
    end
  end

  describe 'Checking Pgpool service target port' do
    describe command("kubectl describe service #{service_name} --namespace=#{service_namespace} | grep TargetPort") do
      its(:stdout) { should match /#{service_port}/ }
    end
  end

  describe 'Checking the status of Pgpool pods - all pods should be running' do
    describe command("kubectl get pods --namespace=#{service_namespace} --field-selector=status.phase=Running | grep -c #{service_name}") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq service_replicas
      end
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking the total number of database nodes' do
    describe command("kubectl exec --namespace=#{service_namespace} $(kubectl get pods --namespace=#{service_namespace} -o custom-columns=:metadata.name -l app=#{service_name} --no-headers | head -n1) -- bash -c 'pcp_node_count -h localhost -U $PGPOOL_ADMIN_USERNAME -w'") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq countInventoryHosts("postgresql")
      end
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking the information on the given node' do
    countInventoryHosts("postgresql").times do |i|
      describe command("kubectl exec --namespace=#{service_namespace} $(kubectl get pods --namespace=#{service_namespace} -o custom-columns=:metadata.name -l app=#{service_name} --no-headers | head -n1) -- bash -c 'pcp_node_info -h localhost -U $PGPOOL_ADMIN_USERNAME -w --node-id=#{i} --verbose'") do
        its(:stdout) { should match /Status.*: 2/ }
        its(:stdout) { should match /Status Name.*: up/ }
        its(:stdout) { should match /Role.*: (primary|standby.*Replication State.*: streaming)/m }
        its(:exit_status) { should eq 0 }
      end
    end
  end
  
  describe 'Checking load balancing' do
    describe command("kubectl exec --namespace=#{service_namespace} $(kubectl get pods --namespace=#{service_namespace} -o custom-columns=:metadata.name -l app=#{service_name} --no-headers | head -n1) -- bash -c 'export PGPASSWORD=$(cat /opt/bitnami/pgpool/secrets/pgpool_sr_check_password) && psql -qAtX -h localhost -U $PGPOOL_SR_CHECK_USER -d postgres -c \"show pool_nodes\"'") do
      countInventoryHosts("postgresql").times do |i|
        its(:stdout) { should match /^#{i}\|.*\|up\|.*(primary\|([1-9][0-9]*)|standby\|([1-9][0-9]*)\|.*streaming)/ }
        its(:exit_status) { should eq 0 }
      end
    end
  end

end

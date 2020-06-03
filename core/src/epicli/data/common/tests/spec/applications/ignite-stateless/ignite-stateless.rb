require 'spec_helper'

def callIgniteDeploymentTests

  rest_api_host = '127.0.0.1'
  cacheName = 'epi-test-k8s'
  service_namespace = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'ignite-stateless'}["namespace"]
  service_replicas = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'ignite-stateless'}["replicas"]
  rest_nodeport = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'ignite-stateless'}["service"]["rest_nodeport"]
  sql_nodeport = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'ignite-stateless'}["service"]["sql_nodeport"]
  thinclients_nodeport = readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'ignite-stateless'}["service"]["thinclients_nodeport"]

  describe 'Checking if th Ignite service exists' do
    describe command("kubectl get services --namespace=#{service_namespace} --no-headers -o custom-columns=:metadata.name") do
      its(:stdout) { should match /ignite/ }
    end
  end

  describe 'Checking if the ports are open' do
    let(:disable_sudo) { false }
    describe port(rest_nodeport) do
      it { should be_listening }
    end
    describe port(sql_nodeport) do
      it { should be_listening }
    end
    describe port(thinclients_nodeport) do
      it { should be_listening }            
    end
  end  

  describe 'Checking the status of Ignite pods - all pods should be running' do
    describe command("kubectl get pods --namespace=#{service_namespace} --field-selector=status.phase=Running --no-headers | wc -l") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq service_replicas
      end
      its(:exit_status) { should eq 0 }
    end
  end  
  
  describe 'Checking API connection' do
    describe command("curl 'http://#{rest_api_host}:#{rest_nodeport}/ignite?cmd=version'") do
      its(:stdout_as_json) { should include('successStatus' => 0) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to create a cache' do
    describe command("curl 'http://#{rest_api_host}:#{rest_nodeport}/ignite?cmd=getorcreate&cacheName=#{cacheName}'") do
      its(:stdout_as_json) { should include('successStatus' => 0) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to add key-value pairs to cache' do
    describe command("curl 'http://#{rest_api_host}:#{rest_nodeport}/ignite?cmd=putall&k1=testKey1&k2=testKey2&k3=testKey3&v1=testValue1&v2=testValue2&v3=testValue3&cacheName=#{cacheName}'") do
      its(:stdout_as_json) { should include('successStatus' => 0) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to get values mapped to the specified keys from cache' do
    describe command("curl 'http://#{rest_api_host}:#{rest_nodeport}/ignite?cmd=getall&k1=testKey1&k2=testKey2&k3=testKey3&cacheName=#{cacheName}'") do
      its(:stdout_as_json) { should include('response' => include('testKey1' => 'testValue1')) }
      its(:stdout_as_json) { should include('response' => include('testKey2' => 'testValue2')) }
      its(:stdout_as_json) { should include('response' => include('testKey3' => 'testValue3')) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to get the number of all entries cached across all nodes' do
    describe command("curl 'http://#{rest_api_host}:#{rest_nodeport}/ignite?cmd=size&cacheName=#{cacheName}'") do
      its(:stdout_as_json) { should include('response' => 3) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to create a test table via API' do
    describe command("curl 'http://#{rest_api_host}:#{rest_nodeport}/ignite?cmd=qryfldexe&pageSize=10&cacheName=#{cacheName}&qry=CREATE+TABLE+PUBLIC.EPI_TEST_TABLE(id+int,+name+varchar,+PRIMARY+KEY+(id))+WITH+\"CACHE_NAME=#{cacheName}-ddl\"'") do
      its(:stdout_as_json) { should include('successStatus' => 0) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to insert values into the test table via API' do
    describe command("curl 'http://#{rest_api_host}:#{rest_nodeport}/ignite?cmd=qryfldexe&pageSize=10&cacheName=#{cacheName}&qry=INSERT+INTO+PUBLIC.EPI_TEST_TABLE(id,+name)+values+(1,+%27SUCCESS%27)'") do
      its(:stdout_as_json) { should include('successStatus' => 0) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to select values from the test table via API' do
    describe command("curl 'http://#{rest_api_host}:#{rest_nodeport}/ignite?cmd=qryfldexe&pageSize=10&cacheName=#{cacheName}&qry=SELECT+NAME+FROM+PUBLIC.EPI_TEST_TABLE' | jq '.response.items'") do
      its(:stdout) { should match /\bSUCCESS\b/ }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to select values from the test table using JDBC connection inside pods' do
    describe command("for pod in $(kubectl get pods --namespace=#{service_namespace} --no-headers --field-selector=status.phase=Running -o custom-columns=':metadata.name'); do kubectl exec $pod -n=ignite -- bash -c \"echo 'SELECT name FROM EPI_TEST_TABLE;' | /opt/ignite/apache-ignite-fabric/bin/sqlline.sh -u jdbc:ignite:thin://127.0.0.1/ 2>&1\"; done") do
    its(:stdout) { should match /(.*1 row selected.*){#{service_replicas}}/m }
    its(:stdout) { should match /(.*SUCCESS.*){#{service_replicas}}/m }
    its(:stdout) { should_not match /Error/ }    
    its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to drop the test table via API' do
    describe command("curl 'http://#{rest_api_host}:#{rest_nodeport}/ignite?cmd=qryfldexe&pageSize=10&cacheName=#{cacheName}&qry=DROP+TABLE+IF+EXISTS+PUBLIC.EPI_TEST_TABLE'") do
      its(:stdout_as_json) { should include('successStatus' => 0) }
      its(:exit_status) { should eq 0 }
    end
  end

  describe 'Checking if it is possible to destroy a cache' do
    describe command("curl 'http://#{rest_api_host}:#{rest_nodeport}/ignite?cmd=destcache&cacheName=#{cacheName}'") do
      its(:stdout_as_json) { should include('successStatus' => 0) }
      its(:exit_status) { should eq 0 }
    end
  end

end

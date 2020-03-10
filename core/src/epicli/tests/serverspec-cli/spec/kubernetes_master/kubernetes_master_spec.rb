require 'spec_helper'
require 'base64'

kube_apiserver_secure_port = 6443

describe 'Waiting for all pods to be ready' do
  describe command("for i in {1..1200}; do if [ $(kubectl get pods --all-namespaces -o json  | jq -r '.items[] | select(.status.phase != \"Running\" or ([ .status.conditions[] | select(.type == \"Ready\" and .status != \"True\") ] | length ) == 1 ) | .metadata.namespace + \"/\" + .metadata.name' | wc -l) -eq 0 ]; \
  then echo 'READY'; break; else echo 'WAITING'; sleep 1; fi; done") do
    its(:stdout) { should match /READY/ }
    its(:exit_status) { should eq 0 }
  end
end 

describe 'Checking if kubelet service is running' do
  describe service('kubelet') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if kube-scheduler is running' do
  describe process('kube-scheduler') do
    it { should be_running }
  end
end

describe 'Checking if kube-controller is running' do
  describe process('kube-controller') do
    it { should be_running }
  end
end

describe 'Checking if kube-apiserver is running' do
  describe process("kube-apiserver") do
    it { should be_running }
  end
end

describe 'Checking if there are any pods that have status other than Running' do
  describe command('kubectl get pods --all-namespaces --field-selector=status.phase!=Running') do
    its(:stdout) { should match /^$/ }
    its(:stderr) { should match /No resources found./ }
  end
end  

describe 'Checking if the number of master nodes is the same as indicated in the inventory file' do
  describe command('kubectl get nodes --selector=node-role.kubernetes.io/master --no-headers | wc -l | tr -d "\n"') do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq countInventoryHosts("kubernetes_master")
      end
  end
end

describe 'Checking if the number of worker nodes is the same as indicated in the inventory file' do
  describe command('kubectl get nodes --no-headers | grep -v master | wc -l | tr -d "\n"') do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq countInventoryHosts("kubernetes_node")
      end
  end
end

describe 'Checking if there are any nodes that have status other than Ready' do
  describe command('kubectl get nodes') do
    its(:stdout) { should match /\bReady\b/ }
    its(:stdout) { should_not match /NotReady/ }
    its(:stdout) { should_not match /Unknown/ }
    its(:stdout) { should_not match /SchedulingDisabled/ }
  end
end  

describe 'Checking if the number of all nodes is the same as the number of Ready nodes' do
  describe command('out1=$(kubectl get nodes --no-headers | wc -l); out2=$(kubectl get nodes --no-headers | grep -wc Ready); if [ "$out1" = "$out2" ]; then echo "EQUAL"; else echo "NOT EQUAL"; fi') do
    its(:stdout) { should match /\bEQUAL\b/ }
    its(:stdout) { should_not match /NOT EQUAL/ }
  end
end  

describe 'Checking the port on which to serve HTTPS with authentication and authorization' do
  describe port(kube_apiserver_secure_port) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end  

describe 'Checking secret creation using kubectl' do

  test_user = 'user123'
  test_pass = 'pass456'
  test_user_b64 = Base64.encode64(test_user)
  test_pass_b64 = Base64.encode64(test_pass)
  timestamp = DateTime.now.to_time.to_i.to_s
  test_secret = 'testsecret' + timestamp

  describe 'Checking if the secret was successfully created' do
    describe command("kubectl create secret generic #{test_secret} --from-literal=username=#{test_user} --from-literal=password=#{test_pass}") do
      its(:stdout) { should match /secret\/#{test_secret} created/ }
    end
  end
  describe 'Checking if the created secret is present on the list with all secrets' do
    describe command('kubectl get secrets') do
      its(:stdout) { should match /#{test_secret}/ }
    end
  end
  describe 'Checking if the secret stores encoded data' do
    describe command("kubectl get secret #{test_secret} -o yaml") do
      its(:stdout) { should match /name: #{test_secret}/ }
      its(:stdout) { should match /#{test_user_b64}/ }
      its(:stdout) { should match /#{test_pass_b64}/ }
    end
  end
  describe 'Deleting created secret' do
    describe command("kubectl delete secret #{test_secret}") do
      its(:stdout) { should match /secret "#{test_secret}" deleted/ }
      its(:exit_status) { should eq 0 }
    end
  end
end  

describe 'Checking kubernetes dashboard availability' do
  describe 'Checking if kubernetes-dashboard pod is running' do
    describe command('kubectl get pods --all-namespaces | grep kubernetes-dashboard') do
        its(:stdout) { should match /kubernetes-dashboard/ }
        its(:stdout) { should match /Running/ }
        its(:exit_status) { should eq 0 }
    end
  end
  describe 'Checking if kubernetes-dashboard is deployed' do
    describe command('kubectl get deployments --all-namespaces --field-selector metadata.name=kubernetes-dashboard') do
      its(:stdout) { should match /kubernetes-dashboard/ }
      its(:stdout) { should match /1\/1/ }
      its(:exit_status) { should eq 0 }
    end
  end
  describe 'Checking if admin token bearer exists' do
    describe command("kubectl describe secret $(kubectl get secrets --namespace=kube-system | grep admin-user \
    | awk '{print $1}') --namespace=kube-system | awk '/^token/ {print $2}' | head -1") do
      its(:stdout) { should_not match /^$/ }
      its(:exit_status) { should eq 0 }
    end
  end
  describe 'Setting up proxy and starting to serve on localhost' do
    describe command('kubectl proxy >/dev/null 2>&1 &') do
      its(:exit_status) { should eq 0 }
    end
  end
  describe 'Checking if the dashboard is available' do
    describe command('for i in {1..60}; do if [ $(curl -o /dev/null -s -w "%{http_code}" "http://localhost:8001/api/v1/namespaces/$(kubectl get deployments --all-namespaces --field-selector metadata.name=kubernetes-dashboard --no-headers | awk \'{print $1}\')/services/https:kubernetes-dashboard:/proxy/") -eq 200 ]; \
    then echo -n "200"; break; else sleep 1; fi; done') do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq 200
      end
    end
  end
  describe 'Terminating kubectl proxy process' do
    describe command('pkill -f "kubectl proxy"') do
      its(:exit_status) { should eq 0 }
    end
  end
end

describe 'Checking if coredns is deployed' do
  describe command('kubectl get deployments --all-namespaces --field-selector metadata.name=coredns') do
    coredns_counter = 2 # always equal 2
    its(:stdout) { should match /coredns/ }
    its(:stdout) { should match /#{coredns_counter}\/#{coredns_counter}/ }
    its(:exit_status) { should eq 0 }
  end
end

describe 'Checking if kubernetes healthz endpoint is responding' do
  describe command('curl --insecure -o /dev/null -s  -w "%{http_code}" "https://127.0.0.1:10250/healthz"') do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq 401
    end
  end
end

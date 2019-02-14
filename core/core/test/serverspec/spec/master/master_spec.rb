require 'spec_helper'
require 'base64'


describe 'Check if kubelet service is up' do
  describe service('kubelet') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Check if kube-scheduler is up' do
  describe process('kube-scheduler') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Check if kube-scheduler is up - 2nd test' do
  describe command('ps -C kube-scheduler --no-headers') do
    its(:stdout) { should match /kube-scheduler/ }
    its(:exit_status) { should eq 0 }
  end
end

describe 'Check if kube-controller is up' do
  describe process('kube-controller') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Check if kube-controller is up - 2nd test' do
  describe command('ps -C kube-controller --no-headers') do
    its(:stdout) { should match /kube-controller/ }
    its(:exit_status) { should eq 0 }
  end
end

describe 'Check if kube-apiserver is up' do
  describe process("kube-apiserver") do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Check if kube-apiserver is up - 2nd test' do
  describe command('ps -C kube-apiserver --no-headers') do
    its(:stdout) { should match /kube-apiserver/ }
    its(:exit_status) { should eq 0 }
  end
end

describe 'Check if there are any pods that have status other than Running' do
  describe command('kubectl get pods --all-namespaces --field-selector=status.phase!=Running') do
    its(:stdout) { should match /^$/ }
    its(:stderr) { should match /No resources found./ }
  end
end  

describe 'Check if the number of master nodes is the same as indicated in the inventory file' do
  describe command('kubectl get nodes --selector=node-role.kubernetes.io/master --no-headers | wc -l | tr -d "\n"') do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq count_inventory_roles("master")
      end
  end
end

describe 'Check if the number of worker nodes is the same as indicated in the inventory file' do
  describe command('kubectl get nodes --no-headers | grep -v master | wc -l | tr -d "\n"') do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq count_inventory_roles("worker")
      end
  end
end

describe 'Check if there are any nodes that have status other than Ready' do
  describe command('kubectl get nodes') do
    its(:stdout) { should match /Ready/ }
    its(:stdout) { should_not match /NotReady/ }
    its(:stdout) { should_not match /Unknown/ }
    its(:stdout) { should_not match /False/ }
  end
end  

describe 'Check the port on which to serve HTTPS with authentication and authorization' do
  describe port(6443) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end  

describe 'Creating, checking and decoding a secret using kubectl' do

  test_user = 'user123'
  test_pass = 'pass456'
  test_user_b64 = Base64.encode64(test_user)
  test_pass_b64 = Base64.encode64(test_pass)
  timestamp = DateTime.now.to_time.to_i.to_s
  test_secret = 'testsecret' + timestamp

  describe 'Creating a secret...' do
    describe command("kubectl create secret generic #{test_secret} --from-literal=username=#{test_user} --from-literal=password=#{test_pass}") do
      its(:stdout) { should match /secret\/#{test_secret} created/ }
    end
  end
  describe 'Checking if it exists...' do
    describe command('kubectl get secrets') do
      its(:stdout) { should match /#{test_secret}/ }
    end
  end
  describe 'Decoding...' do
    describe command("kubectl get secret #{test_secret} -o yaml") do
      its(:stdout) { should match /name: #{test_secret}/ }
      its(:stdout) { should match /#{test_user_b64}/ }
      its(:stdout) { should match /#{test_pass_b64}/ }
    end
  end
end  

describe 'Testing kubernetes dashboard...' do
  describe 'Looking for kubernetes-dashboard pod' do
    describe command('kubectl get pods --all-namespaces | grep kubernetes-dashboard') do
        its(:stdout) { should match /kubernetes-dashboard/ }
        its(:stdout) { should match /Running/ }
        its(:exit_status) { should eq 0 }
    end
  end
  describe 'Checking kubernetes-dashboard deployment status' do
    describe command('kubectl get deployments --all-namespaces --field-selector metadata.name=kubernetes-dashboard') do
      its(:stdout) { should match /kubernetes-dashboard/ }
      its(:stdout) { should match /1\/1/ }
      its(:exit_status) { should eq 0 }
    end
  end
  describe 'Getting admin token bearer' do
    describe command("kubectl describe secret $(kubectl get secrets --namespace=kube-system | grep admin-user \
    | awk '{print $1}') --namespace=kube-system | awk '/^token/ {print $2}' | head -1") do
      its(:stdout) { should_not match /^$/ }
    end
  end
  describe 'Setting up proxy and starting to serve on localhost' do
    describe command('kubectl proxy >/dev/null 2>&1 &') do
      its(:exit_status) { should eq 0 }
    end
  end
  describe 'Checking the dashboard availability' do
    describe command("curl -I 'http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/'") do
      its(:stdout) { should match /HTTP\/1.1 200 OK/ }
    end
  end
  describe 'Terminating kubectl proxy process' do
    describe command('pkill -f "kubectl proxy"') do
      its(:exit_status) { should eq 0 }
    end
  end
end

describe 'Checking coredns deployment status' do
  describe command('kubectl get deployments --all-namespaces --field-selector metadata.name=coredns') do
    coredns_counter = 2 # always equal 2
    its(:stdout) { should match /coredns/ }
    its(:stdout) { should match /#{coredns_counter}\/#{coredns_counter}/ }
    its(:exit_status) { should eq 0 }
  end
end

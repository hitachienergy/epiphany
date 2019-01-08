require 'spec_helper'

describe service('kubelet') do
  it { should be_enabled }
  it { should be_running }
end

describe service('kube-controller') do
    it { should be_enabled }
    it { should be_running }
  end

describe service('kube-apiserver') do
    it { should be_enabled }
    it { should be_running }
  end

describe port(6443) do
    it { should be_listening }
  end

#check if output from "get pods --all-namespaces" has dashboard pod running
describe command('kubectl get pods --all-namespaces | grep dashboard') do
    its(:stdout) { should match /kubernetes-dashboard/ }
    its(:stdout) { should match /running/ }
    its(:exit_status) { should eq 0 }
  end
  

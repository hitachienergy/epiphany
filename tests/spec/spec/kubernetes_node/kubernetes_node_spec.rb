require 'spec_helper'

describe 'Check if containerd service is enabled/running' do
  describe service('containerd') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Check the containerd' do
  describe command('crictl version') do
    let(:disable_sudo) { false }
    its(:stdout) { should include('RuntimeName:  containerd') }
  end
  describe file('/etc/containerd/config.toml') do
    let(:disable_sudo) { false }
    its(:content) { should match(/SystemdCgroup = true/) }
  end
end

describe 'Check the kubelet cgroup driver' do
  describe file('/var/lib/kubelet/config.yaml') do
    let(:disable_sudo) { false }
    its(:content_as_yaml) { should include('cgroupDriver' => 'systemd') }
    its(:content_as_yaml) { should_not include('cgroupDriver' => 'cgroupfs') }
  end
end

describe 'Check certificate rotation for the kubelet' do
  describe file('/var/lib/kubelet/config.yaml') do
    let(:disable_sudo) { false }
    its(:content_as_yaml) { should include('rotateCertificates' => true) }
  end
end

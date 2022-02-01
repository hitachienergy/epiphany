require 'spec_helper'

describe 'Check the containerd' do
  describe command('crictl --runtime-endpoint unix:///run/containerd/containerd.sock version') do
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

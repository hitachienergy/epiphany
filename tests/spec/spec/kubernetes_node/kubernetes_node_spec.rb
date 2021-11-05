require 'spec_helper'

describe 'Check the kubelet cgroup driver' do
  describe file('/var/lib/kubelet/config.yaml') do
    let(:disable_sudo) { false }
    its(:content_as_yaml) { should include('cgroupDriver' => 'systemd') }
    its(:content_as_yaml) { should_not include('cgroupDriver' => 'cgroupfs') }
  end
end

describe 'Check the docker cgroup and logging driver' do
  describe file('/etc/docker/daemon.json') do
    let(:disable_sudo) { false }
    its(:content_as_json) { should include('exec-opts' => include('native.cgroupdriver=systemd')) }
    its(:content_as_json) { should include('log-driver' => 'json-file') }
    its(:content_as_json) { should_not include('exec-opts' => include('native.cgroupdriver=cgroupfs')) }
  end
  describe command('docker info | grep -i driver') do
    let(:disable_sudo) { false }
    its(:stdout) { should match(/Cgroup Driver: systemd/) }
    its(:stdout) { should match(/Logging Driver: json-file/) }
    its(:exit_status) { should eq 0 }
  end
end

describe 'Check certificate rotation for the kubelet' do
  describe file('/var/lib/kubelet/config.yaml') do
    let(:disable_sudo) { false }
    its(:content_as_yaml) { should include('rotateCertificates' => true) }
  end
end

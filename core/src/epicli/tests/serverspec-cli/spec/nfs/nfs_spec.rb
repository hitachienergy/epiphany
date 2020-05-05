require 'spec_helper'

nfs_defs = readDataYaml("configuration/nfs")["specification"]["nfs_defs"]
nfs_default_port = 2049
rpcbind_default_port = 111

if os[:family] == 'redhat'
  describe 'Checking if NFS service is running' do
    describe service('nfs') do
      it { should be_enabled }
      it { should be_running }
    end
    describe service('rpcbind') do
      it { should be_enabled }
      it { should be_running }
    end
  end
elsif os[:family] == 'ubuntu'
  describe 'Checking if NFS service is running' do
    describe service('nfs-kernel-server') do
      it { should be_enabled }
      it { should be_running }
    end
  end
end

describe 'Checking if the ports are open' do
  let(:disable_sudo) { false }
  describe port(nfs_default_port) do
    it { should be_listening }
  end
  describe port(rpcbind_default_port) do
    it { should be_listening }
  end
end  

describe 'Checking NFS export file' do
  describe file('/etc/exports') do
    it { should exist }
    it { should be_a_file }
  end
end

describe 'Checking available NFS mounts' do
  let(:disable_sudo) { false }
  nfs_defs.select {|i|
    describe command("showmount -e localhost | grep #{i['nfs_path'].chomp('/')}") do
      its(:stdout) { should match /^#{i["nfs_path"].chomp("/")}*/}
      its(:exit_status) { should eq 0 }
    end}
end

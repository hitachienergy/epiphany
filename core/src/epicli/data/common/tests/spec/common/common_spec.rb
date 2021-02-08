require 'spec_helper'
require_relative 'common_helpers'

provider = readDataYaml("epiphany-cluster")["provider"]

#=== Test LVM merge (RHEL on Azure) ===

if provider == 'azure' and os[:family] == 'redhat' and lvm_installed?
  describe 'Check LVM logical volumes' do
    let(:disable_sudo) { false }
    describe command("lvs -o lv_name --noheadings") do
      its(:exit_status) { should eq 0 }
      its(:stdout) { should_not match /\bhomelv$/ }
      its(:stdout) { should_not match /\boptlv$/ }
      its(:stdout) { should_not match /\btmplv$/ }
      its(:stdout) { should_not match /\bvarlv$/ }
    end
  end

  # Temporary directory should be cleaned up
  describe 'Check /root/epiphany-lvm-merge directory' do
    let(:disable_sudo) { false }
    describe file('/root/epiphany-lvm-merge') do
      it { should_not exist }
    end
  end

  # crond & kdump services are temporarily masked then started

  describe 'Check crond service' do
    describe service('crond') do
      it { should be_running }
    end
  end

  describe 'Check substate of kdump service' do
    describe command("systemctl show kdump.service -p SubState") do
      its(:exit_status) { should eq 0 }
      its(:stdout) { should contain "SubState=exited" }
    end
  end

  describe 'Check epiphany-lvm-merge service' do
    describe service('epiphany-lvm-merge') do
      it { should_not be_enabled }
    end
  end
end

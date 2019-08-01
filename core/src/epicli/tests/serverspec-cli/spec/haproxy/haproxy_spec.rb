require 'spec_helper'

haproxy_host = 'localhost'
haproxy_front_port = 443

describe 'Checking if HAProxy service is running' do
  describe service('haproxy') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if HAProxy user exists' do
  describe group('haproxy') do
    it { should exist }
  end
  describe user('haproxy') do
    it { should exist }
    it { should belong_to_group 'haproxy' }
    it { should have_home_directory '/var/lib/haproxy' }
    it { should have_login_shell('/usr/sbin/nologin').or have_login_shell('/sbin/nologin') } # HAProxy user shell is located in /sbin/nologin on RedHat
  end
end

describe 'Checking if HAProxy log file exists and is not empty' do
  describe file('/var/log/haproxy.log') do
    let(:disable_sudo) { false }
    it { should exist }
    it { should be_a_file }
    its(:size) { should > 0 }
  end
end

describe 'Checking if the ports are open' do
  describe port(haproxy_front_port) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end 

describe 'Checking SSL certificates' do
  describe file('/etc/ssl/haproxy') do
    it { should exist }
    it { should be_a_directory }
  end
  describe command("ls -1 /etc/ssl/haproxy/*.pem 2>/dev/null | wc -l") do
    it "is expected to be gt 0" do
      expect(subject.stdout.to_i).to be > 0
    end
    its(:exit_status) { should eq 0 }
  end
  describe command("echo 'Q' | openssl s_client -connect #{haproxy_host}:#{haproxy_front_port}") do
    its(:stdout) { should match /^CONNECTED/ }
    its(:exit_status) { should eq 0 }
  end
end

describe 'Checking HAProxy config files' do
  describe file('/etc/haproxy/haproxy.cfg') do
    it { should exist }
    it { should be_a_file }
  end
  describe file('/etc/rsyslog.d/haproxy.conf') do
    it { should exist }
    it { should be_a_file }
  end
  describe file('/etc/logrotate.d/haproxy') do
    it { should exist }
    it { should be_a_file }
  end
end

describe 'Checking HAProxy HTTP status code for stats page' do
  describe command("curl -k --user $(cat /etc/haproxy/haproxy.cfg | grep 'stats auth' | awk '{print $3}') -o /dev/null -s -w '%{http_code}' \
  https://#{haproxy_host}:#{haproxy_front_port}$(cat /etc/haproxy/haproxy.cfg | grep 'stats uri' | awk '{print $3}')") do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq 200
    end
  end
  describe command("curl -k --user $(cat /etc/haproxy/haproxy.cfg | grep 'stats auth' | awk '{print $3}') \
  https://#{haproxy_host}:#{haproxy_front_port}$(cat /etc/haproxy/haproxy.cfg | grep 'stats uri' | awk '{print $3}')") do
    its(:stdout) { should match /Statistics Report for HAProxy/ }
  end
end


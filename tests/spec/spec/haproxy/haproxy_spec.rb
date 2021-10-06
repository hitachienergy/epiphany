require 'spec_helper'

haproxy_host = 'localhost'
haproxy_front_port = 443
haproxy_stats_port = 9000

# Running systemctl status command as "is-active" returns "unknown" in result 
# https://bugzilla.redhat.com/show_bug.cgi?id=1073481

describe 'Checking HAProxy service status' do
  describe command("systemctl status haproxy > /dev/null") do
    its(:exit_status) { should eq 0 }
  end
end

describe 'Checking if HAProxy service is running' do
  describe service('haproxy') do
    it { should be_enabled }
    it { should be_running }
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
  let(:disable_sudo) { false }
  describe port(haproxy_front_port) do
    it { should be_listening }
  end
  describe port(haproxy_stats_port) do
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
  describe command("curl -k --user $(awk '/stats auth/ {print $3}' /etc/haproxy/haproxy.cfg) -o /dev/null -s -w '%{http_code}' \
  http://#{haproxy_host}:#{haproxy_stats_port}$(awk '/stats uri/ {print $3}' /etc/haproxy/haproxy.cfg)") do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq 200
    end
  end
  describe command("curl -k --user $(awk '/stats auth/ {print $3}' /etc/haproxy/haproxy.cfg) \
  http://#{haproxy_host}:#{haproxy_stats_port}$(awk '/stats uri/ {print $3}' /etc/haproxy/haproxy.cfg)") do
    its(:stdout) { should match /Statistics Report for HAProxy/ }
  end
end


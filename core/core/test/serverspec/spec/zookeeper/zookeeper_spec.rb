require 'spec_helper'

describe service('zookeeper') do
  it { should be_enabled }
  it { should be_running }
end

describe port(2181) do
  it { should be_listening }
end

describe port(7072) do
  it { should be_listening }
end

describe user('zookeeper') do
  it { should exist }
  it { should have_login_shell '/sbin/nologin' }
  it { should belong_to_group 'zookeeper' }
  it { should belong_to_group 'jmx-exporter' }
end

#check if output from jmx exporter is correct
#describe command('curl -s localhost:7072 | grep zookeeper') do
#  its(:stdout) { should match /zookeeper_/ }
#  its(:exit_status) { should eq 0 }
#end

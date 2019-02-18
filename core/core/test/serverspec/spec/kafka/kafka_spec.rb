require 'spec_helper'


describe service('kafka') do
  it { should be_enabled }
  it { should be_running }
end

describe port(9092) do
  it { should be_listening }
end

describe port(7071) do
  it { should be_listening }
end

describe user('kafka') do
  it { should exist }
  it { should have_login_shell '/usr/sbin/nologin' }
  it { should belong_to_group 'kafka' }
  it { should belong_to_group 'jmx-exporter' }
end

#check if output from jmx exporter is correct
describe command('curl -s localhost:7071 | grep kafka') do
  its(:stdout) { should match /kafka_/ }
  its(:exit_status) { should eq 0 }
end

require 'spec_helper'

describe service('prometheus-node-exporter') do
  it { should be_enabled }
  it { should be_running }
end

describe port(9100) do
  it { should be_listening }
end

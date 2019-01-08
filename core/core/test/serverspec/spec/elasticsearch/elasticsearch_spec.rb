require 'spec_helper'

describe service('elsaticsearch') do
  it { should be_enabled }
  it { should be_running }
end

describe service('kibana') do
    it { should be_enabled }
    it { should be_running }
  end

describe service('filebeat') do
    it { should be_enabled }
    it { should be_running }
  end


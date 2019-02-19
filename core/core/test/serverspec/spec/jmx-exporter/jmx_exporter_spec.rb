require 'spec_helper'

describe user('jmx-exporter') do
  it { should exist }
  it { should have_login_shell '/usr/sbin/nologin' }
end

describe group('jmx-exporter') do
  it { should exist }
end

describe file('/opt/jmx-exporter') do
  it { should exist }
  it { should be_grouped_into 'jmx-exporter' }
end

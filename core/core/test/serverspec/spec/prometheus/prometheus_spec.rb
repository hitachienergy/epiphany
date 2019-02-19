require 'spec_helper'

describe port(9090) do
  it { should be_listening }
end

describe group('prometheus') do
  it { should exist }
end

describe user('prometheus') do
  it { should exist }
  it { should have_login_shell '/usr/sbin/nologin' }
  it { should belong_to_group 'prometheus' }
end

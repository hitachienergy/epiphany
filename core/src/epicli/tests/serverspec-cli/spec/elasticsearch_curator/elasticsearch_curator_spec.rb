require 'spec_helper'

describe 'Checking if Elasticsearch Curator package is installed' do
  describe package('elasticsearch-curator') do
    it { should be_installed }
  end
end

describe 'Checking if cron job to delete old elasticsearch indices exists' do
  let(:disable_sudo) { false }
  describe command("crontab -l | grep -q 'Delete old elasticsearch indices.' && echo 'EXISTS' || echo 'NOTEXISTS'") do
    its(:stdout) { should match /\bEXISTS\b/ }
    its(:stdout) { should_not match /\bNOTEXISTS\b/ }
  end
end

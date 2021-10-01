require 'spec_helper'

cron_jobs_list = readDataYaml("configuration/elasticsearch-curator")["specification"]["delete_indices_cron_jobs"]

describe 'Checking if Elasticsearch Curator package is installed' do
  describe package('elasticsearch-curator') do
    it { should be_installed }
  end
end

describe 'Checking if the number of cron jobs on the system is the same as defined in the configuration file' do
  let(:disable_sudo) { false }
  describe command("crontab -l | grep -c 'curator_cli'") do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq cron_jobs_list.length
    end
    its(:exit_status) { should eq 0 }
  end
end

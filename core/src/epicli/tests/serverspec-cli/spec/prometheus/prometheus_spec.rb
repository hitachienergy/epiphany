require 'spec_helper'

prometheus_host = 'localhost'
prometheus_port = 9090
kube_apiserver_secure_port = 6443
alertmanager_host = 'localhost'
alertmanager_port = 9093

describe 'Checking if Prometheus user exists' do
  describe group('prometheus') do
    it { should exist }
  end
  describe user('prometheus') do
    it { should exist }
    it { should belong_to_group 'prometheus' }
    it { should have_login_shell '/usr/sbin/nologin' }
  end
end

describe 'Checking Prometheus directories and files' do
  let(:disable_sudo) { false }
  describe file('/var/lib/prometheus') do
    it { should exist }
    it { should be_a_directory }
    it { should be_owned_by 'prometheus' }
    it { should be_grouped_into 'prometheus' }
  end
  describe file('/etc/prometheus') do
    it { should exist }
    it { should be_a_directory }
    it { should be_owned_by 'root' }
    it { should be_grouped_into 'prometheus' }
  end
  describe file("/etc/prometheus/prometheus.yml") do
    it { should exist }
    it { should be_a_file }
    it { should be_readable }
  end
end

describe 'Checking if Prometheus service is running' do
  describe service('prometheus') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if the ports are open' do
  describe port(prometheus_port) do
    let(:disable_sudo) { false }
    it { should be_listening }
  end
end 

describe 'Checking Prometheus health' do
  describe command("curl -o /dev/null -s -w '%{http_code}' #{prometheus_host}:#{prometheus_port}/graph") do
    it "is expected to be equal" do
      expect(subject.stdout.to_i).to eq 200
    end
  end
  describe command("curl #{prometheus_host}:#{prometheus_port}/-/ready") do
    its(:stdout) { should match /^Prometheus is Ready.$/ }
  end
  describe command("curl #{prometheus_host}:#{prometheus_port}/-/healthy") do
    its(:stdout) { should match /^Prometheus is Healthy.$/ }
  end
end

describe 'Checking if Prometheus is serving metrics about itself' do
    describe command("curl -o /dev/null -s -w '%{http_code}' #{prometheus_host}:#{prometheus_port}/metrics") do
      it "is expected to be equal" do
        expect(subject.stdout.to_i).to eq 200
      end
    end
    describe command("curl #{prometheus_host}:#{prometheus_port}/metrics") do
      its(:stdout) { should_not match /^$/ }
    end
  end


describe 'Checking configuration files for Node exporter' do
    listInventoryHosts("node_exporter").each do |val|
        describe command("ls /etc/prometheus/file_sd") do
        let(:disable_sudo) { false }
        its(:stdout) { should match /node-#{val}.yml/ }
        end
    end
end 

describe 'Checking connection to Node Exporter hosts' do
    listInventoryHosts("node_exporter").each do |val|
        let(:disable_sudo) { false }
        describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP \"(?<=targets: \\\[\').*(?=\'\\\])\" /etc/prometheus/file_sd/node-#{val}.yml)/metrics") do
          it "is expected to be equal" do
            expect(subject.stdout.to_i).to eq 200
          end
        end
    end
end 

describe 'Checking configuration files for HAProxy Exporter' do
    listInventoryHosts("haproxy_exporter").each do |val|
        describe command("ls /etc/prometheus/file_sd") do
        let(:disable_sudo) { false }
        its(:stdout) { should match /haproxy-#{val}.yml/ }
        end
    end
end 

describe 'Checking connection to HAProxy Exporter hosts' do
    listInventoryHosts("haproxy_exporter").each do |val|
        let(:disable_sudo) { false }
        describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP \"(?<=targets: \\\[\\\").*(?=\\\"\\\])\" /etc/prometheus/file_sd/haproxy-#{val}.yml)/metrics") do
          it "is expected to be equal" do
            expect(subject.stdout.to_i).to eq 200
          end
        end
    end
end 

describe 'Checking configuration files for JMX Exporter' do
    listInventoryHosts("jmx_exporter").each do |val|
        describe command("ls /etc/prometheus/file_sd") do
        let(:disable_sudo) { false }
        its(:stdout) { should match /kafka-jmx-#{val}.yml/ }
        its(:stdout) { should match /zookeeper-jmx-#{val}.yml/ }
        end
    end
end 

describe 'Checking connection to JMX Exporter hosts' do
    listInventoryHosts("jmx_exporter").each do |val|
        let(:disable_sudo) { false }
        describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP \"(?<=targets: \\\[\').*(?=\'\\\])\" /etc/prometheus/file_sd/kafka-jmx-#{val}.yml)/metrics") do
          it "is expected to be equal" do
            expect(subject.stdout.to_i).to eq 200
          end
        end
        describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP \"(?<=targets: \\\[\').*(?=\'\\\])\" /etc/prometheus/file_sd/zookeeper-jmx-#{val}.yml)/metrics") do
        it "is expected to be equal" do
          expect(subject.stdout.to_i).to eq 200
        end
      end
    end
end 

describe 'Checking configuration files for Kafka Exporter hosts' do
    listInventoryHosts("kafka_exporter").each do |val|
        describe command("ls /etc/prometheus/file_sd") do
        let(:disable_sudo) { false }
        its(:stdout) { should match /kafka-exporter-#{val}.yml/ }
        end
    end
end 

describe 'Checking connection to Kafka Exporter hosts' do
    listInventoryHosts("kafka_exporter").each do |val|
        let(:disable_sudo) { false }
        describe command("curl -o /dev/null -s -w '%{http_code}' $(grep -oP \"(?<=targets: \\\[\').*(?=\'\\\])\" /etc/prometheus/file_sd/kafka-exporter-#{val}.yml)/metrics") do
          it "is expected to be equal" do
            expect(subject.stdout.to_i).to eq 200
          end
        end
    end
end 

describe 'Checking connection to Kubernetes API server' do
    listInventoryHosts("kubernetes_master").each do |val|
        let(:disable_sudo) { false }
        describe command("curl -o /dev/null -s -w '%{http_code}' -k -H \"Authorization: Bearer $(grep -A 3 kubernetes-apiservers /etc/prometheus/prometheus.yml \
        | awk '/bearer_token/ {print $2}')\" https://#{val}:#{kube_apiserver_secure_port}/metrics") do
          it "is expected to be equal" do
            expect(subject.stdout.to_i).to eq 200
          end
        end
    end
end 

describe 'Checking connection to Kubernetes cAdvisor' do
    let(:disable_sudo) { false }
    listInventoryHosts("kubernetes_master").each do |val_m|
        describe command("curl -o /dev/null -s -w '%{http_code}' -k -H \"Authorization: Bearer $(grep -A 3 kubernetes-cadvisor /etc/prometheus/prometheus.yml \
        | awk '/bearer_token/ {print $2}')\" https://#{val_m}:#{kube_apiserver_secure_port}/api/v1/nodes/#{val_m}/proxy/metrics/cadvisor") do
            it "is expected to be equal" do
                expect(subject.stdout.to_i).to eq 200
            end
        end
        listInventoryHosts("kubernetes_node").each do |val_w|
            describe command("curl -o /dev/null -s -w '%{http_code}' -k -H \"Authorization: Bearer $(grep -A 3 kubernetes-cadvisor /etc/prometheus/prometheus.yml \
            | awk '/bearer_token/ {print $2}')\" https://#{val_m}:#{kube_apiserver_secure_port}/api/v1/nodes/#{val_w}/proxy/metrics/cadvisor") do
                it "is expected to be equal" do
                    expect(subject.stdout.to_i).to eq 200
                end
            end
        end
    end 
end

describe 'Checking connection to Kubernetes nodes' do
    let(:disable_sudo) { false }
    listInventoryHosts("kubernetes_master").each do |val_m|
        describe command("curl -o /dev/null -s -w '%{http_code}' -k -H \"Authorization: Bearer $(grep -A 3 kubernetes-nodes /etc/prometheus/prometheus.yml \
        | awk '/bearer_token/ {print $2}')\" https://#{val_m}:#{kube_apiserver_secure_port}/api/v1/nodes/#{val_m}/proxy/metrics") do
            it "is expected to be equal" do
                expect(subject.stdout.to_i).to eq 200
            end
        end
        listInventoryHosts("kubernetes_node").each do |val_w|
            describe command("curl -o /dev/null -s -w '%{http_code}' -k -H \"Authorization: Bearer $(grep -A 3 kubernetes-nodes /etc/prometheus/prometheus.yml \
            | awk '/bearer_token/ {print $2}')\" https://#{val_m}:#{kube_apiserver_secure_port}/api/v1/nodes/#{val_w}/proxy/metrics") do
                it "is expected to be equal" do
                    expect(subject.stdout.to_i).to eq 200
                end
            end
        end
    end 
end


# # Tests for Alertmanager assuming monitoring.alerts.enable == true

# if readDataYaml["monitoring"]["alerts"]["enable"] == true

#   describe 'Checking Alertmanager directories and files' do
#     let(:disable_sudo) { false }
#     describe file('/var/lib/prometheus/alertmanager') do
#       it { should exist }
#       it { should be_a_directory }
#       it { should be_owned_by 'prometheus' }
#       it { should be_grouped_into 'prometheus' }
#     end
#     describe file('/etc/prometheus/rules') do
#         it { should exist }
#         it { should be_a_directory }
#         it { should be_owned_by 'root' }
#         it { should be_grouped_into 'prometheus' }
#       end
#     describe file("/etc/prometheus/alertmanager.yml") do
#       it { should exist }
#       it { should be_a_file }
#       it { should be_readable }
#     end
#   end

#   describe 'Checking if Alertmanager service is enabled' do
#     describe service('alertmanager') do
#       it { should be_enabled }
#     end
#   end

#   describe 'Validating Alertmanager rules' do
#       describe command("/usr/local/bin/promtool check rules /etc/prometheus/rules/*") do
#         let(:disable_sudo) { false }
#         its(:stdout) { should_not match /FAILED/ }
#         its(:exit_status) { should eq 0 }
#       end
#     end 

#   describe 'Checking if it is possible to create a rule checking if node is up' do
#     describe command("cp -p /etc/prometheus/rules/UpDown.rules /etc/prometheus/rules/TEST_RULE.rules && sed -i 's/UpDown/TEST_RULE/g; s/down/up/g; s/== 0/== 1/g; \
#     s/10s/1s/g' /etc/prometheus/rules/TEST_RULE.rules && systemctl restart prometheus") do
#         let(:disable_sudo) { false }
#         its(:exit_status) { should eq 0 }
#     end
#     describe command("for i in {1..10}; do if [ $(curl -o /dev/null -s -w '%{http_code}' #{prometheus_host}:#{prometheus_port}/graph) == 200 ]; \
#     then curl -s #{prometheus_host}:#{prometheus_port}/rules | grep 'TEST_RULE'; break; else echo 'WAITING FOR PROMETHEUS TO BE STARTED'; sleep 1; fi; done;") do
#       its(:stdout) { should match /TEST_RULE/ }
#       its(:exit_status) { should eq 0 }
#     end
#     describe command("rm -rf /etc/prometheus/rules/TEST_RULE.rules && systemctl restart prometheus") do
#         let(:disable_sudo) { false }
#         its(:exit_status) { should eq 0 }
#     end
#     describe command("for i in {1..10}; do if [ $(curl -o /dev/null -s -w '%{http_code}' #{prometheus_host}:#{prometheus_port}/graph) == 200 ]; \
#     then echo 'PROMETHEUS READY'; break; else echo 'WAITING FOR PROMETHEUS TO BE STARTED'; sleep 1; fi; done;") do
#       its(:stdout) { should match /READY/ }
#       its(:exit_status) { should eq 0 }
#     end
#   end 
  
#   # Tests for Alertmanager assuming monitoring.alerts.enable == true and monitoring.alerts.handlers.mail.enable == true

#   if readDataYaml["monitoring"]["alerts"]["handlers"]["mail"]["enable"] == true

#     describe 'Checking if the ports are open' do
#       describe port(alertmanager_port) do
#         let(:disable_sudo) { false }
#         it { should be_listening }
#       end
#     end 

#     describe 'Checking if Alertmanager service is running' do
#       describe service('alertmanager') do
#         it { should be_running }
#       end
#     end

#     describe 'Checking Alertmanager health' do
#       describe command("curl -o /dev/null -s -w '%{http_code}' #{alertmanager_host}:#{alertmanager_port}") do
#         it "is expected to be equal" do
#           expect(subject.stdout.to_i).to eq 200
#         end
#       end
#       describe command("curl #{alertmanager_host}:#{alertmanager_port}/-/ready") do
#         its(:stdout) { should match /^OK$/ }
#       end
#       describe command("curl #{alertmanager_host}:#{alertmanager_port}/-/healthy") do
#         its(:stdout) { should match /^OK$/ }
#       end
#       describe command("curl #{prometheus_host}:#{prometheus_port}/api/v1/alertmanagers") do
#         its(:stdout_as_json) { should include('status' => 'success') }
#       end
#     end

#     describe 'Checking if it is possible to send an alert' do
#       describe command("curl -XPOST -d '[{\"labels\":{\"alertname\":\"TEST ALERT\", \"severity\":\"critical\"}}]' #{alertmanager_host}:#{alertmanager_port}/api/v1/alerts") do
#         its(:stdout_as_json) { should include('status' => 'success') }
#       end
#     end 

#   end
# end

require 'spec_helper'
require 'securerandom'
require 'applications/rabbitmq/rabbitmq'
require 'applications/auth-service/auth-service'
require 'applications/ignite-stateless/ignite-stateless'

if !readDataYaml("configuration/applications")["specification"]["applications"].select {|i| i["name"] == 'rabbitmq' }.nil?
  callRabbitMQDeploymentTests
end

if !readDataYaml("configuration/applications")["specification"]["applications"].select {|i| i["name"] == 'auth-service' }.nil?
  callAuthServiceDeploymentTests
end

if !readDataYaml("configuration/applications")["specification"]["applications"].select {|i| i["name"] == 'ignite-stateless' }.nil?
  callIgniteDeploymentTests
end

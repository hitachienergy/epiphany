require 'spec_helper'
require 'securerandom'
require 'applications/rabbitmq/rabbitmq'
require 'applications/auth-service/auth-service'
require 'applications/ignite-stateless/ignite-stateless'

if !readDataYaml("configuration/applications")["specification"]["applications"].select {|i| i["name"] == 'rabbitmq' }.empty?
  callRabbitMQDeploymentTests
end

if !readDataYaml("configuration/applications")["specification"]["applications"].select {|i| i["name"] == 'auth-service' }.empty?
  callAuthServiceDeploymentTests
end

if !readDataYaml("configuration/applications")["specification"]["applications"].select {|i| i["name"] == 'ignite-stateless' }.empty?
  callIgniteDeploymentTests
end

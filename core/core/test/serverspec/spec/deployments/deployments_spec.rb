require 'spec_helper'
require 'securerandom'
require 'deployments/rabbitmq/rabbitmq'
require 'deployments/auth-service/auth-service'

if readDataYaml.dig("kubernetes","deployments") && !readDataYaml["kubernetes"]["deployments"].index {|h| h["name"] == "rabbitmq" }.nil?
  callRabbitMQDeploymentTests
end

if readDataYaml.dig("kubernetes","deployments") && !readDataYaml["kubernetes"]["deployments"].index {|h| h["name"] == "auth-service" }.nil?
  callAuthServiceDeploymentTests
end

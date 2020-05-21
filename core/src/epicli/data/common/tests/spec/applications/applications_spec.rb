require 'spec_helper'
require 'securerandom'
require 'applications/rabbitmq/rabbitmq'
require 'applications/auth-service/auth-service'
require 'applications/ignite-stateless/ignite-stateless'
require 'applications/pgpool/pgpool'

if !readDataYaml("configuration/applications")["specification"]["applications"].select {|i| i["name"] == 'rabbitmq'}.empty? &&
  readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'rabbitmq'}["enabled"]

  callRabbitMQDeploymentTests

end

if !readDataYaml("configuration/applications")["specification"]["applications"].select {|i| i["name"] == 'auth-service'}.empty? &&
  readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'auth-service'}["enabled"]

  callAuthServiceDeploymentTests

end

if !readDataYaml("configuration/applications")["specification"]["applications"].select {|i| i["name"] == 'ignite-stateless'}.empty? &&
  readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'ignite-stateless'}["enabled"]

  callIgniteDeploymentTests
  
end

if !readDataYaml("configuration/applications")["specification"]["applications"].select {|i| i["name"] == 'pgpool'}.empty? &&
  readDataYaml("configuration/applications")["specification"]["applications"].detect {|i| i["name"] == 'pgpool'}["enabled"]

  callPgpoolDeploymentTests
  
end
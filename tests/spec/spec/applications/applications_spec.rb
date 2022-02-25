require 'spec_helper'
require 'securerandom'
require 'applications/rabbitmq/rabbitmq'
require 'applications/auth-service/auth-service'
require 'applications/pgpool/pgpool'

if !readDataYaml('configuration/applications')['specification']['applications'].select do |i|
  i['name'] == 'rabbitmq'
end.empty? &&
   readDataYaml('configuration/applications')['specification']['applications'].detect do |i|
     i['name'] == 'rabbitmq'
   end ['enabled']

  callRabbitMQDeploymentTests

end

if !readDataYaml('configuration/applications')['specification']['applications'].select do |i|
  i['name'] == 'auth-service'
end.empty? &&
   readDataYaml('configuration/applications')['specification']['applications'].detect do |i|
     i['name'] == 'auth-service'
   end ['enabled']

  callAuthServiceDeploymentTests

end

if !readDataYaml('configuration/applications')['specification']['applications'].select do |i|
  i['name'] == 'pgpool'
end.empty? &&
   readDataYaml('configuration/applications')['specification']['applications'].detect do |i|
     i['name'] == 'pgpool'
   end ['enabled']

  callPgpoolDeploymentTests

end

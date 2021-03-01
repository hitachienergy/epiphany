require 'net/ssh'

def get_zookeeper_admin_server_port
  default_port = 8080
  config_file = "/opt/zookeeper/conf/zoo.cfg"
  grep_cmd = "sudo -u zookeeper grep -Po '(?<=^admin\\.serverPort=)\\d+' #{config_file}"
  port = ""

  Net::SSH.start(ENV['TARGET_HOST'], ENV['user'], keys: [ENV['keypath']], :keys_only => true) do |ssh|
    ssh.exec!(grep_cmd) do |channel, stream, data|
      port << data if stream == :stdout && /^[0-9]+$/.match(data)
    end
  end

  return port.empty? ? default_port : port.to_i
end

def get_zookeeper_admin_server_port
  default_port = 8080
  config_file = "/opt/zookeeper/conf/zoo.cfg"
  grep_cmd = "sudo -u zookeeper grep -Po '(?<=^admin\\.serverPort=)\\d+' #{config_file}"

  result = Specinfra.backend.run_command(grep_cmd)

  if (result.failure? and !result.stderr.empty?)
    raise(result.stderr)
  end

  if /^[0-9]+$/.match?(result.stdout)
    port = result.stdout.chomp.to_i
  else
    port = default_port
  end

  return port
end

require 'serverspec'
require 'net/ssh'
require 'yaml'

set :backend, :ssh



if ENV['ASK_SUDO_PASSWORD']
  begin
    require 'highline/import'
  rescue LoadError
    fail "highline is not available. Try installing it."
  end
  set :sudo_password, ask("Enter sudo password: ") { |q| q.echo = false }
else
  set :sudo_password, ENV['SUDO_PASSWORD']
end

host = ENV['TARGET_HOST']

options = Net::SSH::Config.for(host)

options[:user] = ENV['user']
options[:keys] = ENV['keypath']

set :host,        options[:host_name] || host
set :ssh_options, options

# Disable sudo
set :disable_sudo, true

# Set shell
set :shell, '/bin/bash'

# Set environment variables
# set :env, :LANG => 'C', :LC_MESSAGES => 'C'

# Set PATH
# set :path, '/sbin:/usr/local/sbin:$PATH'

  def count_inventory_roles(role)
    file = File.open(ENV['inventory'], "rb")
    input = file.read
    file.close
      if input.include? "[#{role}]"
        rows = input.split("[#{role}]")[1].split("[")[0]
        counter = rows.scan(/ansible_host/).count
      else counter = 0
      end
    return counter
  end

  def hostInGroups?(role)
    file = File.open(ENV['inventory'], "rb")
    input = file.read
    file.close
      if input.include? "[#{role}]"
        rows = input.split("[#{role}]")[1].split("[")[0]
        return rows.include? ENV['TARGET_HOST']
      else return false
      end
  end

  def readDataYaml
    path = ENV['inventory'].dup
    path.sub! 'inventory' , 'manifest.yml'
    datayaml = YAML.load_file(path)
    return datayaml
  end

  def listInventoryHosts(role)
    file = File.open(ENV['inventory'], "rb")
    input = file.read
    file.close
    list = []
    if input.include? "[#{role}]"
      rows = input.split("[#{role}]")[1].split("[")[0]
      rows.each_line do |line|
        if line[0] != '#' and line =~ /(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/
          list << line.split.first
        end
      end
    end
    return list
   end


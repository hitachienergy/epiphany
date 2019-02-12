require 'serverspec'
require 'net/ssh'

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


# Set environment variables
# set :env, :LANG => 'C', :LC_MESSAGES => 'C'

# Set PATH
# set :path, '/sbin:/usr/local/sbin:$PATH'

  def count_inventory_roles(role)
    file = File.open(ENV['inventory'], "rb")
    input = file.read
    file.close
      if input.include? "[#{role}]"
        rows = input.split("[#{role}]\n")[1].split("\n\n")[0]
        counter = rows.scan(/ansible_host/).count
      else counter = 0
      end
    return counter
  end

def lvm_installed?
  cmd = 'sudo which lvs'
  result = Specinfra.backend.run_command(cmd)
  if result.success?
    true
  elsif result.stderr.include?('no lvs in ') or result.stderr.empty?
    false
  else
    raise(result.stderr)
  end
end

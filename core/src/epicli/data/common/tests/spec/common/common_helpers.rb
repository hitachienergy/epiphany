def lvm_installed?
  cmd = "sudo which lvs"
  result = Specinfra.backend.run_command(cmd)
  if result.success?
    return true
  else
    if result.stderr.include?("no lvs in ") or result.stderr.empty?
      return false
    else
      raise(result.stderr)
    end
  end
end

def lvm_present?
  cmd = 'sudo which vgs && sudo vgs --noheadings --quiet'
  result = Specinfra.backend.run_command(cmd)
  if result.success?
    result.stdout.split("\n").length > 1  # first row contains output from which
  elsif result.stderr.include?('no vgs in ') || result.stderr.empty?
    false
  else
    raise(result.stderr)
  end
end

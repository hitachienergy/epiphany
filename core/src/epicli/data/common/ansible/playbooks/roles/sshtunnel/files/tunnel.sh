if [ "$1" = "--kill" ]; then
  ps aux | 
  grep -P "(/usr/bin/ssh|/usr/lib/autossh/autossh)\s.*$2" |
  awk '{print $2}' |
  xargs -r kill
else
  $(which autossh) "$@"
fi

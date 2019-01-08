###########################
# Maintained by Ansible
# Located in /etc/profile.d/operations.sh
###########################

# Nice bright command prompt
if [ $(id -u) -eq 0 ]; then
  PS1='\[\e[1;31m\][\u@\h \W]#\[\e[0m\] '
else
  PS1='\[\e[1;31m\][\u@\h \W]$\[\e[0m\] '
fi

# Could put something else here if you want...

# Log all the commands
PROMPT_COMMAND='history -a >(tee -a ~/.bash_history | logger -t "$USER[$$] $SSH_CONNECTION")'

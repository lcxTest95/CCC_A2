export ANSIBLE_HOST_KEY_CHECKING=False
. ./unimelb-comp90024-2020-grp-36-openrc.sh; ansible-playbook --ask-become-pass install-environment.yaml -i inventory/hosts.ini
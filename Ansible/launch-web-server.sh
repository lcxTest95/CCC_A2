#!/bin/bash

. ./unimelb-comp90024-2020-grp-36-openrc.sh; ansible-playbook --ask-become-pass launch-web-server.yaml -i inventory/hosts.ini
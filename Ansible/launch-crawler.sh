#!/bin/bash

. ./unimelb-comp90024-2020-grp-36-openrc.sh; ansible-playbook --ask-become-pass launch-crawler.yaml -i inventory/hosts.ini
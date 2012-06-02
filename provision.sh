#!/bin/bash
sudo aptitude update
sudo aptitude install -y git-core python python-dev python-setuptools
sudo easy_install -U pip
sudo pip install fabric
sudo pip install jinja2
cd /vagrant
eval `ssh-agent`
ssh-add /home/vagrant/.ssh/id_rsa
fab -R vagrant config setup_all -A

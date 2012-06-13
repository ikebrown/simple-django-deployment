#!/bin/bash
sudo crontab -u vagrant -r
sudo cp  /etc/apt/sources.list /etc/apt/sources.list_backup
ubuntu_mirror='http://no.archive.ubuntu.com/ubuntu/'
sudo sed -i "s|http://us.archive.ubuntu.com/ubuntu/|$ubuntu_mirror|" /etc/apt/sources.list
sudo aptitude update
sudo aptitude install -y git-core python python-dev python-setuptools
sudo easy_install -U pip
sudo pip install fabric
sudo pip install jinja2
if [ ! -f /vagrant/identity ]; then
    sudo sed -ibak -e "s/PermitEmptyPasswords\\s*no/PermitEmptyPasswords yes/" /etc/ssh/sshd_config
    sudo restart ssh
    cd /vagrant/ && ssh-keygen -f identity -C 'oneusefabrickey' -N '' -t rsa -q
    cd /vagrant/ && cat identity.pub >> /home/vagrant/.ssh/authorized_keys
    sleep 1
fi
cd /vagrant/salt && fab -H 127.0.01 master:"127.0.0.1",t minion:"127.0.0.1",t -i /vagrant/identity

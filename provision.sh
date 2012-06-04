#!/bin/bash
sudo crontab -u vagrant -r
sudo aptitude update
sudo aptitude install -y git-core python python-dev python-setuptools
sudo easy_install -U pip
sudo pip install fabric
sudo pip install jinja2
if [ ! -f /vagrant/identity ]; then
    sudo sed -ibak -e "s/PermitEmptyPasswords\\s*no/PermitEmptyPasswords yes/" /etc/ssh/sshd_config
    sudo restart ssh
    cd /vagrant/ && ssh-keygen -f identity -C 'Key for fabric' -N '' -t rsa -q
    cd /vagrant/ && cat identity.pub >> /home/vagrant/.ssh/authorized_keys
    sleep 1
fi
cd /vagrant/ && fab -R vagrant config setup_all -i /vagrant/identity -f /vagrant/fabfile.py
touch /vagrant/done
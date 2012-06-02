#!/bin/bash
user=$1
if [ -z "$user" ]
then
    user='vagrant'
fi
sudo mkdir -p /home/$user/.ssh
sudo cp /vagrant/vagrant.ppk /home/$user/.ssh/id_rsa
sudo cp /vagrant/vagrant.pub /home/$user/.ssh/authorized_keys
sudo cp /vagrant/vagrant.pub /home/$user/.ssh/authorized_keys2
sudo chown -R vagrant:vagrant /home/$user/.ssh
sudo chmod 0600 /home/$user/.ssh/id_rsa
sudo sed -i -e "s/PermitEmptyPasswords no/PermitEmptyPasswords yes/" /etc/ssh/sshd_config

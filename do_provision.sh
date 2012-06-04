#!/bin/bash
echo 
echo Vagrant has a bug with provisioning, starting provisioning via crontab.
echo Check output.txt for progress.
echo When done a done file will appear next to output.txt. 

if [ -f /vagrant/done ]; then
    rm /vagrant/done
fi

if [ -f /vagrant/output.txt ]; then
    rm /vagrant/output.txt
fi

if [ -f /vagrant/identity ]; then
    rm /vagrant/identity
    sed -i '/oneusefabrickey/d' /home/vagrant/.ssh/authorized_keys
    rm /vagrant/identity.pub
fi

sudo crontab -u vagrant /vagrant/crontab

exit 0
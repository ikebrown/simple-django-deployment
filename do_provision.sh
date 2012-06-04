#!/bin/bash
echo Vagrant has a bug with provisioning, starting provisioning via crontab.
echo Check output.txt for progress.
echo When done a done file will appear next to output.txt. 
sudo crontab -u vagrant /vagrant/crontab
exit 0
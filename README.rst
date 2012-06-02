How to deploy simple-django-deployment.

1. Install VirtualBox
2. Install Ruby
3. Install Vagrant
4. Make a directory e.g. deployment.
5. Save the Vagrant fro github in the deployment dir.
6. Open the deployment dir, hold shift and righ "Open command window here"
7. In the command window do "vagrant box add" and "vagrant up"
8. Wait for provisioning to complete, point your browser to http://33.33.33.10/
9. If no page opens, fire up putty and log in to 33.33.33.10 using the username vagrant and password vagrant if needed. After login cd to /vagrant/ and run ./provision.sh to see what went wrong. Fix the error and send me a pull request. ;)

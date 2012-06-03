What does simple-django-deployment give you?

- Nginx
- Gunicorn
- Supervisord
- Postgresql
- Rabbitmq
- Elasticsearch
- Celery
- Memcached
- Haystack - pyelasticsearch - haystack-celery
- Django CMS - with a search apphook
- Django-shop - with django categories and # todo searchable products 

How to deploy simple-django-deployment.

1. Install VirtualBox.
2. Install Ruby.
3. Install Vagrant.
4. Make a directory e.g. deployment.
5. Save the Vagrant fro github in the deployment dir.
6. Open the deployment dir, hold shift and righ "Open command window here".
7. In the command window do "vagrant box add lucid32 http://files.vagrantup.com/lucid32.box" and "vagrant up".
8. Log in to 33.33.33.10 using the username vagrant and password vagrant if needed.
9. After login:

::

    cd /vagrant/
    sudo apt-get install git-core 
    git clone git://github.com/fivethreeo/simple-django-deployment.git
    ./provision.sh

Wait for provisioning to complete.
    
10. Point your browser to http:://33.33.33.10/.

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
4. Clone this repository to a directory or download zipfile and extract to a directory.
5. Open the directory in explorer, hold shift and right click, choose "Open command window here".
6. In the command window do "vagrant box add lucid32 http://files.vagrantup.com/lucid32.box" and "vagrant up".
7. Wait for provisioning to complete. 
8. Point your browser to http:://33.33.33.10/admin/ or to http:://33.33.33.10/admin/, login using simple / example123.

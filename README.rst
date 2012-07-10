============================================
What does simple-django-deployment give you?
============================================

- Nginx
- Gunicorn
- Supervisord
- Postgresql
- Rabbitmq
- Elasticsearch
- Celery
- Memcached
- Haystack - pyelasticsearch - haystack-celery
- Django CMS - with search
- Django-shop - with django-categories and searchable products - rudimentary shop so far but all parts present

How to deploy simple-django-deployment.
---------------------------------------

1. Install VirtualBox.
2. Install Ruby.
3. Install Vagrant.
4. Clone this repository to a directory or download zipfile and extract to a directory.
5. Open the directory in explorer, hold shift and right click, choose "Open command window here".
6. In the command window do "vagrant box add lucid32 http://files.vagrantup.com/lucid32.box" and "vagrant up".
7. Wait for provisioning to complete. Be very patient. If you are windows sellout like me, you could grab cygwin to tail -f output.txt in the deployment dir.
8. Point your browser to http:://http://127.0.0.1:8080/ or to http://127.0.0.1:8080/admin/, login using (username: simple / password: example123).

If deployment fails somehow you can login to 127.0.0.1:2222 using putty (username: vagrant / password: vagrant).

How to push new changes?
------------------------

Login to 127.0.0.1:2222 using putty (username: vagrant / password: vagrant)

And isssue this command:

::
    
    cd /vagrant
    fab -R vagrant -i identity config push reload

All commands require ``fab -R vagrant -i identity config [command]`` to run properly

How to update the design?
-------------------------

Open ``media/design.ai`` in Illustrator.

Use save for web and devices, save images only to ``project/simple/static/simple/``.

Push changes.




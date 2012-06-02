"""
www.vagrantup.com
Get vagrant up and running using something like this Vagrantfile:

Vagrant::Config.run do |config|
    config.vm.define :dev do |config|
      config.vm.box = "base64"
      config.vm.forward_port("webdev", 80, 8080)
      config.vm.customize do |vm|
          vm.memory_size = 256
      end
    end
end

Login at 127.0.0.1:2222 using the key here
   
   https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.ppk

and run this:

sudo aptitude update

sudo aptitude install -y git-core python python-dev python-setuptools

sudo easy_install -U pip ; sudo pip install fabric ; sudo pip install jinja2

wget https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.ppk

git clone ssh://oyvind@mainframe.cylon.no/home/oyvind/innomed-deployment

cd innomed-deployment

# config below is needed because of fab_settings.py, needs a brilliant mind to set mine straight, yours?

fab -R vagrant config setup_all # if fails vagrant destroy and add a " -w" here
# you will get 4 prompts 2 for java 2 for postfix, use tab and space to navigate
"""
import contextlib
from fabric.api import env, run, cd, sudo, put, get, require, settings, hide, local
from fabric.contrib import project, files, console

import time

from fab_settings import global_settings, group_settings, servers

# prepare settings
groupmapping = {}
roledefs = {}
for role, servers in servers.items():
    roledefs[role] = []
    for server in servers:
       roledefs[role].append(server[0])
       groupmapping[server[0]] = server[1]
       
env.roledefs = roledefs

def config():
    """ Utility: Setup settings """
    for key, setting in global_settings:
        if isinstance(setting, basestring):
            setting = setting % env
        env[key] = setting
    for key, setting in group_settings[groupmapping[env.host_string]].items():
        if isinstance(setting, basestring):
            setting = setting % env
        env[key] = setting

def create_manage_command(cmd):
    """  Utility: return manage.py oneliner """
    cmdstr = "PYTHONPATH=%(extra_paths)s /home/%(user)s/%(project_name)s/bin/python /home/%(user)s/%(project_name)s/project/%(project_name)s/manage.py %%s" % env
    return cmdstr % cmd
    
def manage(cmd, use_sudo=False):
    runcmd = create_manage_command(cmd)
    if use_sudo:
        sudo(runcmd)
    else:
        run(runcmd)

def fix_ph():
    run(python("from cms.models.pluginmodel import CMSPlugin;CMSPlugin.objects.filter(placeholder=781).update(language='nb')"))
    
def script(cmd):
    run("mkdir -p %(root)s/scripts" % env)
    fl = "scripts/%s" % cmd
    fr = "%s/%s" % (env.root, fl)
    put(fl, fr)
    """  Utility: return python one liner """
    cmdstr = "PYTHONPATH=%(extra_paths)s DJANGO_SETTINGS_MODULE=settings /home/%(user)s/%(project_name)s/bin/python %%s" % env
    return run(cmdstr % fr)
    
def python(cmd):
    """  Utility: return python one liner """
    cmdstr = "PYTHONPATH=%(extra_paths)s DJANGO_SETTINGS_MODULE=settings /home/%(user)s/%(project_name)s/bin/python -c \"%%s\"" % env
    return cmdstr % cmd

def collectstatic():
    run(create_manage_command("collectstatic --noinput -l"))
    
def deploy_full(full_setup=False, first_run=False):
    """Full deploy: push, pip and reload."""
    push()
    update_dependencies()
    collectstatic()
    reload(full_setup=full_setup, first_run=first_run)

def deploy_project():
    push()
    collectstatic()
    reload()

def push_project():
    """ Push out new code to the server """
    with settings(warn_only=True):
        local('tar -czf innomed_deployment.tar.gz . --exclude "%(project_name)s.tar.gz"' %  env)
        run("mkdir /home/%(user)s/tmp" % env)
        put("innomed_deployment.tar.gz", "/home/%(user)s/tmp" % env)
        with cd("/home/%(user)s/tmp" % env):
            run("tar -xzf %(project_name)s.tar.gz" %  env) 
            run("rm -rf /home/%(user)s/%(project_name)s/project" % env)
            run("cp -rf project /home/%(user)s/%(project_name)s/project" % env)
            run("rm -rf /home/%(user)s/%(project_name)s/external_apps" % env)
            run("cp -rf external_apps /home/%(user)s/%(project_name)s/external_apps" % env)
            run("rm -rf /home/%(user)s/%(project_name)s/local_apps" % env)
            run("cp -rf local_apps /home/%(user)s/%(project_name)s/local_apps" % env)
        run("rm -rf /home/%(user)s/tmp" % env)
                     
def push_django_settings():
    files.upload_template("config/local_settings.py", "/home/%(user)s/%(project_name)s/project/%(project_name)s/local_settings.py" % env, context=env)   

def push():
    push_project()
    push_django_settings()

def update_dependencies():    
    """ Update requirements remotely """
    put("config/requirements.txt", "%(root)s/requirements.txt" % env)
    run("%(root)s/bin/pip install -r %(root)s/requirements.txt" % env)

def upgrade_dependency(dep):
    run("%s %s" % ("%(root)s/bin/pip install -U" % env, dep) )

def uninstall_dependency(dep):
    run("%s %s" % ("%(root)s/bin/pip uninstall" % env, dep) )

def reload_nginx():
    sudo("kill -HUP `cat %(nginx_pidfile)s`" % env)

def reload(full_setup=False, first_run=False):
    """ Reload webserver/webapp """
    if full_setup==False:
        sudo("kill -QUIT `cat %(nginx_pidfile)s`" % env)
        sudo("supervisorctl restart all")
    sudo("%(nginx_bin)s" % env)
    
def start_gunicorn():
    sudo("supervisorctl start %(user)s_gunicorn" % env)

def stop_gunicorn():
    sudo("supervisorctl stop %(user)s_gunicorn" % env)
        
def runserver():
    stop_gunicorn()
    manage("runserver %(gunicorn_host)s:%(gunicorn_port)s & read -p 'Press any key to continue... ' -n1 -s" % env)
    start_gunicorn()
    
# OK, simple stuff done. Here's a more complex example: provisioning
# a server the simplistic way.

def setup_all():
    """ Setup all parts on one single server adds a fully running setup """
    setup_webserver()
    setup_webapp()
    update_dependencies()
    push()
    setup_dbserver()
    configure_db()
    deploy_full(full_setup=True)
    syncdb()
    add_site()
    add_superuser()
    setup_celery()
    setup_memcached()
    setup_elasticsearch()
    setup_supervisord()
    configure_supervisor_gunicorn()
    configure_supervisor_celeryd()
    configure_supervisor_elasticsearch()
        
def setup_instance():
    setup_webapp()
    update_dependencies()
    push()
    configure_db()
    deploy_full(first_run=True)
    syncdb()
    add_site()
    add_superuser()
    configure_celery()
    configure_memcached()
    configure_supervisor_gunicorn()
    configure_supervisor_celeryd()
    configure_supervisor_elasticsearch()
    
def setup_elasticsearch():
    """ Setup search server """
    with settings(warn_only=True):
        sudo("aptitude update")
        put("jdk-6u31-linux-i586.bin", use_sudo=True)
        sudo("chmod u+x jdk-6u31-linux-i586.bin")
        sudo("./jdk-6u31-linux-i586.bin")
        sudo("mv jdk1.6.0_31 /usr/lib/jvm/")
        sudo('sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.6.0_31/bin/java" 1')
        run("wget https://github.com/downloads/elasticsearch/elasticsearch/elasticsearch-0.19.2.tar.gz -O elasticsearch.tar.gz")
        sudo("tar -xf elasticsearch.tar.gz")
        sudo("rm elasticsearch.tar.gz")
        sudo("mv elasticsearch-* elasticsearch")
        sudo("mv elasticsearch /usr/local/share")
        
def setup_libreoffice():
    with settings(warn_only=True):
        sudo("aptitude update")
        sudo("aptitude -y install python-software-properties")
        sudo("sudo add-apt-repository ppa:libreoffice/ppa")
        sudo("aptitude update")
        sudo("aptitude -y install libreoffice-calc")

def setup_dbserver():
    """ Setup database server with postgis_template db """
    sudo("aptitude update")
    sudo("aptitude -y install git-core "
                              "build-essential "
                              "libpq-dev subversion mercurial "
                              "postgresql-8.4 postgresql-server-dev-8.4")
    sudo("pg_dropcluster --stop 8.4 main")
    sudo("unset LANG && pg_createcluster --start -e UTF-8 8.4 main")
    sudo("mkdir /var/lib/postgresql/8.4/main/pg_log")
    sudo("chown postgres:postgres /var/lib/postgresql/8.4/main/pg_log")
    configure_dbserver()
                              
def configure_dbserver():
    put("postgresql/pg_hba.conf",
        "/etc/postgresql/8.4/main/pg_hba.conf" % env,
        use_sudo=True)
    files.upload_template("postgresql/postgresql.conf",
        "/etc/postgresql/8.4/main/postgresql.conf" % env,
        use_sudo=True, context=env, use_jinja=True)
    sudo("invoke-rc.d postgresql-8.4 restart")
    time.sleep(7)

def setup_webserver():
    """
    Set up (bootstrap) a new server.
    
    This essentially does all the tasks in the script done by hand in one
    fell swoop. In the real world this might not be the best way of doing
    this -- consider, for example, what the various creation of directories,
    git repos, etc. will do if those things already exist. However, it's
    a useful example of a more complex Fabric operation.
    """

    # Initial setup and package install.
    sudo("aptitude update")
    sudo("aptitude -y install git-core python-dev python-setuptools libjpeg62 libjpeg62-dev "
                              "postgresql-dev postgresql-client build-essential "
                              "libpq-dev subversion mercurial "
                              "nginx "
                              "python-pip")

    files.upload_template("nginx/nginx_webserver.conf", "%(nginx_confdir)snginx.conf" % env, use_sudo=True, context=env)
    sudo("mkdir -p %(nginx_confdir)ssites-enabled" % env)

 
def setup_webapp():
    """ Setup virtualenv/startup scripts/configs for webapp """
    sudo("pip install -U virtualenv")
    run("virtualenv /home/%(user)s/%(project_name)s --distribute" % env)
    run("mkdir -p /home/%(user)s/%(project_name)s" % env)
    run("mkdir -p /home/%(user)s/static" % env)
    run("mkdir -p /home/%(user)s/static/media" % env)
    files.upload_template("nginx/nginx_webapp.conf", "%(nginx_confdir)ssites-enabled/%(servername)s.conf" % env, use_sudo=True, context=env)

def setup_celery():
    sudo("aptitude update")
    sudo("aptitude -y install python-software-properties")
    sudo("sudo add-apt-repository \"deb http://www.rabbitmq.com/debian/ testing main\"")
    run("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc")
    sudo("apt-key add rabbitmq-signing-key-public.asc")
    sudo("aptitude update")
    sudo("aptitude -y install rabbitmq-server")
    configure_celery()
    
def configure_celery():
    sudo("rabbitmqctl add_user %(db_user)s %(db_password)s" % env)
    sudo("rabbitmqctl add_vhost %(db_name)s" % env)
    sudo("rabbitmqctl set_permissions -p %(db_name)s %(db_user)s  \".*\" \".*\" \".*\"" % env)

def setup_memcached():
    sudo("aptitude -y install memcached")
    put("memcached/memcached", "/etc/init.d/memcached", use_sudo=True)
    sudo("chown root:root /etc/init.d/memcached")
    sudo("chmod 755 /etc/init.d/memcached")
    put("memcached/start-memcached", "/usr/share/memcached/scripts/start-memcached", use_sudo=True)
    sudo("chown root:root /usr/share/memcached/scripts/start-memcached")
    sudo("chmod 755 /usr/share/memcached/scripts/start-memcached")
    configure_memcached()

def configure_memcached():
    files.upload_template("memcached/memcached.conf", "/etc/memcached_%(user)s.conf" % env, use_sudo=True, context=env)

def setup_supervisord():
    sudo("aptitude update")
    sudo("aptitude -y install supervisor")   
    
def configure_supervisor_gunicorn():
    files.upload_template("supervisor/gunicorn_supervisor.conf", "/etc/supervisor/conf.d/gunicorn_%(user)s.conf" % env, use_sudo=True, context=env)
    sudo("killall -HUP supervisord")
    
def configure_supervisor_celeryd():
    files.upload_template("supervisor/celeryd_supervisor.conf", "/etc/supervisor/conf.d/celeryd_%(user)s.conf" % env, use_sudo=True, context=env)
    sudo("killall -HUP supervisord")
    
def configure_supervisor_elasticsearch():
    files.upload_template("supervisor/elasticsearch_supervisor.conf", "/etc/supervisor/conf.d/elasticsearch_%(user)s.conf" % env, use_sudo=True, context=env)
    run("mkdir -p /home/%(user)s/%(project_name)s/logs/elasticsearch" % env)
    run("mkdir -p /home/%(user)s/%(project_name)s/data/elasticsearch" % env)
    run("chmod u+rw /home/%(user)s/%(project_name)s/data/elasticsearch" % env)
    sudo("killall -HUP supervisord")
    
def supervisorctl(cmd):
    sudo("supervisorctl %s" % cmd)

def add_db(dbname, owner, template=''):
    """ Add database: add_db:dbname,owner,<template> """
    if template:
        template = ' TEMPLATE %s' % template
    sudo('psql -c "CREATE DATABASE %s%s ENCODING \'unicode\' OWNER %s" -d postgres -U %s' % (dbname, template, owner, env.postgres_user or 'postgres'))

def add_dbuser(user, passwd):
    """ Add database user: add_dbuser:user,password """
    with settings(warn_only=True):
        sudo('psql -c "CREATE USER %s WITH NOCREATEDB NOCREATEUSER PASSWORD \'%s\'" -d postgres -U %s' % (user, passwd, env.postgres_user or 'postgres'))
    
def configure_db():
    """ Set up webapps database """
    add_dbuser(env.db_user, env.db_password)
    add_db(env.db_name, env.db_user)

def drop_database():
    sudo('%(pg_dropdb)s %(db_name)s -U %(postgres_user)s' % env)

def syncdb():
    """ Run syncdb """
    run(create_manage_command("syncdb --noinput --all"))

def migrate(arg=''):
    """ Run migrate """
    run(create_manage_command("migrate %s" % arg))

def rebuild_index():
    """ Run rebuild_index """
    manage("rebuild_index")

def add_site():
    """ Add example django site """
    run(python("from django.contrib.sites.models import Site;Site.objects.create(domain='%(servername)s', name='%(project_name)s')" % env))
    
def add_superuser():
    """ Add django superuser """
    run(python("from django.contrib.auth.models import User;User.objects.create_superuser('%(db_user)s', '%(db_user)s@%(servername)s', '%(db_password)s')" % env))
    
def dump_database():
    run("%(pg_dump)s -U %(db_user)s -O -x -c %(db_name)s > /home/%(user)s/fab_dmp.sql" % env)
    get("/home/%(user)s/fab_dmp.sql" % env, "../fab_dmp.sql")
    run("rm /home/%(user)s/fab_dmp.sql" % env)

def load_database():
    if console.confirm("Drop database before loading?"):
        drop_database()
        add_db(env.db_name, env.db_user)
    put("../fab_dmp.sql", "/home/%(user)s/fab_dmp.sql" % env)
    run("cat /home/%(user)s/fab_dmp.sql | %(psql)s -U %(db_user)s %(db_name)s" % env)
    run("rm /home/%(user)s/fab_dmp.sql" % env)

def dump_media():
    run("cd %(mediaroot)s && tar czvf /home/%(user)s/fab_media.tar.gz *" % env)
    get("/home/%(user)s/fab_media.tar.gz" % env, "../fab_media.tar.gz")
    run("rm /home/%(user)s/fab_media.tar.gz" % env)

def load_media():
    put("../fab_media.tar.gz", "/home/%(user)s/fab_media.tar.gz" % env)
    run("cd %(mediaroot)s && tar xzvf /home/%(user)s/fab_media.tar.gz" % env)
    run("rm /home/%(user)s/fab_media.tar.gz" % env)

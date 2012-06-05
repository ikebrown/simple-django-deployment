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

def create_manage_command(command):
    """  Utility: return manage.py oneliner """
    command_string = "DJANGO_SETTINGS_MODULE=simple.settings PYTHONPATH=%(extra_paths)s /home/%(user)s/%(project_name)s/bin/python /home/%(user)s/%(project_name)s/project/%(project_name)s/manage.py %%s" % env
    return command_string % command
    
def python_shell():
    """  Utility: return manage.py oneliner """
    command_string = "DJANGO_SETTINGS_MODULE=simple.settings PYTHONPATH=%(extra_paths)s /home/%(user)s/%(project_name)s/bin/python" % env
    return run(command_string)
        
def manage(command, use_sudo=False):
    runcommand = create_manage_command(command)
    if use_sudo:
        sudo(runcommand)
    else:
        run(runcommand)

def fix_placeholder():
    run(python("from cms.models.pluginmodel import CMSPlugin;CMSPlugin.objects.filter(placeholder=781).update(language='nb')"))
    
def run_script(command):
    run("mkdir -p %(root)s/scripts" % env)
    local_file = "scripts/%s" % command
    remote_file = "%s/%s" % (env.root, local_file)
    files.upload_template(local_file, remote_file, context=env)
    """  Utility: return python one liner """
    command_string = "PYTHONPATH=%(extra_paths)s DJANGO_SETTINGS_MODULE=simple.settings /home/%(user)s/%(project_name)s/bin/python %%s" % env
    return run(command_string % remote_file)

        
def python(command):
    """  Utility: return python one liner """
    command_string = "PYTHONPATH=%(extra_paths)s DJANGO_SETTINGS_MODULE=simple.settings /home/%(user)s/%(project_name)s/bin/python -c \"%%s\"" % env
    return command_string % command

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
        local('tar -czf %(project_name)s.tar.gz . --exclude "%(project_name)s.tar.gz"' %  env)
        run("mkdir /home/%(user)s/tmp" % env)
        put("%(project_name)s.tar.gz" % env, "/home/%(user)s/tmp" % env)
        with cd("/home/%(user)s/tmp" % env):
            run("tar -xzf %(project_name)s.tar.gz" %  env) 
            run("rm -rf /home/%(user)s/%(project_name)s/project" % env)
            run("cp -rf project /home/%(user)s/%(project_name)s/project" % env)
            run("rm -rf /home/%(user)s/%(project_name)s/local_apps" % env)
            run("cp -rf local_apps /home/%(user)s/%(project_name)s/local_apps" % env)
        run("rm -rf /home/%(user)s/tmp" % env)
                     
def push_django_settings():
    files.upload_template("config/local_settings.py", "/home/%(user)s/%(project_name)s/project/%(project_name)s/local_settings.py" % env, context=env)   

def push():
    push_project()
    push_django_settings()
    
def make_bundle():
    put("config/requirements.txt", "/home/%(user)s/requirements.txt" % env)
    files.upload_template("make_bundle.py", "/home/%(user)s/make_bundle.py" % env, context=env)    
    run("/home/%(user)s/%(project_name)s/bin/python /home/%(user)s/make_bundle.py" % env)
    
def install_bundle():    
    run("/home/%(user)s/%(project_name)s.bundle" % env)
    
def update_dependencies():    
    """ Update requirements remotely """
    put("config/requirements.txt", "%(root)s/requirements.txt" % env)
    def inner_update(retries=3):
        with settings(warn_only=True):
            output = run("PIP_DOWNLOAD_CACHE=/vagrant/pipcache %(root)s/bin/pip install -r %(root)s/requirements.txt" % env)
        if output.failed:
            if retries > 0:
                inner_update(retries=retries-1)
    inner_update()

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
    setup_databaseserver()
    configure_database()
    deploy_full(full_setup=True)
    syncdb()
    setup_celery()
    setup_memcached()
    setup_elasticsearch()
    setup_supervisord()
    configure_supervisor_gunicorn()
    configure_supervisor_celeryd()
    configure_supervisor_elasticsearch()
    run_script('python_fixture.py')
    
def setup_instance():
    setup_webapp()
    update_dependencies()
    push()
    configure_database()
    deploy_full(first_run=True)
    syncdb()
    configure_celery()
    configure_memcached()
    configure_supervisor_gunicorn()
    configure_supervisor_celeryd()
    configure_supervisor_elasticsearch()
    run_script('python_fixture.py')

def setup_elasticsearch():
    """ Setup search server """
    sudo("aptitude update")
    sudo('aptitude -y install  install openjdk-6-jre')
    run("wget https://github.com/downloads/elasticsearch/elasticsearch/elasticsearch-0.19.2.tar.gz -O elasticsearch.tar.gz")
    sudo("tar -xf elasticsearch.tar.gz")
    sudo("rm elasticsearch.tar.gz")
    sudo("mv elasticsearch-* elasticsearch")
    sudo("mv elasticsearch /usr/local/share")
        
def setup_libreoffice():
    sudo("aptitude update")
    sudo("aptitude -y install python-software-properties")
    sudo("sudo add-apt-repository ppa:libreoffice/ppa")
    sudo("aptitude update")
    sudo("aptitude -y install libreoffice-calc")

def setup_databaseserver():
    """ Setup database server with database """
    sudo("aptitude update")
    sudo("aptitude -y install git-core "
                              "build-essential "
                              "libpq-dev subversion mercurial "
                              "postgresql-8.4 postgresql-server-dev-8.4")
    sudo("pg_dropcluster --stop 8.4 main")
    sudo("unset LANG && pg_createcluster --start -e UTF-8 8.4 main")
    sudo("mkdir /var/lib/postgresql/8.4/main/pg_log")
    sudo("chown postgres:postgres /var/lib/postgresql/8.4/main/pg_log")
    configure_databaseserver()
                              
def configure_databaseserver():
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
    configure_webapp()

def configure_webapp():
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
    
def supervisorctl(command):
    sudo("supervisorctl %s" % command)

def add_database(database_name, owner, template=''):
    """ Add database: add_database:database_name,owner,<template> """
    if template:
        template = ' TEMPLATE %s' % template
    sudo('psql -c "CREATE DATABASE %s%s ENCODING \'unicode\' OWNER %s" -d postgres -U %s' % (database_name, template, owner, env.postgres_user or 'postgres'))

def add_databaseuser(user, passwd):
    """ Add database user: add_databaseuser:user,password """
    with settings(warn_only=True):
        sudo('psql -c "CREATE USER %s WITH NOCREATEDB NOCREATEUSER PASSWORD \'%s\'" -d postgres -U %s' % (user, passwd, env.postgres_user or 'postgres'))
    
def configure_database():
    """ Set up webapps database """
    add_databaseuser(env.db_user, env.db_password)
    add_database(env.db_name, env.db_user)

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

def dump_database():
    run("%(pg_dump)s -U %(db_user)s -O -x -c %(db_name)s > /home/%(user)s/fab_dmp.sql" % env)
    get("/home/%(user)s/fab_dmp.sql" % env, "../fab_dmp.sql")
    run("rm /home/%(user)s/fab_dmp.sql" % env)

def load_database():
    if console.confirm("Drop database before loading?"):
        drop_database()
        add_database(env.db_name, env.db_user)
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

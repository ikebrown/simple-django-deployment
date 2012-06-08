import contextlib
from fabric.api import env, run, cd, sudo, put, get, require, settings, hide, local
from fabric.contrib import project, files, console

def master(bind_ip, install=False):
    if install:
        base_install()
        sudo("apt-get install salt-master")
    context = {'bind_ip': bind_ip, 'base': '/vagrant/salt'}
    files.upload_template("master.template", "/etc/salt/master", context=context, use_sudo=True)
    sudo("/etc/init.d/salt-master restart")
    
def minion(master_ip, install=False):
    if install:
        base_install()
        sudo("apt-get install salt-minion")    
    files.upload_template("minion.template", "/etc/salt/minion", context={'master_ip': master_ip}, use_sudo=True)
    sudo("/etc/init.d/salt-minion restart")
    
def base_install():
    sudo("apt-get install python-software-properties")
    sudo("add-apt-repository ppa:saltstack/salt")
    sudo("apt-get update")

include:
  - supervisord
  - virtualenv
  - pip
  
app-pkgs:
  pkg:
    - installed
    - names:
      - supervisor

install-virtualenv:
  pip:
    - installed
    - name: virtualenv

{% set root="/home/vagrant/simple" %}
{% set virtualenv='%s/venv' % root %}
{% set project='%s/project/simple' % root %}
{% set ip='127.0.0.1' %}
{% set port='8001' %}
{% set gunicorn_args="--preload --workers 2" %}
{% set gunicorn_user="vagrant" %}

/home/{{ gunicorn_user }}/simple:
   file.directory:
     - makedirs: True
     - user: vagrant
       
/etc/supervisor/conf.d/{{ gunicorn_user }}_gunicorn.conf:
  file.managed:
    - source: salt://django_project/gunicorn_supervisor.conf
    - template: jinja
    - context:
      python: {{ virtualenv }}/bin/python
      ip: {{ ip }}
      port: {{ port }}
      gunicorn_args: {{ gunicorn_args }}
      gunicorn_user: {{ gunicorn_user }}
      log: {{ project }}/gunicorn.log
      program_name: {{ gunicorn_user }}_gunicorn
      extra_paths:
        - {{ root }}/project
        - {{ root }}/local_apps
          
/home/{{ gunicorn_user }}/simple/venv:
   virtualenv:
     - managed
     - distribute: True
     - require:
       - pip: install-virtualenv
       - file: /home/{{ gunicorn_user }}/simple
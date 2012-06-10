include:
  - supervisord
  - virtualev
  
app-pkgs:
  pkg:
    - installed
    - names:
      - python-virtualenv
      - supervisor

{% set root="/home/vagrant/simple" %}
{% set virtualenv='%s/venv' % root %}
{% set project='%s/project/simple' % root %}
{% set ip='127.0.0.1' %}
{% set port='8001' %}
{% set gunicorn_args="--preload --workers 2" %}
{% set gunicorn_user="vagrant" %}

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
    - watch:
      - virtualenv: /home/{{ gunicorn_user }}/simple/venv
          
/home/{{ gunicorn_user }}/simple/venv:
   virtualenv:
     - distribute: True
     - system_site_packages: True
     - manage
     - require:
       - pkg: app-pkgs
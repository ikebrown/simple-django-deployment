postgresql-install:
   pkg.installed:
     - names:
       - postgresql-8.4
       - postgresql-server-dev-8.4

postgresql-8.4:
  service:
    - running
    - require:
      - pkg: postgresql-server-dev-8.4
      - cmd: create_cluster

create_cluster:
  cmd.wait:
    - name: LANG= pg_createcluster --start 8.4 main
    - watch:
      - pkg: postgresql-install

/var/lib/postgresql/8.4/main/pg_log:
  file.directory:
    - makedirs: True
    - user: postgres
    - group: postgres
    - require:
      - cmd: create_cluster
       
/etc/postgresql/8.4/main/postgresql.conf:
  file.managed:
    - source: salt://postgresql_server/postgresql.conf
    - watch:
      - pkg: postgresql-install
    - template: jinja
    - context:
        listen_addresses: "127.0.0.1"
        postgres_logging: "off"
    - watch_in:
       - service: postgresql-8.4
    - require:
      - cmd: create_cluster   
       
/etc/postgresql/8.4/main/pg_hba.conf:
  file.managed:
    - source: salt://postgresql_server/pg_hba.conf
    - watch:
      - pkg: postgresql-install
    - template: jinja
    - context:
        trust_host: "127.0.0.1"
    - watch_in:
       - service: postgresql-8.4
    - require:
      - cmd: create_cluster       

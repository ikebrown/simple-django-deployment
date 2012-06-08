postgresql-install:
   pkg.installed:
     - names:
       - postgresql-8.4
       - postgresql-server-dev-8.4

new_cluster:
  cmd.run:
    - name: pg_createcluster --start -e UTF-8 8.4 main
    - watch:
      - pkg: postgresql-install
      
/var/lib/postgresql/8.4/main/pg_log:
  file.directory:
    - makedirs: True
    - user: postgres
    - group: postgres
       
/etc/postgresql/8.4/main/postgresql.conf:
  file.managed:
    - source: salt://postgresql_server/postgresql.conf
    - watch:
      - pkg: postgresql-install
    - template: jinja
    - context:
        listen_addresses: "127.0.0.1"
        postgres_logging: "off"

/etc/postgresql/8.4/main/pg_hba.conf:
  file.managed:
    - source: salt://postgresql_server/pg_hba.conf
    - watch:
      - pkg: postgresql-install
    - template: jinja
    - context:
        trust_host: "127.0.0.1"
         
postgresql-8.4:
  service:
     - running
     - watch:
       - file: /etc/postgresql/8.4/main/postgresql.conf
       - file: /etc/postgresql/8.4/main/pg_hba.conf
     - require:
       - pkg: postgresql-install
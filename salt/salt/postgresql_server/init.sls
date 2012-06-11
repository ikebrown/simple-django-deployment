postgresql-install:
   pkg.installed:
     - names:
       - postgresql-8.4
       - postgresql-server-dev-8.4

drop_cluster:
  cmd.wait:
    - name: pg_dropcluster --stop 8.4 main
    - unless: 
    - use_in:
      - cmd: postgresql-install
          
create_cluster:
  cmd.wait:
    - name: LANG= pg_createcluster --start 8.4 main
    - use_in:
      - cmd: drop_cluster
       
postgresql-8.4:
  service:
    - name: postgresql-8.4
    - running
    - require:
      - pkg: postgresql-install
      - file: pg_hba.conf
      - file: postgresql.conf
      - file: pg_log
                  
pg_log:
  file.directory:
    - name: /var/lib/postgresql/8.4/main/pg_log
    - makedirs: True
    - user: postgres
    - group: postgres
    - watch_in:
       - service: postgresql-8.4
    - require:
      - pkg: postgresql-install
      
postgresql.conf:
  file.managed:
    - source: salt://postgresql_server/postgresql.conf
    - name: /etc/postgresql/8.4/main/postgresql.conf
    - user: postgres
    - group: postgres
    - watch:
      - pkg: postgresql-install
    - template: jinja
    - context:
        listen_addresses: "127.0.0.1"
        postgres_logging: "off"
    - watch_in:
       - service: postgresql-8.4
    - require:
      - pkg: postgresql-install
             
pg_hba.conf:
  file.managed:
    - source: salt://postgresql_server/pg_hba.conf
    - name: /etc/postgresql/8.4/main/pg_hba.conf
    - user: postgres
    - group: postgres
    - template: jinja
    - context:
        trust_host: "127.0.0.1"
    - watch_in:
       - service: postgresql-8.4
    - require:
      - pkg: postgresql-install       

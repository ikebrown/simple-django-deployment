openjdk-6-jre:
  pkg:
    - installed
    
/usr/local/share/elasticsearch/config/elasticsearch.yml:
  file:
    - managed
    - source: salt://searchserver/elasticsearch.yml
    - template: jinja
    - context:
        cluster: "elasticsearch"
        host: "127.0.0.1"

/usr/local/share/elasticsearch/bin/service/elasticsearch.conf:
  file:
    - managed
    - source: salt://searchserver/elasticsearch.conf
    - template: jinja
    - context:
        home: "/usr/local/share/elasticsearch"
    
install_elasticsearch.sh:
  file.managed:
    - source: salt://searchserver/install.sh
    - name: /usr/local/bin/install_elasticsearch.sh
    - mode: 500

/usr/local/bin/install_elasticsearch.sh:
  cmd.run:
    - shell: /bin/bash
    - require:
      - file: install_elasticsearch.sh
    - unless: test -d /usr/local/share/elasticsearch/
    
elasticsearch:
  service:
    - running
    - require:
      - cmd: /usr/local/bin/install_elasticsearch.sh
      - pkg: openjdk-6-jre
    - watch:
      - file: /usr/local/share/elasticsearch/bin/service/elasticsearch.conf
      - file: /usr/local/share/elasticsearch/config/elasticsearch.yml

      

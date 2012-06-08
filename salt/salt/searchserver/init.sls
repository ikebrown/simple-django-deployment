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
            
elasticsearch:
  service:
    - running
    - require:
      - pkg: openjdk-6-jre

cp.get_path: https://github.com/downloads/elasticsearch/elasticsearch/elasticsearch-0.19.2.tar.gz /tmp/elasticsearch.tar.gz
archive.tar: xzfv /tmp/elasticsearch.tar.gz
cmdmod.run: 'rm elasticsearch.tar.gz'
cmdmod.run: 'mv elasticsearch* elasticsearch'
cmdmod.run: 'mv elasticsearch /usr/local/share'
cp.get_path: http://github.com/elasticsearch/elasticsearch-servicewrapper/tarball/master /tmp/elasticsearch-servicewrapper.tar.gz
archive.tar: xzfv /tmp/eelasticsearch-servicewrapper.tar.gz
cmdmod.run: 'mv *servicewrapper*/service /usr/local/share/elasticsearch/bin/'
cmdmod.run: 'rm -Rf *servicewrapper*'
cmdmod.run: '/usr/local/share/elasticsearch/bin/service/elasticsearch install'
cmdmod.run: 'ln -s `readlink -f /usr/local/share/elasticsearch/bin/service/elasticsearch` /usr/local/bin/rcelasticsearch'

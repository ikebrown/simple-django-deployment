#!/bin/bash
wget https://github.com/downloads/elasticsearch/elasticsearch/elasticsearch-0.19.2.tar.gz -O /tmp/elasticsearch.tar.gz
wget https://github.com/elasticsearch/elasticsearch-servicewrapper/tarball/master -O /tmp/servicewrapper.tar.gz
tar -xzvf /tmp/elasticsearch.tar.gz -C /tmp/
rm /tmp/elasticsearch.tar.gz
mv /tmp/elasticsearch-* /tmp/elasticsearch
mv /tmp/elasticsearch /usr/local/share/
tar -xzvf /tmp/servicewrapper.tar.gz -C /tmp/
mv /tmp/*servicewrapper*/service /usr/local/share/elasticsearch/bin/
rm -Rf *servicewrapper*
/usr/local/share/elasticsearch/bin/service/elasticsearch install
ln -s `readlink -f /usr/local/share/elasticsearch/bin/service/elasticsearch` /usr/local/bin/rcelasticsearch
exit 0
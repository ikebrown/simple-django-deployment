/etc/nginx/nginx.conf:
  file:
    - managed
    - source: salt://webserver/nginx.conf
    - template: jinja
    - context:
        nginx_user: "www-data"
            
nginx:                 # ID declaration
  pkg:                  # state declaration
    - installed         # function declaration
  service:
    - running
    - watch:
      - file: /etc/nginx/nginx.conf
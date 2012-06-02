extra_paths = ':'.join([
    '/home/%(user)s/%(project_name)s/local_apps',
    '/home/%(user)s/%(project_name)s/project',
    '/home/%(user)s/%(project_name)s/project/%(project_name)s'
])
global_settings = [
    ('postgres_logging', False),
    ('django_debug', True),
    ('project_name', 'simple'),
    ('db_user', 'simple'),
    ('db_password', 'example123'),
    ('db_host', 'localhost'),
    ('use_nginx', 'true'),
    ('nginx_user', 'www-data'),
    ('nginx_confdir', '/etc/nginx/'),
    ('nginx_pidfile', '/var/run/nginx.pid'),
    ('nginx_bin', '/usr/sbin/nginx'),
    ('gunicorn_host', '127.0.0.1'),
    ('extra_settings', ''),
    ('staticroot', '/home/%(user)s/static'),
    ('mediaroot', '/home/%(user)s/static/media'),
    ('pg_dump', '/usr/bin/pg_dump'),
    ('pg_dropdb', '/usr/bin/dropdb'),
    ('psql', '/usr/bin/psql'),
    ('postgres_user', 'postgres'),
    ('elasticsearch_host', '127.0.0.1'),
    ('root', '/home/%(user)s/%(project_name)s'),
    ('extra_paths', extra_paths)
]

group_settings = {

    'vagrantdevelop': {
        'email': 'my@oh.no',
        'servername': 'simple.com',
        'gunicorn_port': '8001',
        'gunicorn_autostart': 'true',
        'db_name': 'simple_develop',
        'memcached_port': '11212'
    }
    
}

servers = {
#   'role', [
#       ['me@server:port', 'settings_group']
#   ],
    'vagrant': [['vagrant@127.0.0.1:22', 'vagrantdevelop']],
}
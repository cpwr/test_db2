bind = '0.0.0.0:8000'
workers = 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2
reload = True

errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s"' \
                    ' %(s)s %(b)s "%(f)s" "%(a)s"'

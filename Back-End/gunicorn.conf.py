bind = '0.0.0.0:8080'
errorlog = 'gunicorn_error.log'
loglevel = 'debug'

thread = 5
worker_class = 'gthread'
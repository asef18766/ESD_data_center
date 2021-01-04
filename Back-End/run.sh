echo "" > gunicorn_error.log
echo "" > runtime.log
gunicorn app:app -c gunicorn.conf.py
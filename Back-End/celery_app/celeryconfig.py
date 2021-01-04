broker_url = 'redis://127.0.0.1:6379/1'
result_backend = 'redis://127.0.0.1:6379/2'  
timezone = 'Asia/Taipei'

imports = ( 
    'celery_app.serial_task'
)
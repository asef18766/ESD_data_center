import time  
from . import app  
  
@app.task  
def create_link(s):
    

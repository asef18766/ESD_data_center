from . import (
    app,
    CONNECTION_WAIT_TIME
)
from .endpoint import (
    conn_serial,
    dumpLines
)
from logging import info
from serial import Serial
from json import (
    loads,
    dumps
)
from cache.node_config import get_lastest_cfg_ver

PING_TIME = 0.5

@app.task(time_limit=CONNECTION_WAIT_TIME)
def conn_dev(dev_port:str, baud_rate:int, timeout:int):
    '''
    try to connect to a serial device and retreive connection status as result
    '''
    print("connection started")
    sio = conn_serial(dev_port, baud_rate, timeout)

@app.task
def data_collector(sio:Serial, node_token:str):
    cfg_ver = get_lastest_cfg_ver(node_token)
    while True:
        sio.readline()
        for l in dumpLines(sio):
            if l[0] == '[' and l[-1] == ']':
                info(l)
                continue
            data:dict = loads(l)
            
            # request for new config
            if "version" in data:
                pass
            # sending operation info
            # also check for latest update info
            elif "amount" in data and "device" in data:
                n_ver = get_lastest_cfg_ver(node_token)
                
                # if there's a new config avaible
                if n_ver > cfg_ver:
                    # send version info
                    pass


from logging import error

from .serial_task import conn_dev

def conn_local_dev(node_token:str, dev_port:str, baud_rate:int, timeout:int)->bool:
    '''
    try to connect to a serial device and retreive connection status as result
    '''
    try:
        sio = conn_dev.apply_async((dev_port, baud_rate, timeout))
        sio.wait()
        
    except Exception as e:
        error(e)
        return False
    return True

def test_connect(node_token:str, conn_method:dict)->bool:
    if conn_method["type"] == "USB_Connection":
        return conn_local_dev(node_token, conn_method["fd"], 9600, 1)
    elif conn_method["type"] == "Network_Connection":
        raise ValueError(f"still not implemented ... qwq")
    else:
        raise ValueError(f"invaild connection type {conn_method['type']}")

if __name__ == "__main__":
    # try to create task
    conn_local_dev("/dev/ttyUSB0", 9600, 1)
    #serial_task.create_link.apply_async(["OAO"])

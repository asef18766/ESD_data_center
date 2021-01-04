import serial
import string
import json
from serial import Serial
from database.node.config import (
    get_node_config
)

def bytes_filter(by:bytes)->bytes:
    res = b""
    for i in by:
        if i in string.printable.encode():
            res += chr(i).encode()
    return res

def creat_dev_map(cfg:dict)->dict:
    '''
    this segment shall be substitude to other thing in the future
    '''
    map_ct = 3
    devmap = {}
    for d in cfg["input_devices"] + cfg["output_devices"]:
        devmap.update({
            d["hid"]:map_ct
        })
        map_ct+=1
    
    return {
        "success":True,
        "device_map":devmap
    }

def dumpOutput(sio:Serial):
    while True:
        res = sio.readline().strip()
        if res == b"":
            break
        res = bytes_filter(res)
        res = res.decode()
        if res == "":
            break
        print(res)

def dumpLines(sio:Serial)->list:
    li = []
    while True:
        res = sio.readline().strip()
        if res == b"":
            break
        res = bytes_filter(res)
        res = res.decode()
        if res == "":
            break
        li.append(res)
    return li

def get_cfg(ver:int, node_token:str)->dict:
    data = get_node_config(node_token)
    res = {
        "cfg": [],
        "latest_version": data["version"]
    }

    for idx, cfg in enumerate(data["configures"]):
        res["cfg"].append({
            "dev_hid": cfg["input_device"],
            "condition": cfg["condiction"],
            "val": cfg["value"],
            "sol": []
        })
        for op in cfg["solutions"]:
            res["cfg"][idx]["sol"].append({
                "dev_hid": op["output_device"],
                "operate": op["operate"]
            })
    return res

def get_cfg_lastest(node_token:str)->int:
    data = get_node_config(node_token)
    return data["version"]

def conn_serial(dev_port:str, baud_rate:int, timeout:int)->Serial:
    sio = serial.Serial(dev_port, baud_rate, timeout=timeout)
    node_token = None
    while True:
        res = sio.readline().strip()
        if res == b"":
            continue
        res = bytes_filter(res)
        res = res.decode()
        if res == "":
            continue
        print(res)
        if (res[0] == "{" and res[-1] == "}"):
            if res == '{"msg":"are you dead?"}':
                sio.write('{"msg":"i am alive"}\n'.encode())
                sio.flush()
            else:
                data = json.loads(res)
                if "version" in data:
                    sio.write(f"**{json.dumps(get_cfg(data['version'], node_token))}\n".encode())
                    sio.flush()
                    dumpOutput(sio)
                    break

        elif (res[0] == "[" and res[-1] == "]"):
            if res == '[register state created]':
                cfg = sio.readline().strip().decode()
                print(f"**receive cfg:{cfg}**")
                cfg = json.loads(cfg)
                node_token = cfg["token"]
                dmap = json.dumps(creat_dev_map(cfg), separators=(',', ':'))
                print(f"send dev map {dmap}")
                sio.write((dmap+"\n").encode())
                sio.flush()
            
            elif res == '[End of device mapping]':
                print(f"cur token: {node_token}")
                lver = get_cfg_lastest(node_token)
                print(f"send latest cfg version {lver}")
                print(f"send {json.dumps({'version':lver})}")
                sio.write(f"={json.dumps({'version':lver})}\n".encode())
                sio.flush()
    
    return sio

if __name__ == "__main__":
    '''
    sio = conn_serial("/dev/ttyUSB0", 9600, 1)
    while True:
        dumpOutput(sio)
        sio.write((input("> ")+"\n").encode())
        sio.flush()
        dumpOutput(sio)
    '''
    print(get_cfg(87, "2051c2d21f645e6c"))
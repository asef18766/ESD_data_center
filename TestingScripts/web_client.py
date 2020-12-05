from requests import (
    Session
)
from auth import (
    create_session
)
from config import API_BASE

def download_xml(sess:Session):
    payload = {
        "node_id":["2051c2d21f645e6c"],
        "hids":["deadbeef01"],
        "ts_range":{
            "gt":"",
            "lt":""
        },
        "group":"none",
        "max_record_count":48763
    }
    print("send request")
    with sess.get(f"{API_BASE}/node?operate=download_ss", json=payload) as resp:
        print("receiving response")
        resp.raise_for_status()
        with open("result.xlsx", 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)

if __name__ == "__main__":
    download_xml(create_session("bogay","gg"))
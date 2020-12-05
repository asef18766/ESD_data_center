from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from datetime import (
    datetime
)
from database.schema import (
    DeviceLog
)
class xlsx_file:
    def __init__(self, file_loc:str):
        self.wb = Workbook()
        self.ws:Worksheet = self.wb.active
        self.save_loc = file_loc
    
    def write_line(self, line:list):
        self.ws.append(line)
    
    def save(self):
        self.wb.save(self.save_loc)

def str_to_datetime(str_ts:str)->datetime:
    if str_ts == "":
        return None
    return datetime.strptime(str_ts, "%a %b %d %Y %H:%M:%S %Z%z")

def export_devlog_to_file(records:list, fname:str):
    file = xlsx_file(fname)
    file.write_line(["device", "node", "data", "timestamp"])
    print(f"record length:{len(records)}")
    for rec in records:
        print(f"rec:{rec}")
        rec:DeviceLog
        # shall be substitude to actual name
        hid = rec["device"]
        node = rec["owner"]
        data = rec["data"]
        timestamp = rec["timestamp"].ctime()
        file.write_line([hid, node, data, timestamp])
    file.save()
    
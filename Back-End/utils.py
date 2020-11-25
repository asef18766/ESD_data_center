from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

class xlsx_file:
    def __init__(self, file_loc:str):
        self.wb = Workbook()
        self.ws:Worksheet = self.wb.active
        self.save_loc = file_loc
    
    def write_line(self, line:list):
        self.ws.append(line)
    
    def save(self):
        self.wb.save(self.save_loc)

def export_device_result(hid:str, date ,count:int, fname:str):
    pass
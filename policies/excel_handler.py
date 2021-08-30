import os
import pandas as pd
import openpyxl as op
from pandas import ExcelWriter
from pathlib import Path
from google_drive_api import *


class ExcelHandler():
    def __init__(self):
        self._sheet = pd.DataFrame({'Lám': [''],
                                    'N°Rta': [''],
                                    'N°Loc': [''],
                                    'Loc': [''],
                                    'DQ': [''],
                                    'Det': [''],
                                    'FQ': [''],
                                    '(2)': [''],
                                    'Cont': [''],
                                    'Pop': [''],
                                    'Pje Z': [''],
                                    'CCEE': [''],
                                    'respuesta': [''],
                                    'razon': ['']})
        self._sheet = self._sheet[['Lám', 'N°Rta', 'N°Loc', 'Loc', 'DQ', 'Det', 'FQ', '(2)', 'Cont', 'Pop', 'Pje Z', 'CCEE', 'respuesta', 'razon']]
        self._file_root = None

    def create_excel_sheet(self, nombre: str) -> str:
        self._file_root = str(self.get_project_root()) + \
            os.path.sep + 'files'+os.path.sep + nombre + '.xlsx'
        writer = ExcelWriter(self._file_root)
        self._sheet = self._sheet.to_excel(writer, 'Hoja de datos', index=False)
        writer.save()
        writer.close()
        
    def get_project_root(self) -> Path:
        return Path(__file__).parent.parent

    def upload_data(self, determinantes, contenidos, par, popular, dq, responses, reasons) -> str:
        wb = op.load_workbook(self._file_root)
        ws = wb.get_sheet_by_name('Hoja de datos')
        for lamina in range(3):
            row = str(lamina+2)
            ws['A' + row]=lamina+1
            ws['B' + row]='1'      # Número de respuesta (solo hay una)
            ws['C' + row]='?'
            ws['D' + row]='?'
            ws['E' + row]=dq[lamina]
            ws['F' + row]=(determinantes[lamina])[:-1]
            ws['G' + row]='?'
            ws['H' + row]=par[lamina]
            ws['I' + row]=(contenidos[lamina])[:-1]
            ws['J' + row]=popular[lamina]
            ws['K' + row]='?'
            ws['L' + row]='?'
            ws['M' + row]=responses[lamina]
            ws['N' + row]=reasons[lamina]
        
        wb.save(self._file_root)
        wb.close()         
        upload_file(self._file_root, "1EQ4h-Blfc3PqySXRvViSVrq2ZhCmq2rl")   

        planilla = pd.read_excel(self._file_root)
        print(planilla)

        os.remove(self._file_root)     


    
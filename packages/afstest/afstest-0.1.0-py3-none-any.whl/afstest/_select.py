from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from webui_frame.commons.kdt import Word

attr_list = [attr for attr in dir(Word) if not attr.startswith('_')]
attr_list = sorted(attr_list, key=len)
attr_list.insert(0, 'mark')
attr_list.insert(0, 'name')

excel = "webui_frame/tests/test_conv.xlsx"
wb = load_workbook(excel)
ws = wb.active

dv = DataValidation(type="list", formula1=f'"{",".join(attr_list)}"')
ws.add_data_validation(dv)
dv.add('B2:B20')
wb.save(excel)

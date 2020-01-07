from openpyxl import load_workbook

workbook = load_workbook(filename = 'eval_result.xlsx')
print(workbook.sheetnames)
sheet = workbook.active

sheet_ranges = workbook['추가기사합치기']
print(sheet_ranges['A2'].value)
sheet_ids = sheet_ranges['A']
sheet_values = sheet_ranges['M']
# print(sheet_ids)
# print(sheet_values)
result = {}
print(len(sheet_ids))

sheet_val_none = 0


for idx in range(len(sheet_ids)):
    sheet_val = sheet_values[idx].value
    if sheet_val is None:
        continue
    elif sheet_val is None:
        result[sheet_ids[idx].value] = 4
    elif sheet_val == 'P' or sheet_val == 'p':
        result[sheet_ids[idx].value] = 1
    elif sheet_val == 'N' or sheet_val == 'n':
        result[sheet_ids[idx].value] = 2
    else:
        result[sheet_ids[idx].value] = 3

def get_sheet_value():
    return result

# print(result)

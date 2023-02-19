import xlsxwriter
import pandas as pd
from pandas import ExcelWriter
import os

def createTempAlphabet(headersLen: int):
    alphabet = []
    initialAlphabetRange = 98
    endAlphabetRange = initialAlphabetRange + headersLen
    for i in range(initialAlphabetRange, endAlphabetRange):
        alphabet.append(chr(i).upper())
    return alphabet


def writeWorkSheet(file_path: str, items: list, worksheetname: str, headers: dict):
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet(worksheetname)
    bold = workbook.add_format({'bold': True})
    headerColumnLineNumber = 2
    
    colNames = createTempAlphabet(len(headers))
    for idx, _ in enumerate(headers):
        worksheet.write('{}{}'.format(colNames[idx], headerColumnLineNumber), headers[idx], bold)
    for idx, item in enumerate(items):
        stockList = list(item.values())
        headerColumnLineNumber += 1
        for idx, _ in enumerate(headers):
            worksheet.write('{}{}'.format(colNames[idx], headerColumnLineNumber), stockList[idx])
    workbook.close()


def unionDivsStocksXls():
    divsPandas = pd.DataFrame()
    stocksPandas = pd.DataFrame()
    divsPandas = pd.read_excel('ibkr_report_divs.xls',sheet_name=0)
    stocksPandas = pd.read_excel('ibkr_report_stocks.xls',sheet_name=0)
    
    wb = xlsxwriter.Workbook()
    ws1 = wb.add_worksheet('stocks')
    ws2 = wb.add_worksheet('divs')
    
    with pd.ExcelWriter('ibkr_report_joint.xlsx') as writer:
        divsPandas.to_excel(writer, sheet_name='divs', header=False, index=False)
        stocksPandas.to_excel(writer, sheet_name='stocks', header=False, index=False)
    
    # Remove single xls file
    os.remove('ibkr_report_divs.xls')
    os.remove('ibkr_report_stocks.xls')

            
def main():
    pass


if __name__ == '__main__':
    main()

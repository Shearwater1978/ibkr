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
    headers = [ 'Тип актива', 'Сумма в валюте', 'Сумма в злотых' ]
    
    mainPandas = pd.DataFrame(columns = headers)
    stocksPandas = pd.DataFrame()
    divsIncomePandas = pd.DataFrame()
    stocksPandas = pd.read_excel('ibkr_report_stocks.xls', sheet_name=0, index_col=0, header=1)
    divsIncomePandas = pd.read_excel('ibkr_report_div_income.xls', sheet_name=0, index_col=0, header=1)
    divsTaxPandas = pd.read_excel('ibkr_report_div_tax.xls', sheet_name=0, index_col=0, header=1)
    
    wb = xlsxwriter.Workbook()
    ws0 = wb.add_worksheet('main')
    ws1 = wb.add_worksheet('stocks')
    ws2 = wb.add_worksheet('divsicome')
    ws3 = wb.add_worksheet('divstax')

    mainPandas.at[1, 'Тип актива'] = 'Акции. Доход/Убыток'
    mainPandas.at[1, 'Сумма в валюте'] = round(stocksPandas['ProfitInCurrency'].sum(), 3)
    mainPandas.at[1, 'Сумма в злотых'] = round(stocksPandas['ProfitInPln'].sum(), 3)
    
    mainPandas.at[2, 'Тип актива'] = 'Акции. Комиссия'
    mainPandas.at[2, 'Сумма в валюте'] = round(stocksPandas['TaxInCurrency'].sum(), 3)
    mainPandas.at[2, 'Сумма в злотых'] = round(stocksPandas['TaxInPln'].sum(), 3)
    
    mainPandas.at[3, 'Тип актива'] = 'Дивиденды. Доход'
    mainPandas.at[3, 'Сумма в валюте'] = round(divsIncomePandas['DivInCurrency'].sum(), 3)
    mainPandas.at[3, 'Сумма в злотых'] = round(divsIncomePandas['DivInPln'].sum(), 3)
    
    mainPandas.at[4, 'Тип актива'] = 'Дивиденды. Комиссия'
    mainPandas.at[4, 'Сумма в валюте'] = round(divsTaxPandas['DivTaxInCurrency'].sum(), 3)
    mainPandas.at[4, 'Сумма в злотых'] = round(divsTaxPandas['DivTaxInPln'].sum(), 3)
    
    with pd.ExcelWriter('ibkr_report_joint.xlsx') as writer:
        mainPandas.to_excel(writer, sheet_name='main', index=False)
        stocksPandas.to_excel(writer, sheet_name='stocks', index=False)
        divsIncomePandas.to_excel(writer, sheet_name='divsincome', index=False)
        divsTaxPandas.to_excel(writer, sheet_name='divtax', index=False)
    
    # Remove single xls file
    os.remove('ibkr_report_stocks.xls')
    os.remove('ibkr_report_div_income.xls')
    os.remove('ibkr_report_div_tax.xls')

            
def main():
    pass


if __name__ == '__main__':
    main()

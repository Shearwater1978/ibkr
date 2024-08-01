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
    headers = ['Asset type', 'Amount in currency', 'Amount in pln']

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

    mainPandas.at[1, 'Asset type'] = 'Stocks IB. Profit/Lose'
    mainPandas.at[1, 'Amount in currency'] = round(stocksPandas['ProfitInCurrency'].sum(), 3)
    mainPandas.at[1, 'Amount in pln'] = round(stocksPandas['ProfitInPln'].sum(), 3)

    mainPandas.at[2, 'Asset type'] = 'Stocks IB. Fees'
    mainPandas.at[2, 'Amount in currency'] = round(stocksPandas['TaxInCurrency'].sum(), 3)
    mainPandas.at[2, 'Amount in pln'] = round(stocksPandas['TaxInPln'].sum(), 3)
    
    mainPandas.at[3, 'Asset type'] = 'Dividends IB. Profit'
    mainPandas.at[3, 'Amount in currency'] = round(divsIncomePandas['DivInCurrency'].sum(), 3)
    mainPandas.at[3, 'Amount in pln'] = round(divsIncomePandas['DivInPln'].sum(), 3)

    mainPandas.at[4, 'Asset type'] = 'Dividends IB. Tax'
    mainPandas.at[4, 'Amount in currency'] = round(divsTaxPandas['DivTaxInCurrency'].sum(), 3)
    mainPandas.at[4, 'Amount in pln'] = round(divsTaxPandas['DivTaxInPln'].sum(), 3)

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

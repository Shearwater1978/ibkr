#!/usr/bin/python3
# -*- coding: utf-8 -*-


import csv
import re
import urllib.request
import json
import datetime as dt
from datetime import datetime
from datetime import date as date_new
import sys
import aux_scripts.writer_to_xls as writertoexcell
import aux_scripts.collect_stock_info as stockcalculation
import aux_scripts.collect_divs_income_info as divscalculation
import aux_scripts.collect_divs_tax_info as divtaxcalculation


def getCurrencyExchangeRate(from_date, to_date, currency):
    previous_epoch_year = date_new.today().year - 1
    from_date = date_new(previous_epoch_year, 1, 1)
    to_date = date_new(previous_epoch_year, 12, 31)
    currency_info = {}
    URL = f'http://api.nbp.pl/api/exchangerates/rates/c/{currency}/{from_date}/{to_date}'
    with urllib.request.urlopen(URL) as url:
        data = json.loads(url.read().decode())
        for enum, item in enumerate(data['rates']):
            currency_info[enum] = {}
            currency_info[enum]['effectiveDate'] = item['effectiveDate']
            currency_info[enum]['ask'] = item['ask']
    return (currency_info)


# Move to one day in past, if rate absent to date
def getYesterday(date):
    yesterday = dt.datetime.strptime(date, "%Y-%m-%d").date() - dt.timedelta(days=1)
    return (yesterday.strftime("%Y-%m-%d"))


NOPRINT_TRANS_TABLE = {
    i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
}


def make_printable(s):
    """Replace non-printable characters in a string."""
    # the translate method on str removes characters
    # that map to None from the string
    return s.translate(NOPRINT_TRANS_TABLE)


def find_key(input_dict, value):
    result = None
    for values in input_dict.values():
        if values['effectiveDate'] == value:
            result = values['ask']
            break
    return result


def currency_convert_to_date(currency, date, currencies_bids, currency_index):
    # print('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
    tmp_index = 0
    for item in currency_index:
        if currency == item['currency']:
            tmp_index = item['index']
    tmp_currency_ask_list = currencies_bids[tmp_index][currency]
    for item_data in tmp_currency_ask_list.values():
        if make_printable(date) == make_printable(item_data['effectiveDate']):
            ask = find_key(tmp_currency_ask_list, date)
            return (ask)
    '''
        Detect and hadle situation when date for dividends paid is absent in bank response
    '''
    yesterdayDate = getYesterday(date)
    ask = currency_convert_to_date(currency, yesterdayDate, currencies_bids, currency_index)
    return (ask)


def formationStockFinalReport(rawStocks, currencies_bids, currency_index):
    stockList = []
    for rawStock in rawStocks:
        currency = rawStock['currency']
        date = rawStock['date']
        ask = currency_convert_to_date(currency, date, currencies_bids, currency_index)
        # div_amount_pln = str(round(float(ask) * float(div['div_amount']), 3))
        withholdingtax_pln = round(float(ask) * float(rawStock['withholdingtax']), 3)
        profit_pln = round(float(ask) * float(rawStock['profit']), 3)
        # print('{}: {}: {}:'.format(rawStock['ticker'], rawStock['profit'], profit_pln))
        stockList.append({
            'ticker': rawStock['ticker'], 
            'date': rawStock['date'], 
            'currency': rawStock['currency'],
            'quantity': rawStock['quantity'],
            'withholdingtax': rawStock['withholdingtax'], 
            'withholdingtax_pln': withholdingtax_pln, 
            'profit': rawStock['profit'],
            'profit_pln': profit_pln,
            'order_type': rawStock['order_type'],
            'ask': ask
        })
    return stockList


def formationDivIncomeFinalReport(raw_dividend_list, currencies_bids, currency_index):
    divs_list = []
    for div in raw_dividend_list:
        currency = div['currency']
        date = div['date']
        ask = currency_convert_to_date(currency, date, currencies_bids, currency_index)
        div_amount_pln = round(float(ask) * float(div['div_amount']), 3)
        divs_list.append({'ticker': div['ticker'], 
                          'date': div['date'], 
                          'currency': div['currency'], 
                          'div_amount_in_currency': float(div['div_amount']), 
                          'div_amount_in_pln': div_amount_pln,
                          'ask': ask
                        })
    return (divs_list)


def formationDivTaxFinalReport(raw_dividend_list, currencies_bids, currency_index):
    divs_list = []
    for div in raw_dividend_list:
        currency = div['currency']
        date = div['date']
        ask = currency_convert_to_date(currency, date, currencies_bids, currency_index)
        div_amount_pln = round(float(ask) * float(div['div_tax_amount']), 3)
        divs_list.append({'ticker': div['ticker'], 
                          'date': div['date'], 
                          'currency': div['currency'], 
                          'div_tax_amount_in_currency': float(div['div_tax_amount']), 
                          'div_tax_amount_in_pln': div_amount_pln,
                          'ask': ask
                        })
    return (divs_list)


def getCurrencieBids(currencies):
    previous_epoch_year = date_new.today().year - 1
    from_date = date_new(previous_epoch_year, 1, 1)
    to_date = date_new(previous_epoch_year, 12, 31)
    currencies_bids = []
    for currency in currencies:
        currencies_bids.append({currency: getCurrencyExchangeRate(from_date, to_date, currency)})
    return currencies_bids


def getCurrencyIndex(currencies_bids):
    currency_index = []
    for enum, item in enumerate(currencies_bids):
        for key in item.keys():
            currency_index.append({'currency': key, 'index': enum})
    return currency_index


def main():
    pass


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Input file missed. Abort")
        sys.exit(0)
    else:
        in_file = sys.argv[1]


    # Work with stock
    rawStocks, currencies = stockcalculation.read_input_csv_file('activities_report.csv')
    currencies_bids = getCurrencieBids(currencies)
    currency_index = getCurrencyIndex(currencies_bids)
    stockFinalReport = formationStockFinalReport(rawStocks, currencies_bids, currency_index)
    stockHeaders = ['Ticker', 'Date', 'Currency', 'Quantity', 'TaxInCurrency', 'TaxInPln', 'ProfitInCurrency', 'ProfitInPln', 'OrderType', 'ExchangeRateToDate']
    writertoexcell.writeWorkSheet('ibkr_report_stocks.xls', stockFinalReport, 'stocks', stockHeaders)

    # Work with div income
    rawDivs, currencies = divscalculation.read_input_csv_file('activities_report.csv')
    currencies_bids = getCurrencieBids(currencies)
    currency_index = getCurrencyIndex(currencies_bids)
    divIncomeFinalReport = formationDivIncomeFinalReport(rawDivs, currencies_bids, currency_index)
    divIncomeHeaders = ['Ticker', 'Date', 'Currency', 'DivInCurrency', 'DivInPln', 'ExchangeRateToDate']
    writertoexcell.writeWorkSheet('ibkr_report_div_income.xls', divIncomeFinalReport, 'divincome', divIncomeHeaders)
    
    # Work with div tax
    rawDivsTax, currencies = divtaxcalculation.read_input_csv_file('activities_report.csv')
    currencies_bids = getCurrencieBids(currencies)
    currency_index = getCurrencyIndex(currencies_bids)
    divTaxFinalReport = formationDivTaxFinalReport(rawDivsTax, currencies_bids, currency_index)
    divTaxHeaders = ['Ticker', 'Date', 'Currency', 'DivInCurrency', 'DivInPln', 'ExchangeRateToDate']
    writertoexcell.writeWorkSheet('ibkr_report_div_tax.xls', divTaxFinalReport, 'divincome', divIncomeHeaders)
    
    writertoexcell.unionDivsStocksXls()

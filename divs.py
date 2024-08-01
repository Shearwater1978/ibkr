#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import urllib.request
import json
import datetime as dt
from datetime import datetime
from datetime import date as date_new
import sys
import logging
import os

import aux_scripts.writer_to_xls as writertoexcell
import aux_scripts.collect_stock_info as stockcalculation
import aux_scripts.collect_divs_income_info as divscalculation
import aux_scripts.collect_divs_tax_info as divtaxcalculation


logger = logging.getLogger(__name__)

if os.environ['DIV_LOG_LVL']:
    DEBUG_LVL = str(os.environ['DIV_LOG_LVL']).lower()
    match DEBUG_LVL:
        case "debug":
            FORMAT_INFO = '%(asctime)s - %(message)s'
            logging.basicConfig(format=FORMAT_INFO, level=logging.DEBUG)
        case _:
            FORMAT_INFO = '%(asctime)s - %(levelname)s - %(message)s'
            logging.basicConfig(format=FORMAT_INFO, level=logging.INFO)


def get_currency_exchange_rate(from_date, to_date, currency):
    logger.debug('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
    previous_epoch_year = date_new.today().year - 1
    from_date = date_new(previous_epoch_year, 1, 1)
    to_date = date_new(previous_epoch_year, 12, 31)
    currency_info = {}
    URL = f'http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{from_date}/{to_date}'
    with urllib.request.urlopen(URL) as url:
        data = json.loads(url.read().decode())
        for enum, item in enumerate(data['rates']):
            currency_info[enum] = {}
            currency_info[enum]['effectiveDate'] = item['effectiveDate']
            currency_info[enum]['mid'] = item['mid']
    return currency_info

# Move to one day in past, if rate absent to date
def get_yesterday(date):
    logger.debug('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
    yesterday = dt.datetime.strptime(date, "%Y-%m-%d").date() - dt.timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


NOPRINT_TRANS_TABLE = {
    i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
}


def make_printable(s):
    """Replace non-printable characters in a string."""
    # the translate method on str removes characters
    # that map to None from the string
    logger.debug('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
    return s.translate(NOPRINT_TRANS_TABLE)


def find_key(input_dict, value):
    logger.debug('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
    result = None
    for values in input_dict.values():
        if values['effectiveDate'] == value:
            result = values['mid']
            break
    return result


def currency_convert_to_date(currency, date, currencies_bids, currency_index):
    logger.debug('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
    tmp_index = 0
    for item in currency_index:
        if currency == item['currency']:
            tmp_index = item['index']
    tmp_currency_ask_list = currencies_bids[tmp_index][currency]
    for item_data in tmp_currency_ask_list.values():
        # if make_printable(date) == make_printable(item_data['effectiveDate']):
        if date == item_data['effectiveDate']:
            ask = find_key(tmp_currency_ask_list, date)
            return ask
    '''
        Detect and hadle situation when date for dividends paid is absent in bank response
    '''
    yesterday_date = get_yesterday(date)
    ask = currency_convert_to_date(currency, yesterday_date, currencies_bids, currency_index)
    return ask


def formation_stock_final_report(rawStocks, currencies_bids, currency_index):
    logger.debug('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
    stockList = []
    for rawStock in rawStocks:
        currency = rawStock['currency']
        date = get_yesterday(rawStock['date'])
        ask = currency_convert_to_date(currency, date, currencies_bids, currency_index)
        withholdingtax_pln = round(float(ask) * float(rawStock['withholdingtax']), 3)
        profit_pln = round(float(ask) * float(rawStock['profit']), 3)
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


def formation_div_income_final_report(raw_dividend_list, currencies_bids, currency_index):
    logger.debug('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
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
    return divs_list


def formation_div_tax_final_report(raw_dividend_list, currencies_bids, currency_index):
    logger.debug('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
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
    return divs_list


def get_currencie_bids(currencies):
    logger.debug('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
    previous_epoch_year = date_new.today().year - 1
    from_date = date_new(previous_epoch_year, 1, 1)
    to_date = date_new(previous_epoch_year, 12, 31)
    currencies_bids = []
    for currency in currencies:
        currencies_bids.append({currency: get_currency_exchange_rate(from_date, to_date, currency)})
    return currencies_bids


def get_currency_index(currencies_bids):
    logger.debug('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
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
    MSG_START = 'Start calculate Stocks'
    logger.info(MSG_START)
    rawStocks, currencies = stockcalculation.read_input_csv_file(in_file)
    currencies_bids = get_currencie_bids(currencies)
    currency_index = get_currency_index(currencies_bids)
    stockFinalReport = formation_stock_final_report(rawStocks, currencies_bids, currency_index)
    stockHeaders = [
        'Ticker',
        'Date',
        'Currency',
        'Quantity',
        'TaxInCurrency',
        'TaxInPln',
        'ProfitInCurrency',
        'ProfitInPln',
        'OrderType',
        'ExchangeRateToDate'
    ]
    MSG_RESULT = 'Start writting to ibkr_report_stocks.xls'
    logger.info(MSG_RESULT)
    try:
        writertoexcell.writeWorkSheet(
            'ibkr_report_stocks.xls',
            stockFinalReport,
            'stocks',
            stockHeaders
        )
        MSG_SUCCESS = 'File ibkr_report_stocks.xls was written successfully.'
        logger.info(MSG_SUCCESS)
    except Error as e:
        MSG_ERROR = f'File ibkr_report_stocks.xls was written with error {e}.'
        logger.error(MSG_ERROR)

    # Work with div income
    MSG_START = 'Start calculate Div income'
    logger.info(MSG_START)
    rawDivs, currencies = divscalculation.read_input_csv_file(in_file)
    currencies_bids = get_currencie_bids(currencies)
    currency_index = get_currency_index(currencies_bids)
    divIncomeFinalReport = formation_div_income_final_report(rawDivs, currencies_bids, currency_index)
    divIncomeHeaders = [
        'Ticker',
        'Date',
        'Currency',
        'DivInCurrency',
        'DivInPln',
        'ExchangeRateToDate'
    ]
    MSG_RESULT = 'Start writting to ibkr_report_div_income.xls'
    logger.info(MSG_RESULT)
    try:
        writertoexcell.writeWorkSheet(
            'ibkr_report_div_income.xls',
            divIncomeFinalReport,
            'divincome',
            divIncomeHeaders
        )
        MSG_SUCCESS = 'File ibkr_report_div_income.xls was written successfully.'
        logger.info(MSG_SUCCESS)
    except Error as e:
        MSG_ERROR = f'File ibkr_report_div_income.xls was written with error {e}.'
        logger.error(MSG_ERROR)

    # Work with div tax
    MSG_START = 'Start calculate Div tax'
    logger.info(MSG_START)
    rawDivsTax, currencies = divtaxcalculation.read_input_csv_file(in_file)
    currencies_bids = get_currencie_bids(currencies)
    currency_index = get_currency_index(currencies_bids)
    divTaxFinalReport = formation_div_tax_final_report(
        rawDivsTax,
        currencies_bids,
        currency_index
    )
    divTaxHeaders = [
        'Ticker',
        'Date',
        'Currency',
        'DivTaxInCurrency',
        'DivTaxInPln',
        'ExchangeRateToDate'
    ]
    MSG_START = 'Start writting to ibkr_report_div_tax.xls'
    logger.info(MSG_START)
    try:
        writertoexcell.writeWorkSheet(
            'ibkr_report_div_tax.xls',
            divTaxFinalReport,
            'divincome',
            divTaxHeaders
        )
        MSG_SUCCESS = 'File ibkr_report_div_tax.xls was written successfully.'
        logger.info(MSG_SUCCESS)
    except Error as e:
        MSG_ERROR = f'File ibkr_report_div_tax.xls was written with error {e}.'
        logger.error(MSG_ERROR)

    # Agregate all xls files into one
    MSG_START = 'Start writting final report'
    logger.info(MSG_START)
    writertoexcell.unionDivsStocksXls()

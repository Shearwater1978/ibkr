#!/usr/bin/python3
# -*- coding: utf-8 -*-


import csv
import re
from typing import Pattern
import urllib.request, json
import datetime as dt
from datetime import datetime
import sys
import hashlib


def get_currency_price(from_date, to_date, currency):
    currency_info = {}
    URL = f'http://api.nbp.pl/api/exchangerates/rates/c/%s/%s/%s' %(currency, from_date, to_date)
    # print(URL)
    with urllib.request.urlopen(URL) as url:
        data = json.loads(url.read().decode())
        for enum, item in enumerate(data['rates']):
            currency_info[enum] = {}
            currency_info[enum]['effectiveDate'] = item['effectiveDate']
            # currency_info[enum]['currency'] = currency
            currency_info[enum]['ask'] = item['ask']
    return(currency_info)


# Move to one day in past, if rate absent to date
def get_yesterday(date):
    yesterday = dt.datetime.strptime(date, "%Y-%m-%d").date() - dt.timedelta(days=1)
    return(yesterday.strftime("%Y-%m-%d"))


# Read Dividends report file and fill temp array with Ticker, Div amounts and Divs payment date, Currency 
def csv_read_2023(infile):
    with open(in_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        currencies = []
        raw_divs_list = []
        for row in reader:
            if re.match('Period', str(row[2])):
                '''
                    Parse string with Data range of report
                    Statement,Data,Period,"January 1, 2022 - December 31, 2022"
                    date_string_to_split: extract Data range in format "January 1, 2022 - December 31, 2022"
                    from_date_raw: extract period start date in format "January 1, 2022"
                    to_date: extract period end date in format "December 31, 2022"
                    from_date,to_date: formatting data into format "2022-01-01"/"2022-12-31"
                '''
                date_string_to_split = str(row[3])
                from_date_raw = date_string_to_split.split('-')[0].strip()
                to_date_raw = date_string_to_split.split('-')[1].lstrip()
                from_date = datetime.strptime(from_date_raw, '%B %d, %Y').date().strftime('%Y-%m-%d')
                to_date = datetime.strptime(to_date_raw, '%B %d, %Y').date().strftime('%Y-%m-%d')
            if not re.match('Total', str(row[2])):
                '''
                    Read Reports line by line and add each record about Dividends into list of dictionaries
                '''
                if str(row[0]) == "Dividends" and str(row[1]) != "Header":
                    date = row[3]
                    currency = row[2].lower()
                    div_amount = row[-2]
                    ticker = row[-3].split()[0].split('(')[0]
                    if currency not in currencies:
                        currencies.append(currency)
                    raw_divs_list.append({'ticker': ticker, 'date': date, 'currency': currency, 'div_amount': div_amount})
    return(raw_divs_list, from_date, to_date, currencies)


NOPRINT_TRANS_TABLE = {
    i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
}
def make_printable(s):
    """Replace non-printable characters in a string."""
    # the translate method on str removes characters
    # that map to None from the string
    return s.translate(NOPRINT_TRANS_TABLE)


def get_yesterday(date):
    yesterday = dt.datetime.strptime(date, "%Y-%m-%d").date() - dt.timedelta(days=1)
    return(yesterday.strftime("%Y-%m-%d"))


def currency_convert_to_date(currency, date, currencies_bids, currency_index):
    # print('Called function {message}'.format(message=sys._getframe(0).f_code.co_name))
    tmp_index = 0
    for item in currency_index:
        if currency == item['currency']:
            tmp_index = item['index']
    tmp_currency_ask_list = currencies_bids[tmp_index][currency]
    for item_id, item_data in tmp_currency_ask_list.items():
        for key in item_data:
            if make_printable(date) == make_printable(item_data['effectiveDate']):
                ask = item_data['ask']
                return(ask)
    '''
        Detect and hadle situation when date for dividends paid is absent in bank response
    '''
    yesterdayDate = get_yesterday(date)
    ask = currency_convert_to_date(currency, yesterdayDate, currencies_bids, currency_index)
    return(ask)


def formation_final_report(raw_dividend_list, currencies_bids, currency_index):
    divs_list = []
    for enum, div in enumerate(raw_dividend_list):
        if enum == 999:
            break
        currency = div['currency']
        date = div['date']
        div_amount_pln = str(round(float(currency_convert_to_date(currency, date, currencies_bids, currency_index)) * float(div['div_amount']),3))
        divs_list.append({'ticker': div['ticker'], 'date': div['date'], 'currency': div['currency'], 'div_amount_in_currency': div['div_amount'], 'div_amount_in_pln': div_amount_pln})
    return(divs_list)


def main():
    pass


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Input file missed. Abort")
        sys.exit(0)
    else:
        in_file = sys.argv[1]

    # Reading Report and get list of all dividends, and two date of boundaries for Report
    raw_divs_list, from_date, to_date, currencies = csv_read_2023(in_file)

    # Loading the selling rate for each currency found in the report
    currencies_bids = []
    currency_index = []
    for currency in currencies:
        currencies_bids.append({currency: get_currency_price(from_date, to_date, currency)})
        # # Debug output currencies result list
        # for item_id, item_data in currencies_bids.items():
        #     print('\nid:', item_id)
        #     for key in item_data:
        #         print(key + ":", item_data[key])
    for enum, item in enumerate(currencies_bids):
        for key in item.keys():
            currency_index.append({'currency': key, 'index': enum})
    print(formation_final_report(raw_divs_list, currencies_bids, currency_index))
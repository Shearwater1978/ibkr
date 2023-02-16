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


def get_currency_price(from_date, to_date, currency):
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
def get_yesterday(date):
    yesterday = dt.datetime.strptime(date, "%Y-%m-%d").date() - dt.timedelta(days=1)
    print(f'yesterday: {yesterday}')
    return (yesterday.strftime("%Y-%m-%d"))


# Read Dividends report file and fill temp array with Ticker, Div amounts and Divs payment date, Currency
def read_input_csv_file(infile):
    previous_epoch_year = date_new.today().year - 1
    from_date = date_new(previous_epoch_year, 1, 1)
    to_date = date_new(previous_epoch_year, 12, 31)
    with open(in_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        currencies = []
        raw_divs_list = []
        for row in reader:
            if not re.match('Total', str(row[2])):
                '''
                    Read Reports line by line and add each record about Dividends into list of dictionaries
                    DividendDetail,Data,RevenueComponent,USD,WFC,10375,US,20221201,20221103,,Ordinary Dividend,Qualified - Meets Holding Period,1.8,1.8,1.8,-0.27,-0.27,-0.27,
                '''
                if str(row[0]) == "DividendDetail" and str(row[2]) == "Summary":
                    currency = row[3].lower()
                    ticker = row[4]
                    date_raw = row[7]
                    date = datetime.strptime(date_raw, "%Y%m%d").date().strftime('%Y-%m-%d')
                    div_amount = row[12]
                    withholdingtax = abs(float(row[15]))
                    if currency not in currencies:
                        currencies.append(currency)
                    raw_divs_list.append({'ticker': ticker, 'date': date, 'currency': currency, 'div_amount': div_amount, "withholdingtax": withholdingtax})
    return (raw_divs_list, from_date, to_date, currencies)


NOPRINT_TRANS_TABLE = {
    i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
}


def make_printable(s):
    """Replace non-printable characters in a string."""
    # the translate method on str removes characters
    # that map to None from the string
    return s.translate(NOPRINT_TRANS_TABLE)


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
            else:
                ask = item_data['ask']
            return (ask)
    '''
        Detect and hadle situation when date for dividends paid is absent in bank response
    '''
    yesterdayDate = get_yesterday(date)
    ask = currency_convert_to_date(currency, yesterdayDate, currencies_bids, currency_index)
    return (ask)


def formation_final_report(raw_dividend_list, currencies_bids, currency_index):
    divs_list = []
    for enum, div in enumerate(raw_dividend_list):
        currency = div['currency']
        date = div['date']
        ask = currency_convert_to_date(currency, date, currencies_bids, currency_index)
        # div_amount_pln = str(round(float(currency_convert_to_date(currency, date, currencies_bids, currency_index)) * float(div['div_amount']), 3))
        div_amount_pln = str(round(float(ask) * float(div['div_amount']), 3))
        withholdingtax_pln = str(round(float(currency_convert_to_date(currency, date, currencies_bids, currency_index)) * float(div['withholdingtax']), 3))
        divs_list.append({'ticker': div['ticker'], 'date': div['date'], 'currency': div['currency'], 'div_amount_in_currency': div['div_amount'], 'div_amount_in_pln': div_amount_pln, 'withholdingtax': div['withholdingtax'], 'withholdingtax_pln': withholdingtax_pln, 'ask': ask})
        print(div['ticker'], div['date'], ask)
        if enum == 5:
            sys.exit(0)
    return (divs_list)


def writing_to_csv(divs, divs_csv_filename):
    csv_headers = ['Ticket', 'Date', 'Currency', 'DivInCurrency', 'DivInPln', 'TaxInCurrency', 'TaxInPln']
    div_content = []
    with open(divs_csv_filename, "w") as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(csv_headers)
        for div in divs:
            w = csv.DictWriter(f, div.keys(), delimiter=';')
            w.writerow(div)


def main():
    pass


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("Input file missed. Abort")
        sys.exit(0)
    else:
        in_file = sys.argv[1]
        divs_csv_filename = sys.argv[2]

    # Reading Report and get list of all dividends, and two date of boundaries for Report
    raw_divs_list, from_date, to_date, currencies = read_input_csv_file(in_file)

    # Loading the selling rate for each currency found in the report
    currencies_bids = []
    currency_index = []
    for currency in currencies:
        currencies_bids.append({currency: get_currency_price(from_date, to_date, currency)})

    for enum, item in enumerate(currencies_bids):
        for key in item.keys():
            currency_index.append({'currency': key, 'index': enum})

    divs_final = formation_final_report(raw_divs_list, currencies_bids, currency_index)
    writing_to_csv(divs_final, divs_csv_filename)

#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import csv
import re
from typing import Pattern
import urllib.request, json
import datetime as dt
from datetime import datetime

def get_currency_price(from_date, to_date):
    currency_info = {}
    URL = f'http://api.nbp.pl/api/exchangerates/rates/c/usd/%s/%s' %(from_date, to_date)
    with urllib.request.urlopen(URL) as url:
        data = json.loads(url.read().decode())
        for item in data['rates']:
            effectiveDate = item['effectiveDate']
            bid = item['bid']
            ask = item['ask']
            currency_info[effectiveDate] = {'bid': bid, 'ask': ask}
    return(currency_info)

def get_date_range(skip_lines):
    from_date = ''
    to_date = ''
    tmp_date = ''
    dates = []
    pattern = r'^[0-9]{4}-[0-9]{2}-[0-9]{2}\b'
    with open('data.txt','r') as csvfile:
        reader = csv.reader(csvfile)
        for i in range (0, skip_lines):
            next(reader)
        for row in reader:
            tmp_date = str(row[3])
            if row[0] == 'Dividends':
                if row[1] == 'Data':
                    if row[2] != 'Total':   
                        if re.findall(pattern, str(row[3])):
                            dates.append(datetime.strptime(tmp_date, '%Y-%m-%d').date())
    sorteddates = [datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
    uniquedates = list(dict.fromkeys(sorteddates))
    from_date = uniquedates[0]
    to_date = uniquedates[-1]
    return(from_date, to_date)

def csv_get_stmnt():
    match_count = 0
    pattern = '^Statement'
    with open('data.txt','r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            check_line = str(line[0])
            if re.findall(pattern, check_line):
                match_count += 1
    return(match_count)

def get_yesterday(date):
    yesterday = dt.datetime.strptime(date, "%Y-%m-%d").date() - dt.timedelta(days=1)
    return(yesterday.strftime("%Y-%m-%d"))

def currency_to_actual_date(date,currency_to_date_interval):
    currency_array = currency_to_date_interval
    kurs_on_the_actual_date = currency_array.get(date, {}).get('ask')
    if kurs_on_the_actual_date != None:
        print("On the date >%s< bank course is >%s<" % (date,kurs_on_the_actual_date))
        return kurs_on_the_actual_date
    else:
        yesterday = get_yesterday(date)
        currency_to_actual_date(yesterday,currency_to_date_interval)

def csv_read(skip_lines,currency_to_date_interval):
    currency_date_array = currency_to_date_interval
    with open('data.txt', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i in range (0, skip_lines+1):
            next(reader)
        for row in reader:
            if str(row[2]) != "Total":
                if str(row[0]) == "Dividends" and str(row[1]) != "Header" and row[-3].split()[0].split('(')[0]=="T":
                    date = row[3]
                    currency = row[2]
                    div_amount = row[-2]
                    ticker = row[-3].split()[0].split('(')[0]
                    cur_ask = currency_date_array.get(date, {}).get('ask')
                    currency_current = currency_to_actual_date(date,currency_to_date_interval)
                    print(ticker,date,div_amount,currency_current,cur_ask)
                    #print(f'Ticker: %s, Currency: %s, Date: %s, Dividends(USD): %s, Dividends(PLN): %s' %(ticker,currency,date,div_amount,cur_ask))

def main():
    print('main')

if __name__ == '__main__':
    skip_lines = csv_get_stmnt()
    from_date, to_date = get_date_range(skip_lines)
    csv_read(skip_lines,get_currency_price(from_date, to_date))
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import re
from typing import Pattern
import urllib.request, json
import datetime as dt
from datetime import datetime
import sys

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

def get_date_range(in_file,skip_lines):
    from_date = ''
    to_date = ''
    tmp_date = ''
    dates = []
    pattern = r'^[0-9]{4}-[0-9]{2}-[0-9]{2}\b'
    with open(in_file,'r') as csvfile:
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

# Get lines count for skip when getting didivends
def csv_get_stmnt(in_file):
    match_count = 0
    pat_list = ['StatementHeader','StatementData','DividendsHeader']
    pat = re.compile('|'.join(pat_list))
    with open(in_file,'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if pat.match(line[0]+line[1]):
                match_count += 1
    return(match_count)

# Move to one day in past, if rate absent to date
def get_yesterday(date):
    yesterday = dt.datetime.strptime(date, "%Y-%m-%d").date() - dt.timedelta(days=1)
    return(yesterday.strftime("%Y-%m-%d"))

def currency_to_actual_date(date,currency_to_date_interval):
    kurs_on_the_actual_date = currency_to_date_interval.get(date, {}).get('ask')
    if kurs_on_the_actual_date == None:
        kurs_on_the_actual_date = currency_to_actual_date(get_yesterday(date),currency_to_date_interval)
    return kurs_on_the_actual_date

# Read Dividends report file and fill temp array with Ticker, Div amounts and Divs payment date, Currency 
def csv_read_2023(infile):
    raw_divs_list = []
    with open(in_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
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
                if str(row[0]) == "Dividends" and str(row[1]) != "Header":
                    date = row[3]
                    currency = row[2].lower()
                    div_amount = row[-2]
                    ticker = row[-3].split()[0].split('(')[0]
                    raw_divs_list.append({'ticker': ticker, 'date': date, 'currency': currency, 'div_amount': div_amount})
    return(raw_divs_list, from_date, to_date)


# def csv_read(in_file,skip_lines,currency_to_date_interval):
#     currency_date_array = currency_to_date_interval
#     with open(in_file, newline='') as csvfile:
#         reader = csv.reader(csvfile)
#         for i in range (0, skip_lines+1):
#             next(reader)
#         print("Ticker;Date;Dividends(USD);Dividends(PLN);Rate(PLN-USD)")
#         for row in reader:
#             if str(row[2]) != "Total":
#                 if str(row[0]) == "Dividends" and str(row[1]) != "Header":
#                     date = row[3]
#                     currency = row[2]
#                     div_amount = row[-2]
#                     ticker = row[-3].split()[0].split('(')[0]
#                     cur_ask = currency_date_array.get(date, {}).get('ask')
#                     currency_current = round(currency_to_actual_date(date,currency_to_date_interval),3)
#                     print(f'%s;%s;%s;%s;%s' %(ticker,date,div_amount,round(float(currency_current)*float(div_amount),2),currency_current))
                    
def main():
    pass

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Input file missed. Abort")
        sys.exit(0)
    else:
        in_file = sys.argv[1]
    # skip_lines = csv_get_stmnt(in_file)
    # from_date, to_date = get_date_range(in_file,skip_lines)
    # csv_read(in_file,skip_lines,get_currency_price(from_date, to_date))
    # Reading Report and get list of all dividends, and two date of boundaries for Report
    raw_divs_list, from_date, to_date = csv_read_2023(in_file)


import re
import csv
from datetime import date as date_new


def read_input_csv_file(in_file):
    previous_epoch_year = date_new.today().year - 1
    from_date = date_new(previous_epoch_year, 1, 1)
    to_date = date_new(previous_epoch_year, 12, 31)
    
    dataRegexp = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    tickerRegexp = r"^.*?(?=\()"
    with open(in_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        currencies = []
        raw_divs_list = []
        for row in reader:
            if row[0] == 'Dividends' and not re.match(r'Total', row[2]) and (not row[3] is None):
                if row[1] != 'Header':
                    ticker = str(re.search(tickerRegexp, row[4]).group(0)).strip()
                    currency = row[2].lower()
                    date = row[3]
                    div_amount = row[5]
                    if currency not in currencies:
                        currencies.append(currency)
                    raw_divs_list.append({
                        'ticker': ticker,
                        'date': date,
                        'currency': currency,
                        'div_amount': div_amount
                    })
    return (raw_divs_list, from_date, to_date, currencies)


def main():
    raw_divs_list, from_date, to_date, currencies = read_input_csv_file('activities_report.csv')
    print(raw_divs_list)

if __name__ == '__main__':
    main()

import re
import csv
from datetime import date as date_new


def read_input_csv_file(in_file):
    dataRegexp = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    tickerRegexp = r"^.*?(?=\()"
    with open(in_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        currencies = []
        divsIncomeArray = []
        for row in reader:
            if row[2] == "Period":
                report_date = re.search(r"[0-9]{4}", row[3])[0]
            if row[0] == 'Dividends' and not re.match(r'Total', row[2]) and (not row[3] is None):
                if row[1] != 'Header':
                    if str(re.search(r"[0-9]{4}", row[3])[0]) == str(report_date):
                        ticker = str(re.search(tickerRegexp, row[4]).group(0)).strip()
                        currency = row[2].lower()
                        date = row[3]
                        div_amount = row[5]
                        if currency not in currencies:
                            currencies.append(currency)
                        divsIncomeArray.append({
                            'ticker': ticker,
                            'date': date,
                            'currency': currency,
                            'div_amount': float(div_amount)
                        })
    return divsIncomeArray, currencies


def main():
    divsIncomeArray, currencies = read_input_csv_file('activities_report.csv')
    print(raw_divs_list)


if __name__ == '__main__':
    main()

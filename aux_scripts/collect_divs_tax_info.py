import re
import csv


def read_input_csv_file(in_file):
    dataRegexp = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    tickerRegexp = r"^.*?(?=\()"
    with open(in_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        currencies = []
        divTaxArray = []
        reader = csv.reader(csvfile)

        for row in reader:
            if row[2] == "Period":
                report_date = re.search(r"[0-9]{4}", row[3])[0]
            if row[0] == 'Withholding Tax' and not re.match(r'Total', row[2]) and (not row[3] is None):
                if row[1] != 'Header':
                    if str(re.search(r"[0-9]{4}", row[3])[0]) == str(report_date):
                        ticker = str(re.search(tickerRegexp, row[4]).group(0)).strip()
                        currency = row[2].lower()
                        date = row[3]
                        div_tax_amount = row[5]
                        if currency not in currencies:
                            currencies.append(currency)
                        divTaxArray.append({
                            'ticker': ticker,
                            'date': date,
                            'currency': currency,
                            'div_tax_amount': float(div_tax_amount) * -1
                        })
    return (divTaxArray, currencies)


def main():
    divTaxArray, currencies = read_input_csv_file('activities_report.csv')
    print(divTaxArray)


if __name__ == '__main__':
    main()

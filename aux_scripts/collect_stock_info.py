import re
import csv


def removeTimeFromDate(rawRecord):
    dataRegexp = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    result = re.match(dataRegexp, rawRecord)[0]
    return result


def transformDataField(rawRecordWithQuotas):
    '''
        Each evaluated record is matched by the next rules:
            Number of field | Name field | Values
            0. Trades: Trades
            1. Header: Data
            2. DataDiscriminator: Order
            3. Asset Category: Stocks
            4. Currency: USD
            5. Symbol: LUMN
            6. Date/Time: 2022-08-26
            7. Quantity: -11
            8. T. Price: 10.92
            9. C. Price: 10.76
            10. Proceeds: 120.12
            11. Comm/Fee: -1.004180748
            12. Basis: -140.03145
            13. Realized P/L: -20.91563
            14. MTM P/L: 1.76
            15. Code: C
    '''
    removedTimeFromDataField = removeTimeFromDate(rawRecordWithQuotas)
    result = re.sub(r"\"", '', removedTimeFromDataField)
    return result


def read_input_csv_file(in_file):
    stocksArray = []
    with open(in_file, newline='') as csvfile:
        readerRows = csv.reader(csvfile)
        for readRow in readerRows:
            if re.match('Trades', str(readRow[0])) and (re.match('O', str(readRow[15])) or re.match('C', str(readRow[15]))):
                if re.match('Data', str(readRow[1])):
                    readRow[6] = transformDataField(readRow[6])
                    stocksArray.append({
                        'ticker': readRow[5],
                        'currency': readRow[4],
                        'date': readRow[6],
                        'quantity': readRow[7],
                        'withholdingtax': abs(float(readRow[11])),
                        'profit': abs(float(readRow[13])),
                        'order_type': readRow[15]
                    })
    return stocksArray


def main():
    collectStockTrades = read_input_csv_file('activities_report.csv')
    return collectStockTrades


if __name__ == '__main__':
    main()

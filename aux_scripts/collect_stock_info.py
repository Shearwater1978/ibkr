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
    print(removedTimeFromDataField)
    return result


def read_input_csv_file(in_file):
    stocksArray = []
    with open(in_file, newline='') as csvfile:
        readerRows = csv.reader(csvfile)
        for readRow in readerRows:
            if re.match('Trades', str(readRow[0])) and (re.match('O', str(readRow[15])) or re.match('C', str(readRow[15]))):
                if re.match('Data', str(readRow[1])):
                    # pass
                    readRow[6] = transformDataField(readRow[6])
                    print(readRow)
                    stocksArray.append({
                        'ticker': readRow[5],
                        'currency': readRow[4],
                        'date': readRow[6],
                        'withholdingtax': abs(float(readRow[11])),
                        'profit': abs(float(readRow[13])),
                        'order_type': readRow[15]
                    })
                    # print(transformDataField(row))
    #             '''
    #                 Read Reports line by line and add each record about Dividends into list of dictionaries
    #                 DividendDetail,Data,RevenueComponent,USD,WFC,10375,US,20221201,20221103,,Ordinary Dividend,Qualified - Meets Holding Period,1.8,1.8,1.8,-0.27,-0.27,-0.27,
    #             '''
    #             if str(row[0]) == "DividendDetail" and str(row[2]) == "Summary":
    #                 currency = row[3].lower()
    #                 ticker = row[4]
    #                 date_raw = row[7]
    #                 date = datetime.strptime(date_raw, "%Y%m%d").date().strftime('%Y-%m-%d')
    #                 div_amount = row[12]
    #                 withholdingtax = abs(float(row[15]))
    #                 if currency not in currencies:
    #                     currencies.append(currency)
    #                 raw_divs_list.append({'ticker': ticker, 
    #                                       'date': date, 
    #                                       'currency': currency, 
    #                                       'div_amount': div_amount, 
    #                                       "withholdingtax": withholdingtax
    #                                     })
    return (stocksArray)


def main():
    collectStockTrades = read_input_csv_file('activities_report.csv')
    print(collectStockTrades)
    # rawRecordLine = 'Trades,Data,Order,Stocks,USD,MSFT,"2022-09-01, 10:48:07",-1,256.065,260.4,256.065,-1.005993888,-244.61,10.449006,-4.335,C'
    # rawRecordLine = 'Trades,Data,Order,Stocks,USD,KR,"2022-04-21, 10:37:15",2,57.538,58.18,-115.076,-1,116.076,0,1.284,O'
    # print(transformDataField(rawRecordLine))


if __name__ == '__main__':
    main()
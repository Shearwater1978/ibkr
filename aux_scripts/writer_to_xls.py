import xlsxwriter


def createTempAlphabet(headersLen: int):
    alphabet = []
    initialAlphabetRange = 98
    endAlphabetRange = initialAlphabetRange + headersLen
    for i in range(initialAlphabetRange, endAlphabetRange):
        alphabet.append(chr(i).upper())
    return alphabet


def writeWorkSheet(file_path: str, items: list, worksheetname: str, headers: dict):
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet(worksheetname)
    bold = workbook.add_format({'bold': True})
    headerColumnLineNumber = 2
    
    colNames = createTempAlphabet(len(headers))
    for idx, _ in enumerate(headers):
        worksheet.write('{}{}'.format(colNames[idx], headerColumnLineNumber), headers[idx], bold)
    for idx, item in enumerate(items):
        stockList = list(item.values())
        headerColumnLineNumber += 1
        for idx, _ in enumerate(headers):
            worksheet.write('{}{}'.format(colNames[idx], headerColumnLineNumber), stockList[idx])    
    workbook.close()

            
def main():
    pass


if __name__ == '__main__':
    main()

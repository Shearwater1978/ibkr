[![Build Status](https://app.travis-ci.com/Uglykoyote/ibkr.svg?branch=main)](https://app.travis-ci.com/Uglykoyote/ibkr)
# ibkr
In the actual stage, this code provides the ability to convert dividends from original currencies to PLN.

How-to:
1. Get a special dividend report
2. Execute Python script

How to set up dividends report:
1. Log in into IBKR account
2. Open section "Performance & Report"
3. Select "Tax Documents"
4. Select a Tax Year
5. Click the button " CSV" next to the line "Dividend Report"

How to run the process of calculating dividends in PLN:
1. Download the created report into the directory with the Python script
2. Execute script with command: python3 ./app/divs.py Uxxxxx.YYYY.dividends.csv

Enjoy!

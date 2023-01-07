# ibkr
On actual stage this code provide ability for convert dividens from original currencies to PLN.

How-to:
1. Get special dividend report
2. Execute Python script

How to set-up dividends report:
1. Log-in into IBKR account
2. Open section "Performance & Report"
3. Select "Statements"
4. Click "+" link in section "Custom Statements"
5. Fill fields:
  - Statement Name: Your name for the Report
  - Statement Type: From dropdown menu select "Activity"
6. Select fields below:
  - Dividiend
  - Payment in Lieu of Dividends
7. In section "Section Configurations" set switches in the positions:
  - Profit and Loss: "MTM and Realized P/L"
  - Breakout Positions into Long and Short? - No
  - Combine by Underlying (MTD/YTD only)? - No
  - Display Canceled Trades? - No
  - Group Buys and Sells per Symbol in Trades Section? - No
  - Hide Details for Positions, Trades and Client Fees Sections? - Yes
  - Replace Account ID with Account Alias? - No
  - Display Mailing Address in Account Information Section? - No
8. In section "Delivery Configuration" set switches in the positions:
  - Format: CSV
  - Period: Daily
  - Language: English

How to formation&download dividends report:
1. Log-in into IBKR account
2. Open section "Performance & Report"
3. Select "Statements"
4. Click arrow "Right" opposite the previously created report
5. In newly pop-up window set accordingly switches:
  - Period: Custom date range
  - Set Date range within 2 field From Date & To Date accordinly
  - Format: CSV
  - Languge: Check that language English is selected
6. Push the button "Run" and wait. It can take a lot of time. It depends on the count of records for dividends.

How to run process of calculating dividends in PLN:
1. Download created report into directory with Python script
2. Execute script with command: python3 divs.py report.csv

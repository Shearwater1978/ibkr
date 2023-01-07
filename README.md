# ibkr
On initial stage current code provide ability for convert dividens from original currency to PLN.

How-to:
1. Get special dividend report
2. Execute Python script

How to get dividends report:
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

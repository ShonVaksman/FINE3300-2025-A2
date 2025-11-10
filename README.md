# FINE3300-2025-A2
The purpose of the following code is to create a method that will calculate the loan amortization and payment schedule of a mortgage (shown in graphs and excel) and using Python to analyze Canada’s 2024 Consumer Price Index (CPI) data across provinces to measure inflation, compare price changes, and evaluate real/nominal wages.

Part A -- Loan Amortization and Payment Schedule
Expand the MortgagePayment class (from Assignment 1)

**Input:**
-Principal amount
-Quoted Annual Interest Rate
-Amortization In # of Years
-Mortgage Term (Years)

E.g.,
Enter Mortgage Principal (e.g., 80,000): 80000
Enter Quoted Annual Interest Rate % (e.g., 4.2): 4.2
Enter Amortization In # of Years (e.g., 20): 20
Enter Mortgage Term (years): 15


**Output:**
-Determine payment for each period type (output)
E.g.,

PAYMENT AMOUNTS:

Monthly Payment: $491.71
Semi-monthly Payment: $245.64
Bi-weekly Payment: $226.73
Weekly Payment: $113.32
Rapid Bi-weekly Payment: $245.86
Rapid Weekly Payment: $122.93
Part B -- Consumer Price Index

-Saves all data frames into a single Excel Workbook ("Loan_Payment_Schedule.xlsx) 
*each data fram includes period, starting balance, interest amount, payment, and ending balance*

-Generate a Matplotlib (Loan_Balance_Decline.png) showing the loan balance decline across all six payment types with legends

PART B - Consumer Price Index (CPI Analysis)
*use CPI data files for 10 provinces and Canada overall to answer the following questions*

**Input:** 
1. Combine the 11 data frames into one data frame with column headings: Item, Month, Jurisdiction,
CPI.
2. Print the first 12 lines of your new data frame
3. For Canada and each of the provinces, report the average month-to-month change in food, shelter,
All-items excluding food and energy. Report your numbers as a percent up to one decimal place.
4. Which province experienced the highest average change in the above categories?
5. Using the All-items CPI number, what would be the equivalent salary to $100,000 received in Ontario
in all other provinces (as at December 2024)?
6. Read the MinimumWages.csv file. On a nominal basis, which province has the highest minimum
wage? Which province has the lowest minimum wage? Using the CPI numbers for December 2024,
determine the province with the highest real minimum wage?
7. Compute the annual change in CPI for services across Canada and all provinces. Report your numbers
as a percent up to one decimal place.
8. Which region experienced the highest inflation in services?

**Output:**
All answers are displayed in the terminal as formatted tables and percentages (rounded to one decimal).
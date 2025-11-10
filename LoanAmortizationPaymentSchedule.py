import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

#Print objective of the code
print ("----- Mortgage Payment Calculator -----")
print ("   ")

#Design a class to calculate a variety of payment methods
class MortgagePayment:

    #Design method for the quoted (semiannual) interest rate and amortized period 
    def __init__(self, semiCompoundRates, amortPeriod):

        #Store the semiannual compounded rates and the number of amortized years
        self.__semiCompoundRates = semiCompoundRates
        self.__amortPeriod = amortPeriod

    #Design method to calculate the periodic interest rate for a given number of payments 
    def periodicIR (self, annualPayments):

        #Convert interest rate with semi-annual compounding to the Effective Annual Rate 
            # Formula --> EAR = (1 + i/n)^n -1
            # "n" is 2 (semi annually occur twice) to calculate the interest rate
        semiMonthlyPeriod = 2 
        rate = self.__semiCompoundRates / 100.0
        EAR = (1 + rate/semiMonthlyPeriod) ** semiMonthlyPeriod - 1

        #Convert EAR into the Periodic Interest Rate for each payment type 
            # Formula --> r = (1+ APR/m)^m/f -1)
            # APR/m is equal to the EAR; m is equal to one year (to divide payments throughout the year); f is equal to annualPayments
        return (1 + EAR) ** (1/annualPayments) - 1

    #Design method to calcuate payment amount (given principal and payment period)
    def calcPMT (self, principalAmount, annualPayments):

        #Calculate periodic interest rate based on the payment frequency 
        rate = self.periodicIR(annualPayments)

        #Calculate total number of payments over the full amortiziation period
        numOfPayments = annualPayments * self.__amortPeriod

        #Calculate payment required based on the interest and time period
            #Rearrange the Present Value of Annuity Factor formula to isolate and solve for PMT 
        return principalAmount * rate/(1-(1+rate) ** (-numOfPayments))

    #Design method to calculate the payment for all six payment periods
    def payments (self, principalAmount):

        #Calculate the mortgage payment amount 
        monthly = self.calcPMT(principalAmount, 12)
        semiMonthly = self.calcPMT(principalAmount, 24)
        biWeekly = self.calcPMT(principalAmount, 26)
        weekly = self.calcPMT(principalAmount, 52)

        #BiWeekly occurs twice a month, while Weekly occurs four times a month
        biWeek = 2
        perMonth = 4
        
        accelBiweekly = monthly /biWeek
        accelWeekly = monthly /perMonth 

    #Return a tuple for all six payment options, rounded to 2 decimals
        return (
        "{:.2f}".format(monthly),
        "{:.2f}".format(semiMonthly),
        "{:.2f}".format(biWeekly),
        "{:.2f}".format(weekly),
        "{:.2f}".format(accelBiweekly),
        "{:.2f}".format(accelWeekly)
        )
    
    #Design method that returns a loan amortization and payment schedule
    #principalAmount: total loan amount due
    #paymentsPerYear: number of payments made each year (based on the payment option)
    #isCalculated: determines if the payment amount should be calculated or if it is already known 
    #(used for accelerated payments where payments are based on the monthly payment divided by 2 or 4)
    #fixedPayment: stores the values of the accelerated biweekly and weekly payments
    def amortPay_Schedule(self, principalAmount, paymentsPerYear, isCalculated=0, fixedPayment=0.0):
        
        #Calculate the periodic interest rate per payment period
        r = self.periodicIR(paymentsPerYear)

        #Calculate the total number of payment that need to be made over the full amortization period
        n = int (self.__amortPeriod * paymentsPerYear)

        #If isCalculated == 1, the payment has already been determined (does not need to be calculated) 
        #(represents an accelerated payment)
        if isCalculated == 1:
            #Convert to a float so it can be used in calculations
            payment = float(fixedPayment)

        #If isCalculated is not equal to 1, c alculate the payment amount for the loan 
        else:
            payment = self.calcPMT(principalAmount, paymentsPerYear)

        #Set the starting balance equal to the original amount borrowed
        paymentBalance = principalAmount

        #Create an empty list to hold all payment data
        schedule = []

        #Loop through each payment period (from 1 to n)
        for i in range (1, n + 1):

            #Store the starting balance of the payment
            startBalance = paymentBalance

            #Calculate interest for the current payment period
            interest = paymentBalance * r

            #Calculate how much of the payment goes towards the loan balance (after interest)
            principalPaid = payment - interest

            #Update the loan balance after one payment
            endBalance = paymentBalance - principalPaid

            #Set default payment 
            paymentPeriod = payment

            #Check if this is the final payment period
            if i == n:

                #Set the principal paid equal to the remaining loan balance
                principalPaid = paymentBalance

                #Calculate the total payment for this final period
                paymentPeriod = interest + principalPaid

                #Loan is fully paid off, set ending balance to 0.00
                endBalance = 0.00

            #If the payment exeeds or equals the remaining loan balance
            elif principalPaid >= paymentBalance:

                principalPaid = paymentBalance
                paymentPeriod = interest + principalPaid 
                endBalance = 0.0
    
            
            #Record all payment details for the current payment cycle into the amortization table 
            #Round all values to two decimal places
            schedule.append([
                i, 
                round(startBalance, 2),
                round(interest, 2),
                round(paymentPeriod, 2),
                round(endBalance, 2) 
            ])
           
            #Update the remaining loan balance for the next payment period
            #The ending balance from this period becomes the new starting balance  
            paymentBalance = endBalance

            #If the loan is fully paid off, stop the loop
            if paymentBalance <= 0:
                break

        #Convert the full list of payments into a table
        return pd.DataFrame(
            schedule, 
            columns=["Period", "Starting Balance" , "Interest" , "Payment", "Ending Balance"]
        )
 
#If the code is directly run, execute the code below
if __name__ == "__main__":

#Prompt the user to enter the mortgage principal, quoted interest rate (%), amortization period of mortgage (in years), and mortgage term  
    principalAmount = float((input("Enter Mortgage Principal (e.g., 80,000): ")))
    semiCompoundRates = float((input ("Enter Quoted Annual Interest Rate % (e.g., 4.2): ")))
    amortPeriod = int((input ("Enter Amortization In # of Years (e.g., 20): ")))
    termYears = int((input ("Enter Mortgage Term (years): ")))

#Calculate the quoted interest and amoritzed period for the inputed answers 
    calcIR_AP = MortgagePayment(semiCompoundRates, amortPeriod)

#Returning the tuple --> take the principal amount and calculate for payment options
    monthly, semiMonthly, biWeekly, weekly, accelBiweekly, accelWeekly = calcIR_AP.payments(principalAmount)

#Print the values for all six payment options
    print ("")
    print ("PAYMENT AMOUNTS:")
    print ("")
    print ("Monthly Payment: $" + monthly)
    print ("Semi-monthly Payment: $" + semiMonthly)
    print ("Bi-weekly Payment: $" + biWeekly)
    print ("Weekly Payment: $" + weekly)
    print ("Rapid Bi-weekly Payment: $" + accelBiweekly)
    print ("Rapid Weekly Payment: $" + accelWeekly)

    #Create a dictionary to store the number of payments per year for each payment type
    paymentOptions = {
        "Monthly": 12,
        "Semi-monthly": 24,
        "Bi-weekly": 26,
        "Weekly": 52,
        "Rapid Bi-weekly": 26,
        "Rapid Weekly": 52
    }
    
    #Create Excel Workbook
    wb = openpyxl.Workbook()

    #Delete the automatically created extra blank Excel sheet
    wb.remove(wb.active)

    #Create chart (10 by 6 inches)
    plt.figure(figsize=(10,6))

    #Loop through each payment option in the dictionary
    #Store the label in "paymentName" and its number of payments per year in "numPay"
    for paymentName in paymentOptions:
        numPay = paymentOptions[paymentName]

        #If the payment option is "Rapid Bi-weekly", calculate and generate the accelerated bi-weekly amortization schedule
        if paymentName == "Rapid Bi-weekly":
            df = calcIR_AP.amortPay_Schedule(principalAmount, numPay, 1, accelBiweekly)
        
          #If the payment option is "Rapid Weekly", calculate and generate the accelerated weekly amortization schedule
        elif paymentName == "Rapid Weekly":
            df = calcIR_AP.amortPay_Schedule(principalAmount, numPay, 1, accelWeekly)

        #Calculate and generate the amortization schedule for the other payment types
        else:
            df = calcIR_AP.amortPay_Schedule(principalAmount, numPay, 0, 0.0)

        #Calculate the total number of payments for the mortgage term
        #Trim the dataframe to include only the payments within the mortgage term
        keepRows = termYears * numPay
        df = df.iloc[:keepRows].copy()
        
        #Create new Excel sheet inside the workbook
        ws = wb.create_sheet(title=paymentName)

        #Add column headers to Excel
        ws.append(list(df.columns))

        #Loop through each row and record its data in the Excel sheet
        for row in range(len(df)):
            ws.append(list(df.iloc[row]))

        #Convert the period and ending columns to NumPy arrays for plotting 
        x = np.array(df["Period"])
        y = np.array(df["Ending Balance"])
        plt.plot(x, y, label=paymentName)

    #Save and close the Excel workbook
    wb.save("Loan_Payment_Schedule.xlsx")
    wb.close()

    #Set up graph title and labels
    plt.title("Loan Balance Decline By Payment Frequencies")
    plt.xlabel("Period")
    plt.ylabel("Ending Balance ($)")
    plt.legend()

    #Save graph as a PNG file
    plt.savefig("Loan_Balance_Decline.png")
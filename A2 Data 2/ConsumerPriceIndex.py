import pandas as pd

#Upload CSV files for all provinces and Canada
files = {
    "Canada": "A2 Data 2/Canada.CPI.1810000401.csv",
    "Alberta": "A2 Data 2/AB.CPI.1810000401.csv",
    "British Columbia": "A2 Data 2/BC.CPI.1810000401.csv",
    "Manitoba": "A2 Data 2/MB.CPI.1810000401.csv",
    "New Brunswick": "A2 Data 2/NB.CPI.1810000401.csv",
    "Newfoundland and Labrador": "A2 Data 2/NL.CPI.1810000401.csv",
    "Nova Scotia": "A2 Data 2/NS.CPI.1810000401.csv",
    "Ontario": "A2 Data 2/ON.CPI.1810000401.csv",
    "Prince Edward Island": "A2 Data 2/PEI.CPI.1810000401.csv",
    "Quebec": "A2 Data 2/QC.CPI.1810000401.csv",
    "Saskatchewan": "A2 Data 2/SK.CPI.1810000401.csv"
}

#Upload Minimum Wage CSV file
minWAGE_FILE = "A2 Data 2/MinimumWages.csv"

#Define all valid month labels from the CSV files in the "MM-YY" format 
MONTHS= ["Jan-24","Feb-24","Mar-24","Apr-24","May-24","Jun-24", "Jul-24","Aug-24","Sep-24","Oct-24","Nov-24","Dec-24"]

#Create a method to load the CPI data
def loadData(file, juris):

    #Read the CSV files containing CPI data for all provinces and Canada
    singleCPI_Data = pd.read_csv(file)

    #Remove extra white space from column headers
    singleCPI_Data.columns = [c.strip() for c in singleCPI_Data.columns]

    #Create a method to convert data formats (e.g., 24-Jan --> Jan-24)
    def convertDate(monthLabel):

        #If the date is already in the correct format, return it
        if monthLabel in MONTHS:
            return monthLabel
        
        #Split the string into two seperate parts (seperate the month and year)
        parts = monthLabel.split("-")

        #If there are exactly two parts of a valid date format (month & year) 
        if len(parts) == 2:

            #Flip the order of the strings
            flipped = parts[1] + "-" + parts[0]   # 24-Jan -> Jan-24

            #If the flipped version matches what the format in MONTHS, return it 
            if flipped in MONTHS:
                return flipped
            
        #Return an empty strying if the column is not a valid month or year
        return ""

    #Create an empty to store the month columns
    monthColumns = []

    #Loop through every column name in each spreadsheet
    for c in singleCPI_Data.columns:

        #Use convertDate method to check if the column name represents a valid month 
        #If it does, then store it in the list
        if convertDate (c) != "":
            monthColumns.append(c)              

    #Create empty lists to store each category of data 
    items, months, values, jurisdictions = [], [], [], []

    #Convert each month coloumn to the proper format
    for monthLabel in monthColumns:
        convertCalc = convertDate(monthLabel)

        #Loop through every row in the current spreadsheet to extract data
        for rowNum in range(len(singleCPI_Data)):

            #Add the item name from the Item column
            items.append(singleCPI_Data.loc[rowNum, "Item"])

            #Add the month name 
            months.append(convertCalc)      

            #Add CPI value from the current month column
            values.append(singleCPI_Data.loc[rowNum, monthLabel])

            #Add the jurisidictions name
            jurisdictions.append(juris)

    #Return a table containing all the CPI data
    return pd.DataFrame({
        "Item": items,
        "Month": months, 
        "Jurisdiction": jurisdictions, 
        "CPI": values
    })

#Create a method that calculates the average month-to-month percent change
def avgChanges (jusName, cpiItem):

    #List that will store CPI values needed for this calculation
    avgValues = []

    #Loop through each month in the MONTHS lists
    for monthName in MONTHS:

        #Loop through every row in the combined CPI data table 
        for r in range(len(cpi)):

            #Check that the CPI row belongs to the correct province or "Canada"
            if cpi.loc[r, "Jurisdiction"] == jusName:

                #Check that the CPI row matches the correct items 
                if cpi.loc[r, "Item"] == cpiItem:

                    #Check that the CPI row matches the current month from MONTHS
                    if cpi.loc[r, "Month"] == monthName:

                        #Convert CPI values to float and add to the list for percentage calculation
                        avgValues.append(float(cpi.loc[r,"CPI"]))

                        #Stops checking further rows once the values are found 
                        break
    
    #Store the total sum of all month-to-month percent changes
    total = 0

    #Loop through the avgValues list
    #Takes the previous month's CPI and current month's CPI
    #Finds how much it changed in percent and adds that to the total
    for i in range(1, len(avgValues)):
        previousMonth = avgValues[i - 1]
        currentMonth = avgValues[i]

        #If previous CPI value is not zero, add the percent change to the total
        if previousMonth !=0:
            total = total + ((currentMonth - previousMonth) / previousMonth) * 100.0
    
    #Calculate the average percent change for one speicific item
    if len(avgValues) > 1: 
        return total / (len(avgValues) - 1)
    
    #Return 0 if there is not enough data to calculate an average
    else:
        return 0.0
    
#Create a method that finds the CPI value for a specific jurisdiction, item, and month
def getCpi (specificJur, item, month):

    #Loop through each row in the CPI dataset 
    #Until the Jurisdiction, item ("All-items"), and Month ("Dec-24") matches
    for currentRow in range (len(cpi)):
        row = cpi.loc[currentRow]
        if row["Jurisdiction"] == specificJur:
            if row["Item"] == item:
                if row["Month"] == month:
                    return float(row["CPI"])
    
    #If the at least one of the conditions are not met, return 0.0
    return 0.0

if __name__ == "__main__":

#==========
#QUESTION 1/2
#==========
           
    #Create empty list to store CPI data for all provinces and Canada
    allData = []

    #Loop through each csv file in the dictionary 
    #Load each csv file using loadData() and add its data to the allData list
    for province in files:
        allData.append(loadData(files[province], province))

    #Combine all datasets into a single data
    cpi = pd.concat(allData, ignore_index=True)

    print ("=" * 90)
    print ("Q1/2: Create first 12 rows of CPI Data Table")

    #Print the first 12 rows of the table
    print(cpi.head(12).to_string(index=False))
    print ("")

#==========
#QUESTION 3
#==========

    #Three categories necessary to calculate the average month-to-month change
    targetItems = ["Food", "Shelter", "All-items excluding food and energy"]

    #Print the title and the average month-to-month percent changes for each category
    print("=" * 80)
    print("Q3: Average Month-to-Month change (Food, Shelter, All-items excl. food & energy)")
    print("")
    print("{:<25} {:<35} {:>8}".format("Jurisdiction", "Item", "Change"))
    print("-" * 70)

    #Create an empty list to store all jurisdictions
    jurisList = []

    #Loop through all the jurisdictions and add any that are not already included
    for name in cpi ["Jurisdiction"]:
        if name not in jurisList:
            jurisList.append(name)

    #Loop through each jurisidiction to calculate its overall average change
    for jusName in jurisList:

        #Loops through all categories in targetItems
        for itemName in targetItems:

            #Uses avgChanges method to calculate the average percent change
            sumAvg = avgChanges(jusName, itemName)

            #To ensure there are no negative zeros
            if sumAvg < 0.05:
                if sumAvg > -0.05:
                    sumAvg = 0.0

            #Round the average change to one decimal place
            formattedChange = round(sumAvg, 1)

            #Print the jurisidiction name, item name, and its corresponding average percent change
            print("{:<25} {:<35} {:>6.1f}%".format(jusName, itemName, formattedChange))    

#==========
#QUESTION 4
#==========

    #Create an empty list to store all provinces
    provinces = []
    for province in jurisList:
        if province != "Canada":
            provinces.append(province)

    #Store the name of the province with the highest average change
    bestProvince = ""

    #Store the numerical value of the highest average percent change
    bestValue = 0.0

    #Used to identify the first province in the loop
    firstLineProv = True

    #Loop through each province to calculate its overall average (%) change
    for jname in provinces:

        #total sum of average changes for the current province
        sumProv = 0.0

        #Loop through each of the categories in targetItems 
        #Calculate the overall average percent change for each category
        for item in targetItems:
            sumProv += avgChanges(jname, item)

        #Calculate the overall average percent change for the province across all three categories
        avg = round (sumProv / len(targetItems), 1)   

        #If this is the first province, store its name and average change as the current best
        if firstLineProv:
            bestProvince = jname
            bestValue = avg
            firstLineProv = False

        #If a later province has a higher average change, update the best province and value
        elif avg > bestValue:
            bestProvince = jname
            bestValue = avg

    #Print the province with the highest average change (Food, Shelter, All-items excl.)
    print("")
    print("=" * 90)
    print("Q4: Province with Highest Average Change (Food, Shelter, All-items excl. food & energy):")
    print(bestProvince, ":", round (bestValue, 1), "%")

##==========
#QUESTION 5
#==========

    #Define the reference item, month, salary, and province
    targetItem_q5 = "All-items"
    targetMonth_q5 = "Dec-24"
    base_salary = 100000.0
    base_province = "Ontario"

    #Call the method getCpi to obtain Ontario's All-items CPI number
    ontCpi = getCpi(base_province, targetItem_q5, targetMonth_q5)

    #Print the results
    print("")
    print("=" * 90)
    print("Q5: Equivalent salary to $100000 in Ontario (as at Dec-24):")

    #Loop through each province except Canada
    for j in jurisList:
        if j != "Canada":

            #Find and store each province's All-items CPI value for equivalent salary calculation
            provCpi = getCpi (j, targetItem_q5, targetMonth_q5)

            #If Ontario's All-items CPI is not zero
            if ontCpi > 0.0:

                #Calculate the equivalent salary
                eq = base_salary * (provCpi / ontCpi)

                #Print each province and their equivalant salary (rounded to 1 decimal)
                print(j, ":", "$" + str(round(eq, 1)))

#==========
#QUESTION 6
#==========

    #Read the Minimum Wage CSV file
    minWage = pd.read_csv(minWAGE_FILE)

    #Remove extra white space from column headers
    minWage.columns = [c.strip() for c in minWage.columns]

    #Create a variable to identify when the loop is on its first iteration
    firstLineWage = True

    #Loop every row in the minimum wage file
    for p in range(len(minWage)):

        #Obtain the province code and convert it to a string
        provCode = str(minWage.loc[p, "Province"])

        #Obtain the province's minimum wage and convert it to a float
        wage = float(minWage.loc[p, "Minimum Wage"])

        #If this is the first row of data (first province), Set this as the highest and lowest province and minimum wage
        if firstLineWage:
            highProv = provCode; lowProv = provCode
            highWage = wage; lowWage = wage
            firstLineWage = False
    
        #If the current provinces wage is greater than the currnt maximum wage, update it
        elif wage > highWage:
            highProvProv = provCode; highWage = wage
    
        #If the current provinces wage is lower than the current minimum wage, update it
        elif wage < lowWage:
            lowProvProv = provCode; lowWage = wage

    #Print the highest and lowest nominal wages (rounded to 2 decimals)
    print("")
    print("=" * 90)
    print("Q6: Nominal & Real Minimum Wages")
    print("Highest Nominal Wage:", highProvProv, "-> $", round(highWage, 2))
    print("Lowest Nominal Wage :", lowProv, "-> $", round(lowWage, 2))

    #Dictionary that links each province code to its full name
    provList = {
        "AB": "Alberta",
        "BC": "British Columbia",
        "MB": "Manitoba",
        "NB": "New Brunswick",
        "NL": "Newfoundland and Labrador",
        "NS": "Nova Scotia",
        "ON": "Ontario",
        "PEI": "Prince Edward Island",
        "QC": "Quebec",
        "SK": "Saskatchewan",
    }

    #Create two variables to track the province with the highest real wage
    bestProv_Real = ""
    bestReal_Wage = 0.0

    #Loop through every row (province) in the minimum wage file
    for p in range(len(minWage)):

        #Obtain the province code and convert it to a string
        wage = str(minWage.loc[p, "Province"])

        #If the province code exists in the provList dictionary, look up the full province name and obtain its CPI value 
        if wage in provList:
            name = provList[wage]
            cpiValue = getCpi(name, "All-items", "Dec-24")

            #If the CPI value is greater than zero
            if cpiValue > 0.0:

                #Read the minimum wage column from the CSV for that province and calculate the real minimum wage
                coloum = float(minWage.loc[p, "Minimum Wage"])
                current = coloum / (cpiValue / 100.0)

                #If the current province's real wage is higher than the current one, update it
                if current > bestReal_Wage:
                    bestReal_Wage = current
                    bestProv_Real = wage

    #Print the province with the highest real wage
    print("Highest Real Wage:", bestProv_Real, "-> $", round(bestReal_Wage, 2))

#==========
#QUESTION 7
#==========

    #Define which CPI category to analyze
    targetItem_q7 = "Services"

    #Define the start and end months
    startMonth_q7 = "Jan-24"
    endMonth   = "Dec-24"

    #Create a variable to identify when the loop is on its first iteration
    first = True

    #Store the province with the largest change
    largeProv = ""  

    #Store the value of the province with the largest change
    largeVal = 0.0  

    #Print the annual percentage change
    print("")
    print("=" * 90)
    print("Q7: Annual percentage change in CPI for Services:")

    #Loop through each province 
    #Reset the starting and ending CPI values for each province
    for prov in jurisList:
        startCpi = 0.0
        endCpi = 0.0

        #Loop through every row
        for r in range(len(cpi)):
            row = cpi.loc[r]

            #If the Jurisdiction and item ("Services") match, extract the Jan and Dec values
            if row["Jurisdiction"] == prov:
                if row["Item"] == targetItem_q7:
                    if row["Month"] == startMonth_q7:
                        startCpi = float(row["CPI"])
                    elif row ["Month"] == endMonth:
                        endCpi = float(row["CPI"])

         #If there is a valid number for January, calculate the percentage change
        change = 0.0
        if startCpi > 0.0:
            change = ((endCpi - startCpi) / startCpi) * 100.0

        #To ensure there are no negative zeros
        if -0.05 < change < 0.0:
            change = 0.0

        #Print the annual change for each province (rounded to 1 decimal)
        print(prov, ":", round(change, 1), "%")

        #If the CPI change is higher than the current best, update it
        if first:
            largeProv = prov
            largeVal = change
            first = False
        elif change > largeVal:
            largeProv = prov
            largeVal = change

#==========
#QUESTION 8
#==========

    #Print the region with the highest inflation in services (rounded to 1 decimal)
    print("")
    print("=" * 90)
    print("Q8: Region with Highest Inflation in Services (Jan–Dec 2024):")
    print(largeProv, "->", round(largeVal, 1), "%")

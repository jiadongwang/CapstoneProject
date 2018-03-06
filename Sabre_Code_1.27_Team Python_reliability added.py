from gurobipy import *
n = Model()
from math import *
from scipy.stats import norm

currentYear = int(input('Enter the year: '))
reliabilityLevel = float(input('Enter the desired reliability level: '))
inverseNormalReliability = norm.ppf(reliabilityLevel)

listOfMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'Novermber', 'December']
Months = [0,1,2,3,4,5,6,7,8,9,10,11]

if currentYear%4==0:
    FebuaryLength = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    daysInFeb = 29
else:
    FebuaryLength = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
    daysInFeb = 28
    
ShortMonthLength = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
LongMonthLength = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

m = 0
f = 0
s = 0
l = 0


# monthly line holders, crew scheduled, averges provided, std. devs. provided, and the difference between monthlyLineHolders and monthlyCrew

monthlyLineHolders = [] 
 
for m in Months: 
	lineHolders = int(input('Enter the number of lineholders for the month of ' + listOfMonths[m] + ': '))
	monthlyLineHolders.append(lineHolders)

monthlyCrewScheduled = [] 
 
for m in Months: 
	crewScheduled = int(input('Enter the number of crew scheduled for the month of ' + listOfMonths[m] + ': '))
	monthlyCrewScheduled.append(crewScheduled)

averageMonthlyExpectedAbsences = []

for m in Months: 
	averageAbsences = float(input('Enter the average number of absences the month of ' + listOfMonths[m] + ': '))
	averageMonthlyExpectedAbsences.append(averageAbsences)
    
varOfMonthlyExpectedAbsences = []

for m in Months: 
	varOfAbsences = float(input('Enter the variance of the absences the month of ' + listOfMonths[m] + ': '))
	varOfMonthlyExpectedAbsences.append(varOfAbsences)
    
stdDevMonthlyExpectedAbsences = []

for m in Months:
    stdDevOfAbsences = sqrt(varOfMonthlyExpectedAbsences[m])
    stdDevMonthlyExpectedAbsences.append(stdDevOfAbsences)
    
expectedMonthlyAbsences = []
    
for m in Months:
    expectedAbsenses = inverseNormalReliability * stdDevMonthlyExpectedAbsences[m] + averageMonthlyExpectedAbsences[m]
    expectedMonthlyAbsences.append(expectedAbsenses)

vacationAllottedPlusExpectedAbsences = [(monthlyLineHolders[m]-monthlyCrewScheduled[m]) for m in Months]

# daily, monthly, and annual upper and lower bounds

dailyUpperBoundVacationAllotted = int(input('Enter the maximum number of vacation days allotted for any given day: '))
dailyLowerBoundVacationAllotted = int(input('Enter the minimum number of vacation days allotted for any given day: '))

monthlyUpperBoundVacationAllotted = []

for m in Months:
    vacationAllotted = trunc(vacationAllottedPlusExpectedAbsences[m] - expectedMonthlyAbsences[m])
    monthlyUpperBoundVacationAllotted.append(vacationAllotted)
    
print(monthlyUpperBoundVacationAllotted)
    
monthlyLowerBoundVacationAllotted = int(input('Enter the minimum number of vacation days for any given month: '))

annualUpperBoundVacationAllotted = quicksum(monthlyUpperBoundVacationAllotted[m] for m in Months)
annualLowerBoundVacationAllotted = int(input('Enter the minimum number of vacation days allotted for the year: '))

n.update()

jan = n.addVars(31, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Jan")
feb = n.addVars(daysInFeb, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Feb")
mar = n.addVars(31, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Mar")
apr = n.addVars(30, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Apr")
may = n.addVars(31, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "May")
jun = n.addVars(30, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Jun")
jul = n.addVars(31, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Jul")
aug = n.addVars(31, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Aug")
sep = n.addVars(30, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Sep")
oct = n.addVars(31, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Oct")
nov = n.addVars(30, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Nov")
dec = n.addVars(31, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Dec")

n.update()

# Objective function

n.setObjective((quicksum(jan[l] for l in LongMonthLength))+(quicksum(feb[f] for f in FebuaryLength))+(quicksum(mar[l] for l in LongMonthLength))+(quicksum(apr[s] for s in ShortMonthLength))+(quicksum(may[l] for l in LongMonthLength))+(quicksum(jun[s] for s in ShortMonthLength))+(quicksum(jul[l] for l in LongMonthLength))+(quicksum(aug[l] for l in LongMonthLength))+(quicksum(sep[s] for s in ShortMonthLength))+(quicksum(oct[l] for l in LongMonthLength))+(quicksum(nov[s] for s in ShortMonthLength))+(quicksum(dec[l] for l in LongMonthLength)), GRB.MAXIMIZE)

n.update()

# Constraints for monthly maximums and minimums

janUpperBoundVacationAllotted = n.addConstr(quicksum(jan[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted[0], name = "JanmonthlyUpperBoundVacationAllotted")
febUpperBoundVacationAllotted = n.addConstr(quicksum(feb[f] for f in FebuaryLength) <= monthlyUpperBoundVacationAllotted[1], name = "FebmonthlyUpperBoundVacationAllotted")
marUpperBoundVacationAllotted = n.addConstr(quicksum(mar[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted[2], name = "MarmonthlyUpperBoundVacationAllotted")
aprUpperBoundVacationAllotted = n.addConstr(quicksum(apr[s] for s in ShortMonthLength) <= monthlyUpperBoundVacationAllotted[3], name = "AprmonthlyUpperBoundVacationAllotted")
mayUpperBoundVacationAllotted = n.addConstr(quicksum(may[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted[4], name = "MaymonthlyUpperBoundVacationAllotted")
junUpperBoundVacationAllotted = n.addConstr(quicksum(jun[s] for s in ShortMonthLength) <= monthlyUpperBoundVacationAllotted[5], name = "JunmonthlyUpperBoundVacationAllotted")
julUpperBoundVacationAllotted = n.addConstr(quicksum(jul[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted[6], name = "JulmonthlyUpperBoundVacationAllotted")
augUpperBoundVacationAllotted = n.addConstr(quicksum(aug[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted[7], name = "AugmonthlyUpperBoundVacationAllotted")
sepUpperBoundVacationAllotted = n.addConstr(quicksum(sep[s] for s in ShortMonthLength) <= monthlyUpperBoundVacationAllotted[8], name = "SepmonthlyUpperBoundVacationAllotted")
octUpperBoundVacationAllotted = n.addConstr(quicksum(oct[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted[9], name = "OctmonthlyUpperBoundVacationAllotted")
novUpperBoundVacationAllotted = n.addConstr(quicksum(nov[s] for s in ShortMonthLength) <= monthlyUpperBoundVacationAllotted[10], name = "NovmonthlyUpperBoundVacationAllotted")
decUpperBoundVacationAllotted = n.addConstr(quicksum(dec[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted[11], name = "DecmonthlyUpperBoundVacationAllotted")

janLowerBoundVacationAllotted = n.addConstr(quicksum(jan[l] for l in LongMonthLength) >= monthlyLowerBoundVacationAllotted, name = "JanmonthlyLowerBoundVacationAllotted")
febLowerBoundVacationAllotted = n.addConstr(quicksum(feb[f] for f in FebuaryLength) >= monthlyLowerBoundVacationAllotted, name = "FebmonthlyLowerBoundVacationAllotted")
marLowerBoundVacationAllotted = n.addConstr(quicksum(mar[l] for l in LongMonthLength) >= monthlyLowerBoundVacationAllotted, name = "MarmonthlyLowerBoundVacationAllotted")
aprLowerBoundVacationAllotted = n.addConstr(quicksum(apr[s] for s in ShortMonthLength) >= monthlyLowerBoundVacationAllotted, name = "AprmonthlyLowerBoundVacationAllotted")
mayLowerBoundVacationAllotted = n.addConstr(quicksum(may[l] for l in LongMonthLength) >= monthlyLowerBoundVacationAllotted, name = "MaymonthlyLowerBoundVacationAllotted")
junLowerBoundVacationAllotted = n.addConstr(quicksum(jun[s] for s in ShortMonthLength) >= monthlyLowerBoundVacationAllotted, name = "JunmonthlyLowerBoundVacationAllotted")
julLowerBoundVacationAllotted = n.addConstr(quicksum(jul[l] for l in LongMonthLength) >= monthlyLowerBoundVacationAllotted, name = "JulmonthlyLowerBoundVacationAllotted")
augLowerBoundVacationAllotted = n.addConstr(quicksum(aug[l] for l in LongMonthLength) >= monthlyLowerBoundVacationAllotted, name = "AugmonthlyLowerBoundVacationAllotted")
sepLowerBoundVacationAllotted = n.addConstr(quicksum(sep[s] for s in ShortMonthLength) >= monthlyLowerBoundVacationAllotted, name = "SepmonthlyLowerBoundVacationAllotted")
octLowerBoundVacationAllotted = n.addConstr(quicksum(oct[l] for l in LongMonthLength) >= monthlyLowerBoundVacationAllotted, name = "OctmonthlyLowerBoundVacationAllotted")
novLowerBoundVacationAllotted = n.addConstr(quicksum(nov[s] for s in ShortMonthLength) >= monthlyLowerBoundVacationAllotted, name = "NovmonthlyLowerBoundVacationAllotted")
decLowerBoundVacationAllotted = n.addConstr(quicksum(dec[l] for l in LongMonthLength) >= monthlyLowerBoundVacationAllotted, name = "DecmonthlyLowerBoundVacationAllotted")


# Constraints for annual maximums and minimums

conamax = n.addConstr(((quicksum(jan[l] for l in LongMonthLength))+(quicksum(feb[f] for f in FebuaryLength))+(quicksum(mar[l] for l in LongMonthLength))+(quicksum(apr[s] for s in ShortMonthLength))+(quicksum(may[l] for l in LongMonthLength))+(quicksum(jun[s] for s in ShortMonthLength))+(quicksum(jul[l] for l in LongMonthLength))+(quicksum(aug[l] for l in LongMonthLength))+(quicksum(sep[s] for s in ShortMonthLength))+(quicksum(oct[l] for l in LongMonthLength))+(quicksum(nov[s] for s in ShortMonthLength))+(quicksum(dec[l] for l in LongMonthLength))) <= annualUpperBoundVacationAllotted, name = "TotannualUpperBoundVacationAllotted")

conamin = n.addConstr(((quicksum(jan[l] for l in LongMonthLength))+(quicksum(feb[f] for f in FebuaryLength))+(quicksum(mar[l] for l in LongMonthLength))+(quicksum(apr[s] for s in ShortMonthLength))+(quicksum(may[l] for l in LongMonthLength))+(quicksum(jun[s] for s in ShortMonthLength))+(quicksum(jul[l] for l in LongMonthLength))+(quicksum(aug[l] for l in LongMonthLength))+(quicksum(sep[s] for s in ShortMonthLength))+(quicksum(oct[l] for l in LongMonthLength))+(quicksum(nov[s] for s in ShortMonthLength))+(quicksum(dec[l] for l in LongMonthLength))) >= annualLowerBoundVacationAllotted, name = "TotannualLowerBoundVacationAllotted")

n.update()
n.optimize()

n.write('sabre.sol')



from gurobipy import *
n = Model()
from math import ceil

Months = [0,1,2,3,4,5,6,7,8,9,10,11]
FebuaryLength = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
ShortMonthLength = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
LongMonthLength = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
Y = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,
109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,
192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,
275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,
358,359,360,361,362,363,364]
m = 0
f = 0
s = 0
l = 0
y = 0

# monthly line holders, crew scheduled, averges provided, std. devs. provided, and the difference between monthlyLineHolders and monthlyCrew

monthlyLineHolders = [700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700]
monthlyCrewScheduled = [476, 432, 469, 447, 465, 481, 475, 482, 436, 460, 480, 478]
averageMonthlyExpectedAbsences = [49.8, 32.1, 48.4, 35.3, 42.4, 45.3, 47.0, 40.0, 35.8, 41.0, 46.7, 55.7]
stdDevMonthlyExpectedAbsences = [9.7877, 9.1978, 9.9096, 9.4181, 9.6125, 9.8691, 10, 9.8995, 9.3113, 9.1214, 9.1978, 9.5394]
vacationAllottedPlusExpectedAbsences = [(monthlyLineHolders[m]-monthlyCrewScheduled[m]) for m in Months]

# daily, monthly, and annual upper and lower bounds

dailyUpperBoundVacationAllotted = int(input('Enter daily upper bound of vacation days allotted: '))
dailyLowerBoundVacationAllotted = 2

monthlyUpperBoundVacationAllotted = 250
monthlyLowerBoundVacationAllotted = 60

annualUpperBoundVacationAllotted = 2000
annualLowerBoundVacationAllotted = 1000

n.update()

jan = n.addVars(31, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Jan")
feb = n.addVars(28, lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Feb")
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

janUpperBoundVacationAllotted = n.addConstr(quicksum(jan[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted, name = "JanmonthlyUpperBoundVacationAllotted")
febUpperBoundVacationAllotted = n.addConstr(quicksum(feb[f] for f in FebuaryLength) <= monthlyUpperBoundVacationAllotted, name = "FebmonthlyUpperBoundVacationAllotted")
marUpperBoundVacationAllotted = n.addConstr(quicksum(mar[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted, name = "MarmonthlyUpperBoundVacationAllotted")
aprUpperBoundVacationAllotted = n.addConstr(quicksum(apr[s] for s in ShortMonthLength) <= monthlyUpperBoundVacationAllotted, name = "AprmonthlyUpperBoundVacationAllotted")
mayUpperBoundVacationAllotted = n.addConstr(quicksum(may[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted, name = "MaymonthlyUpperBoundVacationAllotted")
junUpperBoundVacationAllotted = n.addConstr(quicksum(jun[s] for s in ShortMonthLength) <= monthlyUpperBoundVacationAllotted, name = "JunmonthlyUpperBoundVacationAllotted")
julUpperBoundVacationAllotted = n.addConstr(quicksum(jul[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted, name = "JulmonthlyUpperBoundVacationAllotted")
augUpperBoundVacationAllotted = n.addConstr(quicksum(aug[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted, name = "AugmonthlyUpperBoundVacationAllotted")
sepUpperBoundVacationAllotted = n.addConstr(quicksum(sep[s] for s in ShortMonthLength) <= monthlyUpperBoundVacationAllotted, name = "SepmonthlyUpperBoundVacationAllotted")
octUpperBoundVacationAllotted = n.addConstr(quicksum(oct[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted, name = "OctmonthlyUpperBoundVacationAllotted")
novUpperBoundVacationAllotted = n.addConstr(quicksum(nov[s] for s in ShortMonthLength) <= monthlyUpperBoundVacationAllotted, name = "NovmonthlyUpperBoundVacationAllotted")
decUpperBoundVacationAllotted = n.addConstr(quicksum(dec[l] for l in LongMonthLength) <= monthlyUpperBoundVacationAllotted, name = "DecmonthlyUpperBoundVacationAllotted")

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



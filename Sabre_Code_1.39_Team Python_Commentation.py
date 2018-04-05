from gurobipy import *
n = Model()
from math import *
from scipy.stats import norm

try:
    from tkinter import *
    from ttk import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
import tkinter as tk


innerList = []
innerList2 = []
listOfMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#-----First GUI window-----
class SimpleTableInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        
        root.title("User Input")
        
        self._entry = {}
        self.rows = rows
        self.columns = columns        
        
        # register a command to use for validation
        vcmd = (self.register(self._validate), "%P")

        # create the table of widgets
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column+1)
                e = tk.Entry(self, validate="key", validatecommand=vcmd)
                e.grid(row=row, column=column+1, stick="nsew")
                enterYear = tk.Label(self, text="Enter the year")
                enterYear.grid(row=0, column=0, sticky=W)
                enterRely = tk.Label(self, text="Enter the reliability")
                enterRely.grid(row=1, column=0, sticky=W)
                enterMaxDays = tk.Label(self, text="Enter the maximum number of vacation days allotted for any given day")
                enterMaxDays.grid(row=2, column=0, sticky=W)
                enterMinDays = tk.Label(self, text="Enter the minimum number of vacation days allotted for any given day")
                enterMinDays.grid(row=3, column=0, sticky=W)
                enterMinMonth = tk.Label(self, text="Enter the minimum number of vacation days for any given month")
                enterMinMonth.grid(row=4, column=0, sticky=W)
                enterMinYear = tk.Label(self, text="Enter the minimum number of vacation days allotted for the year")
                enterMinYear.grid(row=5, column=0, sticky=W)
                self._entry[index] = e
                
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column+1, weight=1)
            
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(rows, weight=1)

    def get(self):
        #Return a list of lists, containing the data in the table
        
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column+1)
                innerList2.append(float(self._entry[index].get()))
        return innerList2


    def _validate(self, P):
        #Perform input validation. 

        #Allow only an empty value, or a value that can be converted to a float
        
        if P.strip() == "":
            return True

        try:
            f = float(P)
        except ValueError:
            self.bell()
            return False
        return True
   

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.table = SimpleTableInput(self, 6, 1)
        self.submit = tk.Button(self, text="Submit", command=self.on_submit)
        self.table.pack(side="top")
        self.submit.pack(side="bottom")
        
        
    def on_submit(self):
        for m in range(6):
            innerList2.append(self.table.get())
        root.destroy()

        
root = tk.Tk()
Example(root).pack(side="top")
root.mainloop()

#-----Fill in variables with inputs from user-----
for m in range(6):
    if m == 0:
        currentYear = innerList2[m]
    if m == 1:
        reliabilityLevel = innerList2[m]
    if m == 2:
        dailyUpperBoundVacationAllotted = innerList2[m]
    if m == 3:
        dailyLowerBoundVacationAllotted = innerList2[m]
    if m == 4:
        monthlyLowerBoundVacationAllotted = innerList2[m]
    if m == 5:
        annualLowerBoundVacationAllotted = innerList2[m]

#-----Second GUI window-----
class SimpleTableInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        
        root.title("User Input")
        
        self._entry = {}
        self.rows = rows
        self.columns = columns
                
        # register a command to use for validation
        vcmd = (self.register(self._validate), "%P")

        # create the table of widgets
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row+1, column+1)
                e = tk.Entry(self, validate="key", validatecommand=vcmd)
                e.grid(row=row+1, column=column+1, stick="nsew")
                labelMonth = tk.Label(self, text=str(listOfMonths[column]))
                labelMonth.grid(row=0, column=column+1)
                enterLh = tk.Label(self, text="Lineholders")
                enterLh.grid(row=1, column=0, sticky=W)
                enterCr = tk.Label(self, text="Crew Scheduled")
                enterCr.grid(row=2, column=0, sticky=W)
                enterAvg = tk.Label(self, text="Average Absences")
                enterAvg.grid(row=3, column=0, sticky=W)
                enterVar = tk.Label(self, text="Variance of Absences")
                enterVar.grid(row=4, column=0, sticky=W)
                self._entry[index] = e
                
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column+1, weight=1)
            
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(rows+1, weight=1)

    def get(self):
        #Return a list of lists, containing the data in the table
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row+1, column+1)
                innerList.append(float(self._entry[index].get()))
        return innerList

    def _validate(self, P):
        #Perform input validation. 

        #Allow only an empty value, or a value that can be converted to a float
        
        if P.strip() == "":
            return True

        try:
            f = float(P)
        except ValueError:
            self.bell()
            return False
        return True
   

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.table = SimpleTableInput(self, 4, 12)
        self.submit = tk.Button(self, text="Submit", command=self.on_submit)
        self.table.pack(side="top")
        self.submit.pack(side="bottom")
        
        
    def on_submit(self):
        for m in range(48):
            innerList.append(self.table.get())
        root.destroy()

        
root = tk.Tk()
Example(root).pack(side="top")
root.mainloop()


inverseNormalReliability = norm.ppf(reliabilityLevel)

#-----Indexing for filling in variables based on user data from the second GUI window-----
Months = range(12)
ListAppend1 = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
ListAppend2 = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
ListAppend3 = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]

#-----Range for February based on the year----- 
if currentYear%4==0:
    FebruaryLength = range(29)
    daysInFeb = 29
    numberOfDays = 366
else:
    FebruaryLength = range(28)
    daysInFeb = 28
    numberOfDays = 365

#-----Range for months that are 30 days----- 
ShortMonthLength = range(30)
#-----Range for months that are 31 days----- 
LongMonthLength = range(31)

daysInMonths = [31, daysInFeb, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

daysInYear = [LongMonthLength, FebruaryLength, LongMonthLength, ShortMonthLength, LongMonthLength, ShortMonthLength, LongMonthLength, LongMonthLength, ShortMonthLength, LongMonthLength, ShortMonthLength, LongMonthLength]

#-----monthly line holders, crew scheduled, averges provided, variances provided, and the difference between monthlyLineHolders and monthlyCrew-----
monthlyLineHolders = [] 

for m in range(12):
       monthlyLineHolders.append(innerList[m]) 
       

monthlyCrewScheduled = [] 

for m in ListAppend1:
       monthlyCrewScheduled.append(innerList[m]) 


averageMonthlyExpectedAbsences = []

for m in ListAppend2:
       averageMonthlyExpectedAbsences.append(innerList[m]) 


varOfMonthlyExpectedAbsences = []

for m in ListAppend3:
       varOfMonthlyExpectedAbsences.append(innerList[m]) 

    
stdDevMonthlyExpectedAbsences = []

for m in Months:
    stdDevOfAbsences = sqrt(varOfMonthlyExpectedAbsences[m])
    stdDevMonthlyExpectedAbsences.append(stdDevOfAbsences)
    
expectedMonthlyAbsences = []
    
for m in Months:
    expectedAbsenses = inverseNormalReliability * stdDevMonthlyExpectedAbsences[m] + averageMonthlyExpectedAbsences[m]
    expectedMonthlyAbsences.append(expectedAbsenses)

#-----By subtracting crew scheduled from line holders, we're left with a variable that represents vacation days plus expected absences-----
vacationAllottedPlusExpectedAbsences = [(monthlyLineHolders[m]-monthlyCrewScheduled[m]) for m in Months]

#-----Calculated monthly upper bound based on subtracting expected absences subtracted from vacation days plus expected absences-----
monthlyUpperBoundVacationAllotted = []
   
for m in Months:
    vacationAllotted = trunc(vacationAllottedPlusExpectedAbsences[m] - expectedMonthlyAbsences[m])
    monthlyUpperBoundVacationAllotted.append(vacationAllotted)
        
#-----Calculated upper bound for the year-----
annualUpperBoundVacationAllotted = quicksum(monthlyUpperBoundVacationAllotted[m] for m in Months)

n.update()

#-----Decision variable-----
vacationVariable = []
for m in Months:
    vacationVariable.append(n.addVars(daysInMonths[m], lb = dailyLowerBoundVacationAllotted, ub = dailyUpperBoundVacationAllotted, obj = 1, name = "Month" + str(m)))

#-----implementing monthly contraints-----
for m in Months:
       n.addConstr(vacationVariable[m].sum() <= monthlyUpperBoundVacationAllotted[m], name = "monthlyUpperBoundVacationAllottedForMonth" + str(m))

for m in Months:
    n.addConstr(vacationVariable[m].sum() >= monthlyLowerBoundVacationAllotted, name = "monthlyLowerBoundVacationAllotted" + str(m))   

#-----calculating the objective value-----
totalObjectiveValue = 0
for m in Months:
    objectiveValue = 0
    objectiveValue = vacationVariable[m].sum()
    totalObjectiveValue = totalObjectiveValue + objectiveValue

#-----implementing annual constraints-----
n.addConstr(totalObjectiveValue <= annualUpperBoundVacationAllotted, name = "TotannualUpperBoundVacationAllotted") 
n.addConstr(totalObjectiveValue >= annualLowerBoundVacationAllotted, name = "TotannualLowerBoundVacationAllotted")

#-----Objective function-----
for m in Months:
    n.setObjective(totalObjectiveValue, GRB.MAXIMIZE)

n.update()
n.optimize()

n.write('sabre2.sol')
n.write("out.lp")
n.write("outs.mps")

#-----initializing lists for extracting the post-optimization decision variable values-----
optimalValues = []
janOptimalVs = []
febOptimalVs = []
marOptimalVs = []
aprOptimalVs = []
mayOptimalVs = []
junOptimalVs = []
julOptimalVs = []
augOptimalVs = []
sepOptimalVs = []
octOptimalVs = []
novOptimalVs = []
decOptimalVs = []

febOptimalValues = []
marOptimalValues = []
aprOptimalValues = []
mayOptimalValues = []
junOptimalValues = []
julOptimalValues = []
augOptimalValues = []
sepOptimalValues = []
octOptimalValues = []
novOptimalValues = []
decOptimalValues = []

#-----Initial decision variable extraction-----
for l in n.getVars():
    if 0<=l<=30:    
        janOptimalVs.append(int(l.x))
    if numberOfDays == 366:
        if 31<=l<=59:
            febOptimalVs.append(int(l.x))
        if 60<=l<=90:
            marOptimalVs.append(int(l.x))
        if 91<=l<=120:
            aprOptimalVs.append(int(l.x))
        if 121<=l<=151:
            mayOptimalVs.append(int(l.x))
        if 152<=l<=181:
            junOptimalVs.append(int(l.x))
        if 182<=l<=212:
            julOptimalVs.append(int(l.x))
        if 213<=l<=243:
            augOptimalVs.append(int(l.x))
        if 244<=l<=273:
            sepOptimalVs.append(int(l.x))
        if 274<=l<=304:
            octOptimalVs.append(int(l.x))
        if 305<=l<=334:
            novOptimalVs.append(int(l.x))
        if 335<=l<=365:
            decOptimalVs.append(int(l.x))
    if numberOfDays == 365:
        if 31<=l<=58:
            febOptimalVs.append(int(l.x))
        if 59<=l<=89:
            marOptimalVs.append(int(l.x))
        if 90<=l<=119:
            aprOptimalVs.append(int(l.x))
        if 120<=l<=150:
            mayOptimalVs.append(int(l.x))
        if 151<=l<=180:
            junOptimalVs.append(int(l.x))
        if 181<=l<=211:
            julOptimalVs.append(int(l.x))
        if 212<=l<=242:
            augOptimalVs.append(int(l.x))
        if 243<=l<=272:
            sepOptimalVs.append(int(l.x))
        if 273<=l<=303:
            octOptimalVs.append(int(l.x))
        if 304<=l<=333:
            novOptimalVs.append(int(l.x))
        if 334<=l<=364:
           decOptimalVs.append(int(l.x))
     
#-----Secondary level of decision variable extraction in order to create 12 lists of range 31 populated by the decision variables for each month-----         
if numberOfDays == 366:
    febOptimalVs.insert(60, "0")
    febOptimalVs.insert(61, "0")
    aprOptimalVs.insert(121, "0")
    junOptimalVs.insert(182, "0")
    sepOptimalVs.insert(274, "0")
    novOptimalVs.insert(335, "0")
    
    for l in range(31, 62):
        febOptimalValues.append(febOptimalVs[l])
    for l in range(60, 91):
        marOptimalValues.append(marOptimalVs[l])
    for l in range(91, 122):
        aprOptimalValues.append(aprOptimalVs[l])
    for l in range(121, 152):
        mayOptimalValues.append(mayOptimalVs[l])
    for l in range(152, 183):
        junOptimalValues.append(junOptimalVs[l])
    for l in range(182, 213):
        julOptimalValues.append(julOptimalVs[l])
    for l in range(213, 244):
        augOptimalValues.append(augOptimalVs[l])
    for l in range(244, 275):
        sepOptimalValues.append(sepOptimalVs[l])
    for l in range(274, 305):
        octOptimalValues.append(octOptimalVs[l])
    for l in range(305, 336):
        novOptimalValues.append(novOptimalVs[l])
    for l in range(335, 366):
        decOptimalValues.append(decOptimalVs[l])
    
else:
    febOptimalVs.insert(59, "0")
    febOptimalVs.insert(60, "0")
    febOptimalVs.insert(61, "0")
    aprOptimalVs.insert(120, "0")
    junOptimalVs.insert(181, "0")
    sepOptimalVs.insert(273, "0")
    novOptimalVs.insert(334, "0") 
    
    for l in range(31, 62):
        febOptimalValues.append(febOptimalVs[l])
    for l in range(59, 90):
        marOptimalValues.append(marOptimalVs[l])
    for l in range(90, 121):
        aprOptimalValues.append(aprOptimalVs[l])
    for l in range(120, 151):
        mayOptimalValues.append(mayOptimalVs[l])
    for l in range(151, 182):
        junOptimalValues.append(junOptimalVs[l])
    for l in range(181, 212):
        julOptimalValues.append(julOptimalVs[l])
    for l in range(212, 243):
        augOptimalValues.append(augOptimalVs[l])
    for l in range(243, 274):
        sepOptimalValues.append(sepOptimalVs[l])
    for l in range(273, 304):
        octOptimalValues.append(octOptimalVs[l])
    for l in range(304, 335):
        novOptimalValues.append(novOptimalVs[l])
    for l in range(334, 365):
        decOptimalValues.append(decOptimalVs[l])

#----Clean list of lists containing the 12 lists of decision variables-----    
optimalValues = [janOptimalVs, febOptimalValues, marOptimalValues, aprOptimalValues, mayOptimalValues, junOptimalValues, julOptimalValues, augOptimalValues, sepOptimalValues, octOptimalValues, novOptimalValues, decOptimalValues]

#-----Output GUI window----
class SimpleTableInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        
        root.title("Output")
        
        self._entry = {}
        self.rows = rows
        self.columns = columns

        # create the table of widgets
        for column in range(self.columns):
            for row in range(self.rows):
                #------Month Labels---------
                labelMonth = tk.Label(self, text=str(listOfMonths[column]))
                labelMonth.grid(row=0, column=column+1)
                
                #------Display Vars---------
                index = (row+1, column)
                e = tk.Label(self, text = str(optimalValues[column][row]))
                e.grid(row=row+1, column=column+1, stick="nsew")
                self._entry[index] = e
      
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column+1, weight=1)
            
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(rows+1, weight=1)
  

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.table = SimpleTableInput(self, 31, 12)
        self.table.pack(side="top")
        
root = tk.Tk()
Example(root).pack(side="top")
root.mainloop()
  
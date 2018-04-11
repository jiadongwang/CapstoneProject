from gurobipy import *
n = Model()
from math import *
from scipy.stats import norm
import matplotlib.pyplot as plt
import pickle
try:
    from tkinter import *
    from ttk import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk

#-----Initilizations for the GUI----
innerList = []
innerList2 = []
saveList = []
loadList = []
global buttonClicks
buttonClicks = 0
listOfMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
                'August', 'September', 'October', 'November', 'December']

#-----First GUI window-----
class SimpleTableInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        
        root.title("User Input")
        
        self._entry = {}
        self.rows = rows
        self.columns = columns 
        self.default = ttk.Button(self, text="Default", command=self.autofill)
        self.default.grid(row=9,column=0)
        self.loadValues = ttk.Button(self, text="Load Values", 
                                     command=self.load_save)
        self.loadValues.grid(row=9,column=1)

        
        #-----Default values-----
        self.LookUpList=[2019,0.85,9,2,300,20,3000,200]
        
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
                enterRely = tk.Label(self, text=
                    "Enter the reliability (must be a value between 0 and 1)")
                enterRely.grid(row=1, column=0, sticky=W)
                enterMaxDays = tk.Label(self, text=
    "Enter the maximum number of vacation days allotted for any given day")
                enterMaxDays.grid(row=2, column=0, sticky=W)
                enterMinDays = tk.Label(self, text=
    "Enter the minimum number of vacation days allotted for any given day")
                enterMinDays.grid(row=3, column=0, sticky=W)
                enterMaxMonth = tk.Label(self, text=
            "Enter the maximum number of vacation days for any given month")
                enterMaxMonth.grid(row=4, column=0, sticky=W)
                enterMinMonth = tk.Label(self, text=
            "Enter the minimum number of vacation days for any given month")
                enterMinMonth.grid(row=5, column=0, sticky=W)
                enterMaxYear = tk.Label(self, text=
            "Enter the maximum number of vacation days allotted for the year")
                enterMaxYear.grid(row=6, column=0, sticky=W)
                enterMinYear = tk.Label(self, text=
            "Enter the minimum number of vacation days allotted for the year")
                enterMinYear.grid(row=7, column=0, sticky=W)
                self._entry[index] = e
                
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column+1, weight=1)
            
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(rows, weight=1)
            

        #Return a list containing the data in the table
    def get(self):
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column+1)
                innerList.append(float(self._entry[index].get()))
        return innerList
    
    #-----Fill table with default values------
    def autofill(self):
        for row in range(self.rows):
            self._entry[row,1].delete(0, END)
            self._entry[row,1].insert(row, str(self.LookUpList[row]))
            
    def load_save(self): 
        loadList = []
        with open('save_file.db', 'rb') as file:
            while True:
                try:
                    loadList=pickle.load(file)
                except EOFError:
                    break
        for row in range(self.rows):
            self._entry[row,1].delete(0, END)
            self._entry[row,1].insert(row, str(loadList[0][row]))
    #Perform input validation. 
    def _validate(self, P):
        
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
        self.table = SimpleTableInput(self, 8, 1)
        self.submit = ttk.Button(self, text="Submit", command=self.on_submit)
        self.table.pack(side="top")
        self.submit.pack(side='bottom')  
        self.saveValues = ttk.Button(self, text="Save Values", 
                                     command=self.save_values)
        self.saveValues.place(x=405,y=193) 
        
    def on_submit(self):
        innerList.append(self.table.get())
        root.destroy()
        
    def save_values(self):
        saveList = []
        saveList.append(self.table.get())
        with open('save_file.db', 'wb+') as file2:
            pickle.dump(saveList, file2)
                
root = tk.Tk()
Example(root).pack(side="top")
root.mainloop()

#-----Fill in variables with inputs from user-----
for m in range(8):
    if m == 0:
        currentYear = int(innerList[m])
    elif m == 1:
        reliabilityLevel = float(innerList[m])
    elif m == 2:
        dailyUpperBoundVacationAllotted = int(innerList[m])
    elif m == 3:
        dailyLowerBoundVacationAllotted = int(innerList[m])
    elif m == 4:
        userMonthlyUpperBoundVacationAllotted = int(innerList[m])
    elif m == 5:
        monthlyLowerBoundVacationAllotted = int(innerList[m])
    elif m == 6:
        userAnnualUpperBoundVacationAllotted = int(innerList[m])
    else:
        annualLowerBoundVacationAllotted = int(innerList[m])


#-----Second GUI window-----
class SimpleTableInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        
        root.title("User Input")
        
        self._entry = {}
        self.rows = rows
        self.columns = columns
        self.default = ttk.Button(self, text="Default", command=self.autofill)
        self.loadValues = ttk.Button(self, text="Load Values", 
                                     command=self.load_save)
        self.default.grid(row=6,column=5)
        self.loadValues.grid(row=6,column=7)
        
        #-----Default values-----
        self.LookUpList=[
                    [700,700,700,700,700,700,700,700,700,700,700,700],
                    [476,432,469,447,465,481,475,482,436,460,480,478],
                    [49.8,32.1,48.4,35.3,42.4,45.3,47.0,40.0,35.8,41.0,46.7,
                     55.7],
                    [95.8,84.6,98.2,88.7,92.4,97.4,100.0,98.0,86.7,83.2,84.6,
                     91.0]]
                
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
     
    #-----Fill table with default values------    
    def autofill(self):
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row+1, column+1)
                self._entry[index].delete(0, END)
                self._entry[index].insert(0, str(self.LookUpList[row][column]))
            
    def load_save(self):
        loadList = []
        with open('save_file2.p', 'rb') as file2:
            loadList = pickle.load(file2)
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row+1, column+1)
                self._entry[index].delete(0, END)
                self._entry[index].insert(0, str(loadList[0][column+row*12]))

    def get(self):
        #Return a list of lists, containing the data in the table
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row+1, column+1)
                innerList2.append(float(self._entry[index].get()))
        return innerList2
    #Perform input validation. 
    def _validate(self, P):
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
        self.submit = ttk.Button(self, text="Submit", command=self.on_submit)
        self.table.pack(side="top")
        self.submit.pack(side="bottom")
        self.saveValues = ttk.Button(self, text="Save Values", 
                                     command=self.save_values)
        self.saveValues.place(x=758,y=130)
        
    def on_submit(self):
        innerList2.append(self.table.get())
        root.destroy()
          
    def save_values(self):
        saveList = []
        saveList.append(self.table.get())
        with open('save_file2.p', 'wb+') as file2:
            pickle.dump(saveList, file2)

root = tk.Tk()
Example(root).pack(side="top")
root.mainloop()


inverseNormalReliability = norm.ppf(reliabilityLevel)

#-----Indexing for filling in variables based on user data 
#      from the second GUI window-----
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

daysInYear = [LongMonthLength, FebruaryLength, LongMonthLength, 
              ShortMonthLength, LongMonthLength, ShortMonthLength, 
              LongMonthLength, LongMonthLength, ShortMonthLength, 
              LongMonthLength, ShortMonthLength, LongMonthLength]

#-----monthly line holders, crew scheduled, averges provided, 
#      variances provided, and the difference between monthlyLineHolders 
#      and monthlyCrew-----
monthlyLineHolders = [] 
for m in range(12):
       monthlyLineHolders.append(int(innerList2[m])) 
       

monthlyCrewScheduled = [] 
for m in ListAppend1:
       monthlyCrewScheduled.append(int(innerList2[m])) 


averageMonthlyExpectedAbsences = []
for m in ListAppend2:
       averageMonthlyExpectedAbsences.append(float(innerList2[m])) 


varOfMonthlyExpectedAbsences = []
for m in ListAppend3:
       varOfMonthlyExpectedAbsences.append(float(innerList2[m])) 

#-----Calculating the standard deviations based on given variances-----    
stdDevMonthlyExpectedAbsences = []
for m in Months:
    stdDevOfAbsences = sqrt(varOfMonthlyExpectedAbsences[m])
    stdDevMonthlyExpectedAbsences.append(stdDevOfAbsences)

#-----Calculating the expected absences for each month based on the average 
#      absences, std. dev. of absences, and the reliability level-----
expectedMonthlyAbsences = []
for m in Months:
    expectedAbsenses = inverseNormalReliability * stdDevMonthlyExpectedAbsences[m] + averageMonthlyExpectedAbsences[m]
    expectedMonthlyAbsences.append(expectedAbsenses)

#-----By subtracting crew scheduled from line holders, we're left with a 
#      variable that represents vacation days plus expected absences-----
vacationAllottedPlusExpectedAbsences = [(monthlyLineHolders[m]-monthlyCrewScheduled[m]) for m in Months]

#-----Calculated monthly upper bound based on subtracting expected absences 
#      subtracted from vacation days plus expected absences-----
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
    vacationVariable.append(n.addVars(daysInMonths[m], 
                                      lb = dailyLowerBoundVacationAllotted, 
                                      ub = dailyUpperBoundVacationAllotted, 
                                      obj = 1, name = "Month" + str(m)))

#-----implementing monthly contraints-----
for m in Months:
       n.addConstr(vacationVariable[m].sum() <= monthlyUpperBoundVacationAllotted[m], 
                   name = "monthlyUpperBoundVacationAllottedForMonth" + str(m))
for m in Months:
       n.addConstr(vacationVariable[m].sum() <= userMonthlyUpperBoundVacationAllotted, 
                   name = "userMonthlyUpperBoundVacationAllottedForMonth" + str(m))
for m in Months:
    n.addConstr(vacationVariable[m].sum() >= monthlyLowerBoundVacationAllotted, 
                name = "monthlyLowerBoundVacationAllotted" + str(m))   

#-----calculating the objective value-----
totalObjectiveValue = 0
for m in Months:
    objectiveValue = 0
    objectiveValue = vacationVariable[m].sum()
    totalObjectiveValue = totalObjectiveValue + objectiveValue

#-----implementing annual constraints-----
n.addConstr(totalObjectiveValue <= annualUpperBoundVacationAllotted, 
            name = "TotannualUpperBoundVacationAllotted") 
n.addConstr(totalObjectiveValue <= userAnnualUpperBoundVacationAllotted, 
            name = "userTotannualUpperBoundVacationAllotted") 
n.addConstr(totalObjectiveValue >= annualLowerBoundVacationAllotted, 
            name = "TotannualLowerBoundVacationAllotted")

#-----Objective function-----
for m in Months:
    n.setObjective(totalObjectiveValue, GRB.MAXIMIZE)

#-----execute optimization-----
n.update()
n.optimize()

#-----Creating files with the deatils of the formulation and optimization for 
#      further inspection/review-----
n.write('sabre2.sol')
n.write("out.lp")
n.write("outs.mps")

#-----initializing lists for extracting the post-optimization decision 
#      variable values-----
decisionVariables = []
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

#-----Extracting a clean list of the decision variables-----
for l in n.getVars():
    decisionVariables.append(int(l.x))

#-----Seperating the decision variables into months-----
if numberOfDays == 366:
    for l in range(366):
        if 0<=l<=30:    
            janOptimalVs.append(decisionVariables[l])
        elif 31<=l<=59:
            febOptimalVs.append(decisionVariables[l])
        elif 60<=l<=90:
            marOptimalVs.append(decisionVariables[l])
        elif 91<=l<=120:
            aprOptimalVs.append(decisionVariables[l])
        elif 121<=l<=151:
            mayOptimalVs.append(decisionVariables[l])
        elif 152<=l<=181:
            junOptimalVs.append(decisionVariables[l])
        elif 182<=l<=212:
            julOptimalVs.append(decisionVariables[l])
        elif 213<=l<=243:
            augOptimalVs.append(decisionVariables[l])
        elif 244<=l<=273:
            sepOptimalVs.append(decisionVariables[l])
        elif 274<=l<=304:
            octOptimalVs.append(decisionVariables[l])
        elif 305<=l<=334:
            novOptimalVs.append(decisionVariables[l])
        else:
            decOptimalVs.append(decisionVariables[l])
#-----making each list 31 values long-----
    febOptimalVs.insert(29, 0)
    febOptimalVs.insert(30, 0)
    aprOptimalVs.insert(30, 0)
    junOptimalVs.insert(30, 0)
    sepOptimalVs.insert(30, 0)
    novOptimalVs.insert(30, 0)
    
elif numberOfDays == 365:
    for l in range(365):
        if 0<=l<=30:    
            janOptimalVs.append(decisionVariables[l])
        elif 31<=l<=58:
            febOptimalVs.append(decisionVariables[l])
        elif 59<=l<=89:
            marOptimalVs.append(decisionVariables[l])
        elif 90<=l<=119:
            aprOptimalVs.append(decisionVariables[l])
        elif 120<=l<=150:
            mayOptimalVs.append(decisionVariables[l])
        elif 151<=l<=180:
            junOptimalVs.append(decisionVariables[l])
        elif 181<=l<=211:
            julOptimalVs.append(decisionVariables[l])
        elif 212<=l<=242:
            augOptimalVs.append(decisionVariables[l])
        elif 243<=l<=272:
            sepOptimalVs.append(decisionVariables[l])
        elif 273<=l<=303:
            octOptimalVs.append(decisionVariables[l])
        elif 304<=l<=333:
            novOptimalVs.append(decisionVariables[l])
        else:
            decOptimalVs.append(decisionVariables[l])

    febOptimalVs.insert(28, 0)
    febOptimalVs.insert(29, 0)
    febOptimalVs.insert(30, 0)
    aprOptimalVs.insert(30, 0)
    junOptimalVs.insert(30, 0)
    sepOptimalVs.insert(30, 0)
    novOptimalVs.insert(30, 0) 

#-----list of lists containing the decision variables sperated by month-----
optimalValues = [janOptimalVs, febOptimalVs, marOptimalVs, aprOptimalVs, 
                 mayOptimalVs, junOptimalVs, julOptimalVs, augOptimalVs, 
                 sepOptimalVs, octOptimalVs, novOptimalVs, decOptimalVs]

#-----Initialization for totaling the decision variables for each month-----
janTotal = 0
febTotal = 0
marTotal = 0
aprTotal = 0
mayTotal = 0
junTotal = 0
julTotal = 0
augTotal = 0
sepTotal = 0
octTotal = 0
novTotal = 0
decTotal = 0

#-----Totaling the decision variables for each month-----
for m in Months:
    for l in range(31):
        if m == 0:
            janTotal += janOptimalVs[l]
        elif m == 1:
            febTotal += febOptimalVs[l]
        elif m == 2:
            marTotal += marOptimalVs[l]
        elif m == 3:
            aprTotal += aprOptimalVs[l]
        elif m == 4:
            mayTotal += mayOptimalVs[l]
        elif m == 5:
            junTotal += junOptimalVs[l]
        elif m == 6:
            julTotal += julOptimalVs[l]
        elif m == 7:
            augTotal += augOptimalVs[l]
        elif m == 8:
            sepTotal += sepOptimalVs[l]
        elif m == 9:
            octTotal += octOptimalVs[l]
        elif m == 10:
            novTotal += novOptimalVs[l]
        else:
            decTotal += decOptimalVs[l]
            
#-----list of monthly totals-----
optimalValuesMonths = [janTotal, febTotal, marTotal, aprTotal, mayTotal, 
                       junTotal, julTotal, augTotal, sepTotal, octTotal, 
                       novTotal, decTotal]

#-----initial bar chart-----
plt.bar(range(1,13), optimalValuesMonths)
plt.xlabel('Month')
plt.ylabel('Vacation Days')
plt.title('Vacation Days per Month')
plt.show()

#-----Output GUI window-----
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
  
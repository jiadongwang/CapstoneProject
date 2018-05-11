from gurobipy import *
n = Model()

from math import *
from scipy.stats import norm
import pickle
import os

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")

try:
    from tkinter import *
    from ttk import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk

#-----Initilizations for various GUI methods----
innerList = []
innerList2 = []
innerList3 = []
innerList4 = []
saveList = []
saveList2 = []
saveList3 = []
saveList4 = []
loadList = []
loadList2 = []
loadList3 = []
loadList4 = []
listOfMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
                'August', 'September', 'October', 'November', 'December']

#-----Part 1, Initial values--------------------------------------------------
#-----Part 1, Initial values--------------------------------------------------
#-----Part 1, Initial values--------------------------------------------------
#-----First GUI window-----
class SimpleTableInput1(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        #-----Title-----
        root.title("Reliability Data Driven Vacation Allocation Optimizer")
        #-----Icon-----
        root.wm_iconbitmap("OSabreIcon.ico")
        #-----Initializations-----
        self._entry = {}
        self.rows = rows
        self.columns = columns 
        #-----"Default" button-----
        self.default = ttk.Button(self, text="Default", command=self.autofill)
        self.default.grid(row=9,column=0)
        #-----"Load Values" button-----
        self.loadValues = ttk.Button(self, text="Load Values", 
                                     command=self.load_save)
        self.loadValues.grid(row=9,column=1)

        #-----Default values-----
        self.LookUpList=[2019,0.85,9,2,300,20,3000,200]
        
        #-----register a command to use for validation-----
        vcmd = (self.register(self._validate), "%P")

        #-----create the table of widgets-----
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
                
        #-----adjust column weights so they all expand equally-----
        for column in range(self.columns):
            self.grid_columnconfigure(column+1, weight=1)
            
        #-----designate a final, empty row to fill up any extra space-----
        self.grid_rowconfigure(rows, weight=1)
            

    #-----Return a list containing the data in the table-----
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
            
    #-----"Load Values" button function-----      
    def load_save(self): 
        loadList = []
        subLoadList = []
        with open('save_file.db', 'rb') as file:
            while True:
                try:
                    loadList=pickle.load(file)
                    y = len(loadList)
                    x = y-9
                    for m in range(8):
                        subLoadList.append(loadList[0][m+x])
                except EOFError:
                    break
        for row in range(self.rows):
            self._entry[row,1].delete(0, END)
            self._entry[row,1].insert(row, str(subLoadList[row]))
            
    #-----Perform input validation-----
    def _validate(self, P):
        #-----Allow only an empty value, or a value that can be converted to 
        #      a float-----
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
        #-----Table-----
        self.table = SimpleTableInput1(self, 8, 1)
        self.table.pack(side="top")
        #-----"Submit" button-----
        self.submit = ttk.Button(self, text="Submit", command=self.on_submit)
        self.submit.pack(side='bottom') 
        #-----"Save Values" button-----
        self.saveValues = ttk.Button(self, text="Save Values", 
                                     command=self.save_values)
        self.saveValues.place(x=405,y=193) 

    #-----"Submit" button function-----    
    def on_submit(self):
        innerList.append(self.table.get())
        root.destroy()
    
    #-----"Save Values" button function-----    
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
class SimpleTableInput2(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        #-----Title-----
        root.title("Reliability Data Driven Vacation Allocation Optimizer")
       #-----Icon-----
        root.wm_iconbitmap("OSabreIcon.ico")
        #-----Initializations-----
        self._entry = {}
        self.rows = rows
        self.columns = columns
        #-----"Default" button-----
        self.default = ttk.Button(self, text="Default", command=self.autofill)
        self.default.grid(row=6,column=5)
        #-----"Load Values" button-----
        self.loadValues = ttk.Button(self, text="Load Values", 
                                     command=self.load_save)
        self.loadValues.grid(row=6,column=7)
        
        #-----Default values-----
        self.LookUpList=[
                    [700,700,700,700,700,700,700,700,700,700,700,700],
                    [476,432,469,447,465,481,475,482,436,460,480,478],
                    [49.8,32.1,48.4,35.3,42.4,45.3,47.0,40.0,35.8,41.0,46.7,
                     55.7],
                    [95.8,84.6,98.2,88.7,92.4,97.4,100.0,98.0,86.7,83.2,84.6,
                     91.0]]
                
        #-----register a command to use for validation-----
        vcmd = (self.register(self._validate), "%P")

        #-----create the table of widgets-----
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
                
        #-----adjust column weights so they all expand equally-----
        for column in range(self.columns):
            self.grid_columnconfigure(column+1, weight=1)
            
        #-----designate a final, empty row to fill up any extra space-----
        self.grid_rowconfigure(rows+1, weight=1)
     
    #-----Fill table with default values------    
    def autofill(self):
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row+1, column+1)
                self._entry[index].delete(0, END)
                self._entry[index].insert(0, str(self.LookUpList[row][column]))
                
    #-----"Load Values" button function-----         
    def load_save(self):
        loadList2 = []
        subLoadList = []
        with open('save_file2.p', 'rb') as file2:
            loadList2=pickle.load(file2)
            y = len(loadList2)
            x = y-49
            for m in range(48):
                subLoadList.append(loadList2[0][m+x])
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row+1, column+1)
                self._entry[index].delete(0, END)
                self._entry[index].insert(0, str(subLoadList[column+row*12]))
                
    #-----Return a list of lists, containing the data in the table------
    def get(self):
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row+1, column+1)
                innerList2.append(float(self._entry[index].get()))
        return innerList2
    
    #-----Perform input validation-----
    def _validate(self, P):
        #-----Allow only an empty value, or a value that can be converted to 
        #      a float-----
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
        #-----Table-----
        self.table = SimpleTableInput2(self, 4, 12)
        self.table.pack(side="top")
        #-----"Submit" button-----
        self.submit = ttk.Button(self, text="Submit", command=self.on_submit)
        self.submit.pack(side="bottom")
        #-----"Save Values" button-----
        self.saveValues = ttk.Button(self, text="Save Values", 
                                     command=self.save_values)
        self.saveValues.place(x=558,y=130)
    
    #-----"Submit" button function-----     
    def on_submit(self):
        innerList2.append(self.table.get())
        root.destroy()
        
    #-----"Save Values" button function-----           
    def save_values(self):
        saveList2 = []
        saveList2.append(self.table.get())
        with open('save_file2.p', 'wb+') as file2:
            pickle.dump(saveList2, file2)

root = tk.Tk()
Example(root).pack(side="top")
root.geometry('1000x158')
root.mainloop()

#-----Part 2, First optimization----------------------------------------------
#-----Part 2, First optimization----------------------------------------------
#-----Part 2, First optimization----------------------------------------------
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

#-----Monthly line holders, crew scheduled, averges provided, 
#      variances provided, and the difference between monthlyLineHolders 
#      and monthlyCrew-----
monthlyLineHolders = [] 
for m in range(12):
       monthlyLineHolders.append(int(innerList2[m])) 
       

monthlyCrewScheduled = [] 
for m in ListAppend1:
       monthlyCrewScheduled.append(int(innerList2[m])) 


averageMonthlyAbsences = []
for m in ListAppend2:
       averageMonthlyAbsences.append(float(innerList2[m])) 


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
    expectedAbsenses = inverseNormalReliability * stdDevMonthlyExpectedAbsences[m] + averageMonthlyAbsences[m]
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
                                      obj = 1, name = listOfMonths[m]))

#-----Implementing monthly contraints-----
for m in Months:
       n.addConstr(vacationVariable[m].sum() <= monthlyUpperBoundVacationAllotted[m], 
                   name = "MonthlyUpperBoundVacationAllottedFor" + listOfMonths[m])
for m in Months:
       n.addConstr(vacationVariable[m].sum() <= userMonthlyUpperBoundVacationAllotted, 
                   name = "userMonthlyUpperBoundVacationAllottedFor" + listOfMonths[m])
for m in Months:
    n.addConstr(vacationVariable[m].sum() >= monthlyLowerBoundVacationAllotted, 
                name = "monthlyLowerBoundVacationAllottedFor" + listOfMonths[m])   

#-----Calculating the objective value-----
totalObjectiveValue = 0
for m in Months:
    objectiveValue = 0
    objectiveValue = vacationVariable[m].sum()
    totalObjectiveValue = totalObjectiveValue + objectiveValue

#-----Implementing annual constraints-----
n.addConstr(totalObjectiveValue <= annualUpperBoundVacationAllotted, 
            name = "TotalAnnualUpperBoundVacationAllotted") 
n.addConstr(totalObjectiveValue <= userAnnualUpperBoundVacationAllotted, 
            name = "UserTotalAnnualUpperBoundVacationAllotted") 
n.addConstr(totalObjectiveValue >= annualLowerBoundVacationAllotted, 
            name = "TotalAnnualLowerBoundVacationAllotted")

#-----Objective function-----
for m in Months:
    n.setObjective(totalObjectiveValue, GRB.MAXIMIZE)

#-----Execute optimization-----
n.update()
n.optimize()

#-----Creating files with the deatils of the formulation and optimization for 
#      further inspection/review-----
n.write('SolutionList1.sol')
n.write("SimpleModel1.lp")
n.write("DetailedModel1.mps")

#-----Scatter plot-----
standRelyLevels = [.5,.52,.54,.56,.58,.60,.62,.64,.66,.68,.70,.72,.74,.76,.78,
                   .80,.82,.84,.86,.88,.90,.92,.94,.96,.98]
standInverseNorm =[]

for l in range(25):
    tempCalculation = 0
    tempCalculation = norm.ppf(standRelyLevels[l])
    standInverseNorm.append(tempCalculation)
    
newDevAndVacation = []

for m in Months:
    newDevAndVacation.append(vacationAllottedPlusExpectedAbsences[m]-averageMonthlyAbsences[m])
    
scatterPlotValues = []
    
for l in range(25):
    tempTotalList = []
    for m in Months:
        tempCalculation = newDevAndVacation[m] - stdDevMonthlyExpectedAbsences[m]*standInverseNorm[l]
        tempTotalList.append(tempCalculation)
        if tempTotalList[m] > userMonthlyUpperBoundVacationAllotted:
            tempTotalList[m] = userMonthlyUpperBoundVacationAllotted
        else:
            pass
        if tempTotalList[m] < monthlyLowerBoundVacationAllotted:
            tempTotalList[m] = monthlyLowerBoundVacationAllotted
        else:
            pass
        if tempTotalList[m] > dailyUpperBoundVacationAllotted*daysInMonths[m]:
            tempTotalList[m] = dailyUpperBoundVacationAllotted*daysInMonths[m]
        else:
           pass
        if tempTotalList[m] < dailyLowerBoundVacationAllotted*daysInMonths[m]:
          tempTotalList[m] = dailyLowerBoundVacationAllotted*daysInMonths[m]
        else:
           pass
        if len(tempTotalList) == 12:
            tempCalculation = sum(tempTotalList)
            scatterPlotValues.append(trunc(tempCalculation))
        else:
            pass
    if scatterPlotValues[l] > userAnnualUpperBoundVacationAllotted:
        scatterPlotValues[l] = userAnnualUpperBoundVacationAllotted
    else:
        pass
    if scatterPlotValues[l] < annualLowerBoundVacationAllotted:  
           scatterPlotValues[l] = annualLowerBoundVacationAllotted
    else:
        pass         

#-----Initializing lists for extracting the post-optimization decision 
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
#-----Making each list 31 values long-----
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

#-----List of lists containing the decision variables sperated by month-----
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
            
#-----List of monthly totals-----
optimalValuesMonths = [janTotal, febTotal, marTotal, aprTotal, mayTotal, 
                       junTotal, julTotal, augTotal, sepTotal, octTotal, 
                       novTotal, decTotal]
tempTotal = 0
for m in Months:
    tempTotal += optimalValuesMonths[m]

#-----Part 3, First Menu-----------------------------------------------------
#-----Part 3, First Menu-----------------------------------------------------
#-----Part 3, First Menu-----------------------------------------------------
#-----First Menu-----
class SaberApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        root.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand='true')
        
        #-----Icon-----
        root.iconbitmap(self, "OSabreIcon.ico")
        root.wm_title(self, "Reliability Data Driven Vacation Allocation Optimizer")
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (StartPage, Histogram, Scatterplot):

            frame = F(container, self)
                
            self.frames[F] = frame
                
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Menu")
        label.pack(side = 'top', pady=10, padx=10)
        
        
        self.HistButton = ttk.Button(self, text='Bar Chart', command=lambda: controller.show_frame(Histogram))
        self.HistButton.pack(side='top')
        
        self.ScatterButton = ttk.Button(self, text='Scatter Plot', command=lambda: controller.show_frame(Scatterplot))
        self.ScatterButton.pack(side='top', pady=10)
        
        self.ScatterButton = ttk.Button(self, text='Write Results', command=self.Writefile)
        self.ScatterButton.pack(side='top')
       
        self.Opt2Button = ttk.Button(self, text='  Secondary\nOptimization', command=self.SecondOpt)
        self.Opt2Button.pack(side='top', pady=10)
        
        self.ExitButton = ttk.Button(self, text='Exit Program', command=self.Exit)
        self.ExitButton.pack(side='top')

    def Writefile(self):
        with open('Optimization Results.txt', 'w') as file3:
            file3.write("Results of the initial optimization.\n\nThe total number of vacation days for the year is ")
            file3.write(str(tempTotal))
            file3.write(".\n\n")
            for m in Months:
                file3.write("The optimal value for ")
                file3.write(listOfMonths[m])
                file3.write(" is ")
                file3.write(str(optimalValuesMonths[m]))
                file3.write(".\n")
            
    def SecondOpt(self):
        App.destroy() 
            
    def Exit(self):
        os._exit(1)
    
class Histogram(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Bar Chart")
        label.pack(side = 'top', pady=10, padx=10)
        
        self.MenuButton = ttk.Button(self, text='Menu', command=lambda: controller.show_frame(StartPage))
        self.MenuButton.pack(side='top')
        
        f = Figure(figsize = (8,5), dpi = 100)
        a = f.add_subplot(111)
        
        xList = []
        yList = []
        for m in Months:
            xList.append(m+1)
            yList.append(int(optimalValuesMonths[m]))
        a.clear()
        a.bar(xList, yList, label = "Initial Optimization")
        
        a.legend(bbox_to_anchor=(0, 1.08, 2, .102), loc=3,
                 ncol=2, borderaxespad=0)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        a.set_title("Vacation Days per Month")
        a.set_xlabel("Month")
        a.set_ylabel("Vacation Days")
        
class Scatterplot(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Scatter Plot")
        label.pack(side = 'top', pady=10, padx=10)
        
        self.MenuButton = ttk.Button(self, text='Menu', command=lambda: controller.show_frame(StartPage))
        self.MenuButton.pack(side='top')
        
        f = Figure(figsize = (8,5), dpi = 100)
        a = f.add_subplot(111)
        
        a.clear()
        a.scatter(standRelyLevels, scatterPlotValues, label = "Initial Optimization")
        
        a.legend(bbox_to_anchor=(0, 1.08, 1, .102), loc=3,
                 ncol=2, borderaxespad=0)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        a.set_title("Annual Vacation Days vs. Reliability Level")
        a.set_xlabel("Reliability Level")
        a.set_ylabel("Annual Vacation Days")   
 
root = tk.Tk
App = SaberApp()
App.mainloop()


#-----Part 4, Secondary values-----------------------------------------------
#-----Part 4, Secondary values-----------------------------------------------
#-----Part 4, Secondary values-----------------------------------------------
#-----Second Parameter GUI window-----
class SimpleTableInput3(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        #-----Title-----
        root.title("Reliability Data Driven Vacation Allocation Optimizer")
        #-----Icon-----
        root.wm_iconbitmap("OSabreIcon.ico")
        #-----Initializations-----
        self._entry = {}
        self.rows = rows
        self.columns = columns 
        #-----"Default" button-----
        self.default = ttk.Button(self, text="Default", command=self.autofill)
        self.default.grid(row=9,column=0)
        #-----"Load Values" button-----
        self.loadValues = ttk.Button(self, text="Load Values", 
                                     command=self.load_save)
        self.loadValues.grid(row=9,column=1)

        #-----Default values-----
        self.LookUpList=[2019,0.85,9,2,300,20,3000,200]
        
        #-----register a command to use for validation-----
        vcmd = (self.register(self._validate), "%P")

        #-----create the table of widgets-----
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
                
        #-----adjust column weights so they all expand equally-----
        for column in range(self.columns):
            self.grid_columnconfigure(column+1, weight=1)
            
        #-----designate a final, empty row to fill up any extra space-----
        self.grid_rowconfigure(rows, weight=1)
            

    #-----Return a list containing the data in the table-----
    def get(self):
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column+1)
                innerList3.append(float(self._entry[index].get()))
        return innerList3
    
    #-----Fill table with default values------
    def autofill(self):
        for row in range(self.rows):
            self._entry[row,1].delete(0, END)
            self._entry[row,1].insert(row, str(self.LookUpList[row]))
            
    #-----"Load Values" button function-----      
    def load_save(self): 
        loadList3 = []
        subLoadList =[]
        with open('save_file3.db', 'rb') as file:
            while True:
                try:
                    loadList3=pickle.load(file)
                    y = len(loadList3)
                    x = y-9
                    for m in range(8):
                        subLoadList.append(loadList3[0][m+x])
                except EOFError:
                    break
        for row in range(self.rows):
            self._entry[row,1].delete(0, END)
            self._entry[row,1].insert(row, str(subLoadList[row]))
            
    #-----Perform input validation-----
    def _validate(self, P):
        #-----Allow only an empty value, or a value that can be converted to 
        #      a float-----
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
        #-----Table-----
        self.table = SimpleTableInput3(self, 8, 1)
        self.table.pack(side="top")
        #-----"Submit" button-----
        self.submit = ttk.Button(self, text="Submit", command=self.on_submit)
        self.submit.pack(side='bottom') 
        #-----"Save Values" button-----
        self.saveValues = ttk.Button(self, text="Save Values", 
                                     command=self.save_values)
        self.saveValues.place(x=405,y=193) 
    
    #-----"Submit" button function-----    
    def on_submit(self):
        innerList3.append(self.table.get())
        root.destroy()
    
    #-----"Save Values" button function-----    
    def save_values(self):
        saveList3 = []
        saveList3.append(self.table.get())
        with open('save_file3.db', 'wb+') as file2:
            pickle.dump(saveList3, file2)
                
root = tk.Tk()
Example(root).pack(side="top")
root.mainloop()

#-----Fill in variables with inputs from user-----
for m in range(8):
    if m == 0:
        currentYear2 = int(innerList3[m])
    elif m == 1:
        reliabilityLevel2 = float(innerList3[m])
    elif m == 2:
        dailyUpperBoundVacationAllotted2 = int(innerList3[m])
    elif m == 3:
        dailyLowerBoundVacationAllotted2 = int(innerList3[m])
    elif m == 4:
        userMonthlyUpperBoundVacationAllotted2 = int(innerList3[m])
    elif m == 5:
        monthlyLowerBoundVacationAllotted2 = int(innerList3[m])
    elif m == 6:
        userAnnualUpperBoundVacationAllotted2 = int(innerList3[m])
    else:
        annualLowerBoundVacationAllotted2 = int(innerList3[m])


#-----Second Crew GUI window-----
class SimpleTableInput4(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        #-----Title-----
        root.title("Reliability Data Driven Vacation Allocation Optimizer")
        #-----Icon-----
        root.wm_iconbitmap("OSabreIcon.ico")
        #-----Initializations-----
        self._entry = {}
        self.rows = rows
        self.columns = columns
        #-----"Default" button-----
        self.default = ttk.Button(self, text="Default", command=self.autofill)
        self.default.grid(row=6,column=5)
        #-----"Load Values" button-----
        self.loadValues = ttk.Button(self, text="Load Values", 
                                     command=self.load_save)
        self.loadValues.grid(row=6,column=7)
        
        #-----Default values-----
        self.LookUpList=[
                    [700,700,700,700,700,700,700,700,700,700,700,700],
                    [476,432,469,447,465,481,475,482,436,460,480,478],
                    [49.8,32.1,48.4,35.3,42.4,45.3,47.0,40.0,35.8,41.0,46.7,
                     55.7],
                    [95.8,84.6,98.2,88.7,92.4,97.4,100.0,98.0,86.7,83.2,84.6,
                     91.0]]
                
        #-----register a command to use for validation-----
        vcmd = (self.register(self._validate), "%P")

        #-----create the table of widgets-----
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
                
        #-----adjust column weights so they all expand equally-----
        for column in range(self.columns):
            self.grid_columnconfigure(column+1, weight=1)
            
        #-----designate a final, empty row to fill up any extra space-----
        self.grid_rowconfigure(rows+1, weight=1)
     
    #-----Fill table with default values------    
    def autofill(self):
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row+1, column+1)
                self._entry[index].delete(0, END)
                self._entry[index].insert(0, str(self.LookUpList[row][column]))
                
    #-----"Load Values" button function-----         
    def load_save(self):
        loadList4 = []
        subLoadList = []
        with open('save_file4.p', 'rb') as file2:
            loadList4=pickle.load(file2)
            y = len(loadList4)
            x = y-49
            for m in range(48):
                subLoadList.append(loadList4[0][m+x])
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row+1, column+1)
                self._entry[index].delete(0, END)
                self._entry[index].insert(0, str(subLoadList[column+row*12]))
                
    #-----Return a list of lists, containing the data in the table------
    def get(self):
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row+1, column+1)
                innerList4.append(float(self._entry[index].get()))
        return innerList4
    
    #-----Perform input validation-----
    def _validate(self, P):
        #-----Allow only an empty value, or a value that can be converted to 
        #      a float-----
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
        #-----Table-----
        self.table = SimpleTableInput4(self, 4, 12)
        self.table.pack(side="top")
        #-----"Submit" button-----
        self.submit = ttk.Button(self, text="Submit", command=self.on_submit)
        self.submit.pack(side="bottom")
        #-----"Save Values" button-----
        self.saveValues = ttk.Button(self, text="Save Values", 
                                     command=self.save_values)
        self.saveValues.place(x=558,y=130)
    
    #-----"Submit" button function-----     
    def on_submit(self):
        innerList4.append(self.table.get())
        root.destroy()
        
    #-----"Save Values" button function-----           
    def save_values(self):
        saveList4 = []
        saveList4.append(self.table.get())
        with open('save_file4.p', 'wb+') as file2:
            pickle.dump(saveList4, file2)

root = tk.Tk()
Example(root).pack(side="top")
root.geometry('1000x158')
root.mainloop()

#-----Part 5, Second optimization--------------------------------------------
#-----Part 5, Second optimization--------------------------------------------
#-----Part 5, Second optimization--------------------------------------------
inverseNormalReliability = norm.ppf(reliabilityLevel2)

#-----Range for February based on the year----- 
if currentYear2%4==0:
    FebruaryLength2 = range(29)
    daysInFeb2 = 29
    numberOfDays2 = 366
else:
    FebruaryLength2 = range(28)
    daysInFeb2 = 28
    numberOfDays2 = 365

daysInMonths2 = [31, daysInFeb2, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
#-----Monthly line holders, crew scheduled, averges provided, 
#      variances provided, and the difference between monthlyLineHolders 
#      and monthlyCrew-----
monthlyLineHolders2 = [] 
for m in range(12):
       monthlyLineHolders2.append(int(innerList4[m])) 
       

monthlyCrewScheduled2 = [] 
for m in ListAppend1:
       monthlyCrewScheduled2.append(int(innerList4[m])) 


averageMonthlyAbsences2 = []
for m in ListAppend2:
       averageMonthlyAbsences2.append(float(innerList4[m])) 


varOfMonthlyExpectedAbsences2 = []
for m in ListAppend3:
       varOfMonthlyExpectedAbsences2.append(float(innerList4[m])) 

#-----Calculating the standard deviations based on given variances-----    
stdDevMonthlyExpectedAbsences2 = []
for m in Months:
    stdDevOfAbsences = sqrt(varOfMonthlyExpectedAbsences2[m])
    stdDevMonthlyExpectedAbsences2.append(stdDevOfAbsences)

#-----Calculating the expected absences for each month based on the average 
#      absences, std. dev. of absences, and the reliability level-----
expectedMonthlyAbsences2 = []
for m in Months:
    expectedAbsenses = inverseNormalReliability * stdDevMonthlyExpectedAbsences2[m] + averageMonthlyAbsences2[m]
    expectedMonthlyAbsences2.append(expectedAbsenses)

#-----By subtracting crew scheduled from line holders, we're left with a 
#      variable that represents vacation days plus expected absences-----
vacationAllottedPlusExpectedAbsences2 = [(monthlyLineHolders2[m]-monthlyCrewScheduled2[m]) for m in Months]

#-----Calculated monthly upper bound based on subtracting expected absences 
#      subtracted from vacation days plus expected absences-----
monthlyUpperBoundVacationAllotted2 = []
for m in Months:
    vacationAllotted = trunc(vacationAllottedPlusExpectedAbsences2[m] - expectedMonthlyAbsences2[m])
    monthlyUpperBoundVacationAllotted2.append(vacationAllotted)
        
#-----Calculated upper bound for the year-----
annualUpperBoundVacationAllotted2 = quicksum(monthlyUpperBoundVacationAllotted2[m] for m in Months)

n.remove(n.getVars()[0:numberOfDays])
n.update()

#-----Decision variable-----
vacationVariable = []
for m in Months:
    vacationVariable.append(n.addVars(daysInMonths2[m], 
                                      lb = dailyLowerBoundVacationAllotted2, 
                                      ub = dailyUpperBoundVacationAllotted2, 
                                      obj = 1, name = listOfMonths[m] + "2"))
#-----Deleting monthly contraints-----

n.remove(n.getConstrs()[0:39])
    
#-----Implementing monthly contraints-----
for m in Months:
       n.addConstr(vacationVariable[m].sum() <= monthlyUpperBoundVacationAllotted2[m], 
                   name = "SecondMonthlyUpperBoundVacationAllottedFor" + listOfMonths[m])
for m in Months:
       n.addConstr(vacationVariable[m].sum() <= userMonthlyUpperBoundVacationAllotted2, 
                   name = "SecondUserMonthlyUpperBoundVacationAllottedFor" + listOfMonths[m])
for m in Months:
    n.addConstr(vacationVariable[m].sum() >= monthlyLowerBoundVacationAllotted2, 
                name = "SecondMonthlyLowerBoundVacationAllottedFor" + listOfMonths[m])   

#-----Calculating the objective value-----
totalObjectiveValue2 = 0
for m in Months:
    objectiveValue = 0
    objectiveValue = vacationVariable[m].sum()
    totalObjectiveValue2 = totalObjectiveValue2 + objectiveValue

#-----Implementing annual constraints-----
n.addConstr(totalObjectiveValue2 <= annualUpperBoundVacationAllotted2, 
            name = "TotalAnnualUpperBoundVacationAllotted2") 
n.addConstr(totalObjectiveValue2 <= userAnnualUpperBoundVacationAllotted2, 
            name = "UserTotalAnnualUpperBoundVacationAllotted2") 
n.addConstr(totalObjectiveValue2 >= annualLowerBoundVacationAllotted2, 
            name = "TotalAnnualLowerBoundVacationAllotted2")

#-----Objective function-----
for m in Months:
    n.setObjective(totalObjectiveValue2, GRB.MAXIMIZE)
#-----Execute optimization-----
n.update()
n.optimize()

#-----Creating files with the deatils of the formulation and optimization for 
#      further inspection/review-----
n.write('SolutionList2.sol')
n.write("SimpleModel2.lp")
n.write("DetailedModel2.mps")

#-----Initializing lists for extracting the post-optimization decision 
#      variable values-----
decisionVariables2 = []
optimalValues2 = []
janOptimalVs2 = []
febOptimalVs2 = []
marOptimalVs2 = []
aprOptimalVs2 = []
mayOptimalVs2 = []
junOptimalVs2 = []
julOptimalVs2 = []
augOptimalVs2 = []
sepOptimalVs2 = []
octOptimalVs2 = []
novOptimalVs2 = []
decOptimalVs2 = []

#-----Extracting a clean list of the decision variables-----
for l in n.getVars():
    decisionVariables2.append(int(l.x))


if numberOfDays2 == 366:
    for l in range(366):
        if 0<=l<=30:    
            janOptimalVs2.append(decisionVariables2[l])
        elif 31<=l<=59:
            febOptimalVs2.append(decisionVariables2[l])
        elif 60<=l<=90:
            marOptimalVs2.append(decisionVariables2[l])
        elif 91<=l<=120:
            aprOptimalVs2.append(decisionVariables2[l])
        elif 121<=l<=151:
            mayOptimalVs2.append(decisionVariables2[l])
        elif 152<=l<=181:
            junOptimalVs2.append(decisionVariables2[l])
        elif 182<=l<=212:
            julOptimalVs2.append(decisionVariables2[l])
        elif 213<=l<=243:
            augOptimalVs2.append(decisionVariables2[l])
        elif 244<=l<=273:
            sepOptimalVs2.append(decisionVariables2[l])
        elif 274<=l<=304:
            octOptimalVs2.append(decisionVariables2[l])
        elif 305<=l<=334:
            novOptimalVs2.append(decisionVariables2[l])
        else:
            decOptimalVs2.append(decisionVariables2[l])
#-----Making each list 31 values long-----
    febOptimalVs2.insert(29, 0)
    febOptimalVs2.insert(30, 0)
    aprOptimalVs2.insert(30, 0)
    junOptimalVs2.insert(30, 0)
    sepOptimalVs2.insert(30, 0)
    novOptimalVs2.insert(30, 0)
    
elif numberOfDays2 == 365:
    for l in range(365):
        if 0<=l<=30:    
            janOptimalVs2.append(decisionVariables2[l])
        elif 31<=l<=58:
            febOptimalVs2.append(decisionVariables2[l])
        elif 59<=l<=89:
            marOptimalVs2.append(decisionVariables2[l])
        elif 90<=l<=119:
            aprOptimalVs2.append(decisionVariables2[l])
        elif 120<=l<=150:
            mayOptimalVs2.append(decisionVariables2[l])
        elif 151<=l<=180:
            junOptimalVs2.append(decisionVariables2[l])
        elif 181<=l<=211:
            julOptimalVs2.append(decisionVariables2[l])
        elif 212<=l<=242:
            augOptimalVs2.append(decisionVariables2[l])
        elif 243<=l<=272:
            sepOptimalVs2.append(decisionVariables2[l])
        elif 273<=l<=303:
            octOptimalVs2.append(decisionVariables2[l])
        elif 304<=l<=333:
            novOptimalVs2.append(decisionVariables2[l])
        else:
            decOptimalVs2.append(decisionVariables2[l])

    febOptimalVs2.insert(28, 0)
    febOptimalVs2.insert(29, 0)
    febOptimalVs2.insert(30, 0)
    aprOptimalVs2.insert(30, 0)
    junOptimalVs2.insert(30, 0)
    sepOptimalVs2.insert(30, 0)
    novOptimalVs2.insert(30, 0) 

#-----List of lists containing the decision variables sperated by month-----
optimalValues2 = [janOptimalVs2, febOptimalVs2, marOptimalVs2, aprOptimalVs2, 
                 mayOptimalVs2, junOptimalVs2, julOptimalVs2, augOptimalVs2, 
                 sepOptimalVs2, octOptimalVs2, novOptimalVs2, decOptimalVs2]

#-----Initialization for totaling the decision variables for each month-----
janTotal2 = 0
febTotal2 = 0
marTotal2 = 0
aprTotal2 = 0
mayTotal2 = 0
junTotal2 = 0
julTotal2 = 0
augTotal2 = 0
sepTotal2 = 0
octTotal2 = 0
novTotal2 = 0
decTotal2 = 0

#-----Totaling the decision variables for each month-----
for m in Months:
    for l in range(31):
        if m == 0:
            janTotal2 += janOptimalVs2[l]
        elif m == 1:
            febTotal2 += febOptimalVs2[l]
        elif m == 2:
            marTotal2 += marOptimalVs2[l]
        elif m == 3:
            aprTotal2 += aprOptimalVs2[l]
        elif m == 4:
            mayTotal2 += mayOptimalVs2[l]
        elif m == 5:
            junTotal2 += junOptimalVs2[l]
        elif m == 6:
            julTotal2 += julOptimalVs2[l]
        elif m == 7:
            augTotal2 += augOptimalVs2[l]
        elif m == 8:
            sepTotal2 += sepOptimalVs2[l]
        elif m == 9:
            octTotal2 += octOptimalVs2[l]
        elif m == 10:
            novTotal2 += novOptimalVs2[l]
        else:
            decTotal2 += decOptimalVs2[l]
            
#-----List of monthly totals-----
optimalValuesMonths2 = [janTotal2, febTotal2, marTotal2, aprTotal2, mayTotal2, 
                       junTotal2, julTotal2, augTotal2, sepTotal2, octTotal2, 
                       novTotal2, decTotal2]

tempTotal2 = 0
for m in Months:
    tempTotal2 += optimalValuesMonths2[m]
    
#-----Scatterplot-----
newDevAndVacation = []

for m in Months:
    newDevAndVacation.append(vacationAllottedPlusExpectedAbsences2[m]-averageMonthlyAbsences2[m])
    
scatterPlotValues2 = []
    
for l in range(25):
    tempTotalList = []
    for m in Months:
        tempCalculation = newDevAndVacation[m] - stdDevMonthlyExpectedAbsences2[m]*standInverseNorm[l]
        tempTotalList.append(tempCalculation)
        if tempTotalList[m] > userMonthlyUpperBoundVacationAllotted2:
            tempTotalList[m] = userMonthlyUpperBoundVacationAllotted2
        else:
            pass
        if tempTotalList[m] < monthlyLowerBoundVacationAllotted2:
            tempTotalList[m] = monthlyLowerBoundVacationAllotted2
        else:
            pass
        if tempTotalList[m] > dailyUpperBoundVacationAllotted2*daysInMonths2[m]:
            tempTotalList[m] = dailyUpperBoundVacationAllotted2*daysInMonths2[m]
        else:
           pass
        if tempTotalList[m] < dailyLowerBoundVacationAllotted2*daysInMonths2[m]:
          tempTotalList[m] = dailyLowerBoundVacationAllotted2*daysInMonths2[m]
        else:
           pass
        if len(tempTotalList) == 12:
            tempCalculation = sum(tempTotalList)
            scatterPlotValues2.append(trunc(tempCalculation))
        else:
            pass
    if scatterPlotValues2[l] > userAnnualUpperBoundVacationAllotted2:
        scatterPlotValues2[l] = userAnnualUpperBoundVacationAllotted2
    else:
        pass
    if scatterPlotValues2[l] < annualLowerBoundVacationAllotted2:  
           scatterPlotValues2[l] = annualLowerBoundVacationAllotted2
    else:
        pass    
    
#-----Part 6, Second Menu----------------------------------------------------
#-----Part 6, Second Menu----------------------------------------------------
#-----Part 6, Second Menu----------------------------------------------------
#-----Second Menu-----
class SaberApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        root.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand='true')
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        root.wm_title(self, "Reliability Data Driven Vacation Allocation Optimizer")
        #-----Icon-----
        root.iconbitmap(self, "OSabreIcon.ico")
        
        self.frames = {}

        for F in (StartPage, Histogram, Scatterplot):

            frame = F(container, self)
                
            self.frames[F] = frame
                
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Menu")
        label.pack(side = 'top', pady=10, padx=10)
        
        self.HistButton = ttk.Button(self, text='Comparison\n     Chart', command=lambda: controller.show_frame(Histogram))
        self.HistButton.pack(side='top', pady=10)
        
        self.ScatterButton = ttk.Button(self, text='Scatter Plot', command=lambda: controller.show_frame(Scatterplot))
        self.ScatterButton.pack(side='top')
        
        self.ScatterButton = ttk.Button(self, text='Write Results', command=self.Writefile)
        self.ScatterButton.pack(side='top', pady=10)
        
        self.ExitButton = ttk.Button(self, text='Exit Program', command=self.Exit)
        self.ExitButton.pack(side='top')
        
    def Writefile(self):
        with open('Optimization Results.txt', 'w') as file5:
            file5.write("Results of the initial optimization.\n\nThe total number of vacation days for the year is ")
            file5.write(str(tempTotal))
            file5.write(" days.\n\n")
            for m in Months:
                file5.write("The optimal number of vacation days for ")
                file5.write(listOfMonths[m])
                file5.write(" is ")
                file5.write(str(optimalValuesMonths[m]))
                file5.write(" days.\n")
            file5.write("\n\n")
            file5.write("Results of the secondary optimization.\n\nThe total number of vacation days for the year is ")
            file5.write(str(tempTotal2))
            file5.write(" days.\n\n")
            for m in Months:
                file5.write("The optimal number of vacation days for ")
                file5.write(listOfMonths[m])
                file5.write(" is ")
                file5.write(str(optimalValuesMonths2[m]))
                file5.write(" days.\n")
            file5.write("\n\n")
            file5.write("Analysis\n\n")
            if tempTotal - tempTotal2 == 0:
                file5.write("The optimal number of vacation days did not change.\n")
            elif tempTotal - tempTotal2 > 0:
                file5.write("The optimal number of vacation days decreased by ")
                file5.write(str(abs(tempTotal2 - tempTotal)))
                file5.write(" days.\n")
            else:
                file5.write("The optimal number of vacation days increased by ")
                file5.write(str(abs(tempTotal - tempTotal2)))
                file5.write(" days.\n")
            file5.write("\n")
            for m in Months:
                if optimalValuesMonths[m] - optimalValuesMonths2[m] == 0:
                    pass
                elif optimalValuesMonths[m] - optimalValuesMonths2[m] > 0:
                    file5.write("The optimal number of vacation days for ")
                    file5.write(listOfMonths[m])
                    file5.write(" decreased by ")
                    file5.write(str(abs(optimalValuesMonths[m] - optimalValuesMonths2[m])))
                    file5.write(" days.\n")
                else:
                    file5.write("The optimal number of vacation days for ")
                    file5.write(listOfMonths[m])
                    file5.write(" increased by ")
                    file5.write(str(abs(optimalValuesMonths[m] - optimalValuesMonths2[m])))
                    file5.write(" days.\n")
                    
            if tempTotal == userAnnualUpperBoundVacationAllotted:
                file5.write("\n\nThe optimal number of vacation days for the first optimization is equal to the annual upper bound that you entered.")
                file5.write("\nThis is because the true optimal value is greater than or equal to your upper bound.")
            else:
                pass
            if tempTotal == annualLowerBoundVacationAllotted:
                file5.write("\n\nThe optimal number of vacation days for the first optimization is equal to the annual lower bound that you entered.")
                file5.write("\nThis is because the true optimal value is less than or equal to your lower bound.")
            else:
                pass
            if tempTotal2 == userAnnualUpperBoundVacationAllotted2:
                file5.write("\n\nThe optimal number of vacation days for the second optimization is equal to the second annual upper bound that you entered.")
                file5.write("\nThis is because the true optimal value is greater than or equal to your upper bound.")
            else:
                pass
            if tempTotal2 == annualLowerBoundVacationAllotted2:
                file5.write("\n\nThe optimal number of vacation days for the second optimization is equal to the second annual lower bound that you entered.")
                file5.write("\nThis is because the true optimal value is less than or equal to your lower bound.")
            else:
                pass
            
            if currentYear == currentYear2:
                pass
            elif currentYear > currentYear2:
                file5.write("\n\nThe year was decreased by ")
                file5.write(currentYear - currentYear2)
                if currentYear - currentYear2 == 1:
                    file5.write(" year.")
                elif currentYear - currentYear2 == -1:
                    file5.write(" year.")
                else:
                    file5.write(" years.")
            else:
                file5.write("\n\nThe year was increased by ")
                file5.write(str(abs(currentYear - currentYear2)))
                if currentYear - currentYear2 == 1:
                    file5.write(" year.")
                elif currentYear - currentYear2 == -1:
                    file5.write(" year.")
                else:
                    file5.write(" years.")
                
            if reliabilityLevel == reliabilityLevel2:
                pass
            elif reliabilityLevel > reliabilityLevel2:
                file5.write("\n\nThe reliability level was decreased by ")
                file5.write(str(abs(round(reliabilityLevel - reliabilityLevel2, 3))))
                file5.write(".")
            else:
                file5.write("\n\nThe reliability level was increased by ")
                file5.write(str(abs(round(reliabilityLevel - reliabilityLevel2, 3))))
                file5.write(".")
                
            if dailyUpperBoundVacationAllotted == dailyUpperBoundVacationAllotted2:
                pass
            elif dailyUpperBoundVacationAllotted > dailyUpperBoundVacationAllotted2:
                file5.write("\n\nThe daily upper bound was decreased by ")
                file5.write(dailyUpperBoundVacationAllotted - dailyUpperBoundVacationAllotted2)
                if dailyUpperBoundVacationAllotted - dailyUpperBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif dailyUpperBoundVacationAllotted - dailyUpperBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
            else:
                file5.write("\n\nThe daily upper bound was increased by ")
                file5.write(str(abs(dailyUpperBoundVacationAllotted - dailyUpperBoundVacationAllotted2)))
                if dailyUpperBoundVacationAllotted - dailyUpperBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif dailyUpperBoundVacationAllotted - dailyUpperBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
                
            if dailyLowerBoundVacationAllotted == dailyLowerBoundVacationAllotted2:
                pass
            elif dailyLowerBoundVacationAllotted > dailyLowerBoundVacationAllotted2:
                file5.write("\n\nThe daily lower bound was decreased by ")
                file5.write(str(dailyLowerBoundVacationAllotted - dailyLowerBoundVacationAllotted2))
                if dailyLowerBoundVacationAllotted - dailyLowerBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif dailyLowerBoundVacationAllotted - dailyLowerBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
            else:
                file5.write("\n\nThe daily lower bound was increased by ")
                file5.write(str(abs(dailyLowerBoundVacationAllotted - dailyLowerBoundVacationAllotted2)))
                if dailyLowerBoundVacationAllotted - dailyLowerBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif dailyLowerBoundVacationAllotted - dailyLowerBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
            
            if userMonthlyUpperBoundVacationAllotted == userMonthlyUpperBoundVacationAllotted2:
                pass
            elif userMonthlyUpperBoundVacationAllotted > userMonthlyUpperBoundVacationAllotted2:
                file5.write("\n\nThe monthly upper bound was decreased by ")
                file5.write(str(userMonthlyUpperBoundVacationAllotted - userMonthlyUpperBoundVacationAllotted2))
                if userMonthlyUpperBoundVacationAllotted - userMonthlyUpperBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif userMonthlyUpperBoundVacationAllotted - userMonthlyUpperBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
            else:
                file5.write("\n\nThe monthly upper bound was increased by ")
                file5.write(str(abs(userMonthlyUpperBoundVacationAllotted - userMonthlyUpperBoundVacationAllotted2)))
                if userMonthlyUpperBoundVacationAllotted - userMonthlyUpperBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif userMonthlyUpperBoundVacationAllotted - userMonthlyUpperBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
            
            if monthlyLowerBoundVacationAllotted == monthlyLowerBoundVacationAllotted2:
                pass
            elif monthlyLowerBoundVacationAllotted > monthlyLowerBoundVacationAllotted2:
                file5.write("\n\nThe monthly lower bound was decreased by ")
                file5.write(str(monthlyLowerBoundVacationAllotted - monthlyLowerBoundVacationAllotted2))
                if monthlyLowerBoundVacationAllotted - monthlyLowerBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif monthlyLowerBoundVacationAllotted - monthlyLowerBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
            else:
                file5.write("\n\nThe monthly lower bound was increased by ")
                file5.write(str(abs(monthlyLowerBoundVacationAllotted - monthlyLowerBoundVacationAllotted2)))
                if monthlyLowerBoundVacationAllotted - monthlyLowerBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif monthlyLowerBoundVacationAllotted - monthlyLowerBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
            
            if userAnnualUpperBoundVacationAllotted == userAnnualUpperBoundVacationAllotted2:
                pass
            elif userAnnualUpperBoundVacationAllotted > userAnnualUpperBoundVacationAllotted2:
                file5.write("\n\nThe annual upper bound was decreased by ")
                file5.write(str(userAnnualUpperBoundVacationAllotted - userAnnualUpperBoundVacationAllotted2))
                if userAnnualUpperBoundVacationAllotted - userAnnualUpperBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif userAnnualUpperBoundVacationAllotted - userAnnualUpperBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
            else:
                file5.write("\n\nThe annual upper bound was increased by ")
                file5.write(str(abs(userAnnualUpperBoundVacationAllotted - userAnnualUpperBoundVacationAllotted2)))
                if userAnnualUpperBoundVacationAllotted - userAnnualUpperBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif userAnnualUpperBoundVacationAllotted - userAnnualUpperBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
                
            if annualLowerBoundVacationAllotted == annualLowerBoundVacationAllotted2:
                pass
            elif annualLowerBoundVacationAllotted > annualLowerBoundVacationAllotted2:
                file5.write("\n\nThe annual lower bound was decreased by ")
                file5.write(str(annualLowerBoundVacationAllotted - annualLowerBoundVacationAllotted2))
                if annualLowerBoundVacationAllotted - annualLowerBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif annualLowerBoundVacationAllotted - annualLowerBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
            else:
                file5.write("\n\nThe annual lower bound was increased by ")
                file5.write(str(abs(annualLowerBoundVacationAllotted - annualLowerBoundVacationAllotted2)))
                if annualLowerBoundVacationAllotted - annualLowerBoundVacationAllotted2 == 1:
                    file5.write(" vacation day.")
                elif annualLowerBoundVacationAllotted - annualLowerBoundVacationAllotted2 == -1:
                    file5.write(" vacation day.")
                else:
                    file5.write(" vacation days.")
            
                
    def Exit(self):
        os._exit(1)
    
class Histogram(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Comparison Chart")
        label.pack(side = 'top', pady=10, padx=10)
        
        self.MenuButton = ttk.Button(self, text='Menu', command=lambda: controller.show_frame(StartPage))
        self.MenuButton.pack(side='top')
        
        f = Figure(figsize = (8,5), dpi = 100)
        a = f.add_subplot(111)
        
        xList = [1,3,5,7,9,11,13,15,17,19,21,23]
        yList = []
        for m in Months:
            yList.append(int(optimalValuesMonths[m]))
        a.clear()
        
        xList2 = [2,4,6,8,10,12,14,16,18,20,22,24]
        yList2 = []
        for m in Months:
            yList2.append(int(optimalValuesMonths2[m]))
        a.clear()
        a.bar(xList, yList, label = "Optimization One", color = 'r')
        a.bar(xList2, yList2, label = "Secondary Optimization", color = 'c')
        
        a.legend(bbox_to_anchor=(0, 1.08, 1, .102), loc=3,
                 ncol=2, borderaxespad=0)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        a.set_title("Vacation Days per Month")
        a.set_xlabel("Month")
        a.set_ylabel("Vacation Days")
    
class Scatterplot(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Scatter Plot")
        label.pack(side = 'top', pady=10, padx=10)
        
        self.MenuButton = ttk.Button(self, text='Menu', command=lambda: controller.show_frame(StartPage))
        self.MenuButton.pack(side='top')
        
        f = Figure(figsize = (8,5), dpi = 100)
        a = f.add_subplot(111)
        
        a.clear()
        a.scatter(standRelyLevels, scatterPlotValues, color = 'r', label = "Initial Optimization")
        a.scatter(standRelyLevels, scatterPlotValues2, color = 'c', label = "Secondary Optimization")
        
        a.legend(bbox_to_anchor=(0, 1.08, 1, .102), loc=3,
                 ncol=2, borderaxespad=0)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        a.set_title("Annual Vacation Days vs. Reliability Level")
        a.set_xlabel("Reliability Level")
        a.set_ylabel("Annual Vacation Days")         
    
root = tk.Tk
App = SaberApp()
App.mainloop()
  
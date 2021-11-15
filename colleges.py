"""
Benjamin Chen
Colleges Class
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
def displayResult(fct):
    def getResult(*args, **kwargs):
        """
        decorator function
        input: 2 integers: max and min of the function return
        return: function that is passed into decorator function
        Prints out the max and the min passed into the function in console.
        """
        result,result2 = fct(*args, **kwargs)
        print("The Max and Min is: %i and %i"%(result, result2))
        return result,result2
    return getResult
class colleges:
    def __init__(self): #part a of colleges.py
        """
        constructor for colleges object
        input: none
        constructs a college object by opening and reading 3 csv files and saves the data into data structures
        """
        with open("colleges.csv") as f:
            reader = csv.reader(f)
            self.colleges = []
            for row in reader:
                self.colleges.append(row) #adds rows from colleges.csv into self.colleges (list)
        with open("scores.csv") as f:
            reader = csv.reader(f)
            aList = []
            for row in reader:
                aList.append(row)
            self.arr = np.array(aList).astype(np.int) #creates a 2d array from aList (which is a list of lists)
        with open("header.csv") as f:
            reader = csv.reader(f)
            self.header = list(reader)

    def requirements(self):
        """
        gets mean and std of the ACT scores, Total Annual Cost, and SAT scores
        input:none
        return: none
        uses numpy methods to get mean and std of each data field and saves it into college object
        """
        actScores = self.arr[:,10] #10 is column with ACT Lower field
        tmp = np.where(actScores== -1) #gets array of indices where the -1s are

        """
        can do dataValid = data[data > 0]
        """
        newScores = np.delete(actScores, tmp) #deletes all the -1s in the array
        self.actScoresMean = round(np.mean(newScores))
        self.actScoresSTD = round(np.std(newScores))
        
        totalAnnualCost = self.arr[:,5]#5 is column with Total Annual Cost
        self.totalAnnualCostMean = round(np.mean(totalAnnualCost))
        self.totalAnnualCostSTD = round(np.std(totalAnnualCost))

        satScores = self.arr[:,8]
        tmp = np.where(satScores == -1) #same as actScores
        newScores = np.delete(satScores, tmp)
        self.satScoresMean = round(np.mean(newScores))
        self.satScoresSTD = round(np.std(newScores))
    
    def getACTMean(self):
        return self.actScoresMean

    def getACTSTD(self):
        return self.actScoresSTD

    def getAnnualCostMean(self):
        return self.totalAnnualCostMean

    def getAnnualCostSTD(self):
        return self.totalAnnualCostSTD

    def getSATMean(self):
        return self.satScoresMean

    def getSATSTD(self):
        return self.satScoresSTD

    def getHeader(self):
        return self.header

    @displayResult
    def annualCostDistribution(self):
        """
        plots the annual cost of each college
        input: none
        output: max and min of the annualcost of the colleges
        """
        annualCost = self.arr[:,5]
        tmp = np.where(annualCost== -1) #gets array of indices where the -1s are
        newCost = np.delete(annualCost, tmp) #deletes all the -1s in the array
        binList = [0,10000,20000,30000,40000,50000,60000,70000,80000]
        plt.hist(newCost, bins = binList)
        plt.title("Distribution of Schools based on Annual Cost")
        plt.ylabel("Number of Schools")
        plt.xlabel("Annual Cost")
        #plt.show()
        return np.max(annualCost),np.min(annualCost)
    
    @displayResult
    def againstStudentRanking(self, x):
        """
        plots desired field against student ranking
        input: number representing the data field desired by user
        output: max and min of the data field desired by user
        """
        data = self.arr[:, x]
        tmp = np.where(data== -1) #gets array of indices where the -1s are
        newData = np.delete(data, tmp) #deletes all the -1s in the array
        plt.title(self.header[0][x] +" vs School Ranking")
        plt.ylabel(self.header[0][x])
        plt.xlabel("School Ranking")
        plt.plot(np.arange(0,newData.size), newData)
        #plt.show()
        return np.max(newData),np.min(newData)
    
    @displayResult
    def topAlumniSalaries(self, num):
        """
        creates a bar graph of num colleges with greatest alumni salaries
        input: a number indication how many colleges to include in bar graph
        output: max and min of the alumni salaries
        """
        counter = 0
        listOfNames = []
        array = np.flip(np.flip(np.sort(self.arr[:, 6]))[:num])
        """
        just sorted the data
        i = np.argsort(data)
        colleges = self.colleges[:1][i][-1:]
        """
        for x in array:
            for y in self.arr[:,6]:
                if x == y and not self.colleges[counter][1] in listOfNames and not len(listOfNames) == num:
                    listOfNames.append(self.colleges[counter][1])
                counter += 1
            counter = 0
        plt.bar(listOfNames, array, align = "center")
        plt.xlabel("Name of School")
        plt.ylabel("Alumni Salary")
        plt.title("Top %i Alumni Salary" %(num))
        plt.ylim(100000,170000)
        plt.xticks(np.arange(0,num),listOfNames, rotation = "vertical")
        plt.tight_layout()
        #plt.show()
        return np.max(array), np.min(array)

#c = colleges()
#c.requirements()
#c.annualCostDistribution()
#c.againstStudentRanking(10)
#c.topAlumniSalaries(15)
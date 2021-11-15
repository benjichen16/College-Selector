"""
Benjamin Chen
GUI Classes
"""
import sys
from colleges import colleges
import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter.messagebox as tkmb

TOPNUM = 15

class DisplayWin(tk.Toplevel):
    def __init__(self,master):
        """
        constructor method for top level window
        input: a master window
        output: none
        creates a window that displays radiobuttons a number of buttons that lets the user decide what graph they want to look at
        """
        super().__init__()

        self.c = colleges()
        self.controlVar = tk.IntVar(master) #user input 
        counter = 0
        alist = self.c.getHeader()[0] #c.getHeader() returns a list of list
        for x in alist:
            tk.Radiobutton(self, text = str(x), variable = self.controlVar, value = counter).grid(column = 0, sticky = 'w')
            counter +=1
        
        self.controlVar.set(0)
        tk.Button(self, text = "Ok", command = self.destroy).grid()
        
        self.focus_set()
        self.grab_set()
        self.transient()

        self.protocol('WM_DELETE_WINDOW', self.close_app)

    def getNum(self):
        return self.controlVar.get() #returns int
    def close_app(self):
        self.controlVar.set(-1)#sets the controlVar to -1 so there will be no graph that displays
        self.destroy()

class PlotWin(tk.Toplevel):
    def __init__(self, master):
        """
        constructor method for plot window
        input: a master window
        output: none
        takes the matplotlib methods and draws it on a window using canvas widget
        """
        super().__init__()
        fig = plt.figure(figsize = (7,7)) #plt is set up before construction
        canvas = FigureCanvasTkAgg(fig, master = self)
        canvas.get_tk_widget().grid()
        canvas.draw()

class MainWin(tk.Tk):
    def __init__(self):
        """
        constructor method for main win
        input: none
        output: none
        creates a college object and a gui window with three buttons. the buttons, when clicked, will display a plot with the desired fields
        """
        super().__init__()
        try:
            self.c = colleges()
            self.c.requirements()
        except FileNotFoundError:
            tkmb.showerror("Error:", sys.exc_info()[0], parent = self) #creates error message box if there is a file not found error
            self.quit() #exits main loop after error message box
        frame1 = tk.Frame(self)
        self.title("Top Colleges")
        tk.Label(frame1, text = "College Lookup", fg = "blue").grid(row = 0)
        frame1.grid(row = 0)
        frame2 = tk.Frame(self)
        frame3 = tk.Frame(self)
        frame4 = tk.Frame(self)
        tk.Button(frame2, text = "By Cost", command = self.byCost).grid(row = 1, column = 0)
        tk.Button(frame3, text = "By Data", command = self.byData).grid(row = 1, column = 2 )
        tk.Button(frame4, text = "By Salary", command = lambda: self.bySalary(TOPNUM)).grid(row = 1, column = 3 )
        frame2.grid(row = 1, sticky = 'w', padx = "40")
        frame3.grid(row = 1)
        frame4.grid(row = 1, sticky = 'e', padx = "40")
        tk.Label(self, text= "Mean Total Annual Cost: %i, standard deviation: %i"%(self.c.getAnnualCostMean(), self.c.getAnnualCostSTD())).grid(row = 2, sticky = 'w')
        tk.Label(self, text= "Mean SAT Lower: %i, standard deviation: %i"%(self.c.getSATMean(), self.c.getSATSTD())).grid(row = 3, sticky = 'w')
        tk.Label(self, text= "Mean ACT Lower: %i, standard deviation: %i"%(self.c.getACTMean(), self.c.getACTSTD())).grid(row = 4, sticky = 'w')
        self.protocol('WM_DELETE_WINDOW', self.close_app)
    
    def byCost(self):
        top = PlotWin(self)
        self.c.annualCostDistribution()
        self.wait_window(top)

    def byData(self):
        top = DisplayWin(self)
        self.wait_window(top)
        if(top.getNum() == -1):
            pass
        else:
            win = PlotWin(self)
            self.c.againstStudentRanking(top.getNum())
            self.wait_window(win)

    def bySalary(self, num):
        top = PlotWin(self)
        self.c.topAlumniSalaries(num)
        self.wait_window(top)

    def close_app(self):
        if tkmb.askokcancel("Close", "Are you sure?"): #makes sure user wants to quit before exiting mainloop
            self.destroy()
            self.quit()
app = MainWin()
app.mainloop()

"""
1. Is there a trend for student count vs college ranking?
No, there is no disernable trend between student count and college ranking.
2. Is there a trend for cost vs college ranking?
There is a slight trend with the higher ranking colleges being a but more expensive than the lower ranking colleges but the difference is not that big.
3. Is there a trend for alumni salary vs. college ranking?
Yes, there is a clear trend with colleges with higher ranking and their alumnis earning more.
4. Is there a trend for acceptance rate vs college ranking?
Yes, colleges with higher ranking have lower acceptance rates than colleges with lower ranking.
5. Is there a trend for test scores vs college ranking?
Yes, colleges with higher ranking have higher test scores and colleges with lower ranking have lower test scores.
"""
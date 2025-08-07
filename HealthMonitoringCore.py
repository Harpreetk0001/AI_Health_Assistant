import json
import numpy as np
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

VitalsMatrix = ([],[],[],[],[],[])

TimeStamps = []

class HealthGraph:
    def __init__(self, title="Health Analytics", x_label="Days", y_label="Vitals"):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.fig, self.ax = plt.subplots()

    def add_line(self, x_data, y_data, label=None, color=None, linestyle='-'):
        self.ax.plot(x_data, y_data, label=label, color=color, linestyle=linestyle)

    def show(self, legend=True, grid=True):
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        if legend:
            self.ax.legend()
        if grid:
            self.ax.grid(True)
        plt.show()

    def showVitals():
        graph = HealthGraph(title="Health Analytics", x_label="Days", y_label="Vitals")

        graph.add_line(TimeStamps, VitalsMatrix[0], label="Hydration (ml)", color="blue")
        graph.add_line(TimeStamps, VitalsMatrix[1], label="Sleep (hrs)", color="red")
        graph.add_line(TimeStamps, VitalsMatrix[2], label="Heartbeat (bpm)", color="green")
        graph.add_line(TimeStamps, VitalsMatrix[3], label="Systolic BP (mmHg)", color="orange")
        graph.add_line(TimeStamps, VitalsMatrix[4], label="Diastolic BP (mmHg)", color="brown")
        graph.add_line(TimeStamps, VitalsMatrix[5], label="Steps", color="purple", linestyle='--')
        
        graph.show()
        

class Vitals:
    def __init__(self, hydration, sleep, hb, bp_systolic, bp_diastolic, steps, timestamp = None):
        self.hydration = hydration
        self.sleep = sleep
        self.hb = hb
        self.bp_systolic = bp_systolic
        self.bp_diastolic = bp_diastolic
        self.steps = steps
        
        self.timestamp = timestamp or datetime.now()

        TimeStamps.append(self.timestamp)

        VitalsMatrix[0].append(self.hydration)

        VitalsMatrix[1].append(self.sleep)

        VitalsMatrix[2].append(self.hb)

        VitalsMatrix[3].append(self.bp_systolic)
        VitalsMatrix[4].append(self.bp_diastolic)
        self.bp_systolic = bp_systolic
        self.bp_diastolic = bp_diastolic
        bp_value = f"{bp_systolic}/{bp_diastolic}"

        VitalsMatrix[5].append(self.steps)

        

    #health monitoring grab historical vital signs from JSON DB#
    #grab vitals over certain period of time and store in numpy array
    def getHistory():
        #get data records

        #record time stamps
        
        
        pass

    ##NICE TO HAVE - FOR FUTURE DEV##
    #health monitoring AI integration#
    #use AI data analysis to generate alerts
    def healthDataAnalysis():
        pass

    def displayHealthWarning(self, vital_type):
        warning = "Your " + vital_type + " is not healthy, please seek medical advice/care"
        print(warning)

    #custom function and set boundary for alerts
    def alert_boundary(self):
        if self.hydration not in range(2100, 2600):
            #produce alert
            self.displayHealthWarning("Hydration")

        if self.sleep not in range(7, 10):
            #produce alert
            self.displayHealthWarning("Sleep")

        if self.hb not in range(60, 100):
            #produce alert
            self.displayHealthWarning("Heartbreat")

        if (self.bp_systolic > 120) and (self.bp_diastolic > 80):
            #produce alert
            self.displayHealthWarning("Blood pressure")

        if self.steps not in range(6000, 8000):
            #produce alert
            self.displayHealthWarning("Steps")

##TESTING##

#data record 1#
dayBefore = (datetime.now()) - timedelta(days=2)
Vitals1 = Vitals(2150, 8, 75, 110, 75, 7500, dayBefore)

#data record 2#
yesterday = (datetime.now()) - timedelta(days=1)
Vitals2 = Vitals(2000, 9, 80, 120, 80, 8000)

#data record 3#
Vitals3 = Vitals(2150, 6, 75, 110, 75, 5000)

#check for alert boundaries
Vitals.alert_boundary(Vitals1)
Vitals.alert_boundary(Vitals2)
Vitals.alert_boundary(Vitals3)

#display graph
HealthGraph.showVitals()





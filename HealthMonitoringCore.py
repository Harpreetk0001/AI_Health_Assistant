import json
import numpy as np
import time
import matplotlib.pyplot as plt

VitalsMatrix = np.array([],
                        [],
                        [],
                        [],
                        [],
                        [])

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

    def showVitals(VitalsMatrix, TimeStamps):
        graph = HealthGraph(title="Health Analytics", x_label="Days", y_label="Vitals")

        graph.add_line(TimeStamps, VitalsMatrix[0], label="Hydration (ml)", color="blue")
        graph.add_line(TimeStamps, VitalsMatrix[1], label="Sleep (hrs)", color="red")
        graph.add_line(TimeStamps, VitalsMatrix[2], label="Heartbeat (bpm)", color="green")
        graph.add_line(TimeStamps, VitalsMatrix[3], label="Systolic BP (mmHg)", color="orange")
        graph.add_line(TimeStamps, VitalsMatrix[4], label="Diastolic BP (mmHg)", color="brown")
        graph.add_line(TimeStamps, VitalsMatrix[5], label="Steps", color="purple", linestyle='--')
        
        graph.show()
        

class Vitals:
    def __init__(self, vital_type, measure, timestamp = None):
        self.vital_type = vital_type
        self.measure = measure
        self.timestamp = timestamp or datetime.now()

        TimeStamps.append(self.timestamp)

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

    def displayHealthWarning():
        warning = "Your", vital_type, "is not healthy, please seek medical advice/care"
        print(warning)
    

class Hydration(Vitals):
    def __init__(self, value_ml):
        VitalsMatrixself[0].append(value_ml)
        super().__init__("Hydration", value_ml)
        

    #custom function and set boundary for alerts
    def alert_boundary(self):
        if self.value_ml not in range(2100, 2600):
            #produce alert
            self.displayHealthWarning()

class Sleep(Vitals):
    def __init__(self, hours):
        VitalsMatrixself[1].append(hours)
        super().__init__("Sleep", hours)

    #custom function and set boundary for alerts
    def alert_boundary(self):
        if self.hours not in range(7, 10):
            #produce alert
            self.displayHealthWarning()

class HeartRate(Vitals):
    def __init__(self, bpm):
        VitalsMatrixself[2].append(bpm)
        super().__init__("Heart Rate", bpm)

    #custom function and set boundary for alerts
    def alert_boundary(self):
        if self.bpm not in range(60, 100):
            #produce alert
            self.displayHealthWarning()

class BloodPressure(Vitlas):
    def __init__(self, systolic, diastolic):
        VitalsMatrixself[3].append(systolic)
        VitalsMatrixself[4].append(diastolic)
        self.systolic = systolic
        self.diastolic = diastolic
        value = f"{systolic}/{diastolic}"
        super().__init__("Blood Pressure", value)

    #custom function and set boundary for alerts
    def alert_boundary(self):
        if (self.systolic > 120) and (self.diastolic > 80):
            #produce alert
            self.displayHealthWarning()

class Steps(HealthVital):
    def __init__(self, count):
        VitalsMatrixself[5].append(count)
        super().__init__("Steps", count)
        

    #custom function and set boundary for alerts
    def alert_boundary(self):
        if self.count not in range(6000, 8000):
            #produce alert
            self.displayHealthWarning()

##TESTING##

Steps()




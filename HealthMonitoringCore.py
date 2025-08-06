import json
import numpy as np
import time
import matplotlib.pyplot as plt

class Vitals:
    def __init__(self, vital_type, measure, timestamp = None):
        self.vital_type = vital_type
        self.measure = measure
        self.timestamp = timestamp or datetime.now()

    #health monitoring grab historical vital signs from JSON DB#
    #grab vitals over certain period of time and store in numpy array
    def getHistory():

    #health monitoring AI integration#
    #use AI data analysis to generate alerts

    def displayHealthWarning():
        warning = "Your", vital_type, "is not healthy, please seek medical advice/care"
    

class Hydration(Vitals):
    def __init__(self, value_ml):
            super().__init__("Hydration", value_ml)

    #custom function and set boundary for alerts
    def alert_boundary(self):
        if self.value_ml not in range(2100, 2600):
            #produce alert
            self.displayHealthWarning()

class Sleep(Vitals):
    def __init__(self, hours):
        super().__init__("Sleep", hours)

    #custom function and set boundary for alerts
    def alert_boundary(self):
        if self.hours not in range(7, 10):
            #produce alert
            self.displayHealthWarning()

class HeartRate(Vitals):
    def __init__(self, bpm):
        super().__init__("Heart Rate", bpm)

    #custom function and set boundary for alerts
    def alert_boundary(self):
        if self.bpm not in range(60, 100):
            #produce alert
            self.displayHealthWarning()

class BloodPressure(Vitlas):
    def __init__(self, systolic, diastolic):
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
        super().__init__("Steps", count)

    #custom function and set boundary for alerts
    def alert_boundary(self):
        if self.count not in range(6000, 8000):
            #produce alert
            self.displayHealthWarning()


#health monitoring graph visualisation#

#health monitoring alerts#



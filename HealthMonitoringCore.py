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
    #grab vitals vitals every day  into a numpy array
    def getHistory():

    #health monitoring AI integration#
    #use AI data analysis to generate alerts
    

class Hydration(Vitals):
    def __init__(self, value_ml):
            super().__init__("Hydration", value_ml)

    #custom function and set boundary for alerts

class Sleep(Vitals):
    def __init__(self, hours):
        super().__init__("Sleep", hours)

    #custom function and set boundary for alerts

class HeartRate(Vitals):
    def __init__(self, bpm):
        super().__init__("Heart Rate", bpm)

    #custom function and set boundary for alerts

class BloodPressure(Vitlas):
    def __init__(self, systolic, diastolic):
        self.systolic = systolic
        self.diastolic = diastolic
        value = f"{systolic}/{diastolic}"
        super().__init__("Blood Pressure", value)

    #custom function and set boundary for alerts

class Steps(HealthVital):
    def __init__(self, count):
        super().__init__("Steps", count)

    #custom function and set boundary for alerts


#health monitoring graph visualisation#

#health monitoring alerts#


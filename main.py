##MAIN##

#import files for front-end
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.metrics import dp
from kivy.core.window import Window
import os, sys
import Front-End.py

#import files from backend
from fastapi import FastAPI
from app.api.endpoints import(
    user, activity_log, conversation_log, device_integration, emergency_contact,
    fall_event, health, health_vital, medication, mental_health_log, reminder_log,
    suggestion, ui_preference,
)

app = FastAPI(title="AI Health Assistant API")

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(activity_log.router, prefix="/activity_logs", tags=["Activity Logs"])
app.include_router(conversation_log.router, prefix="/conversation_logs", tags=["Conversation Logs"])
app.include_router(device_integration.router, prefix="/device_integrations", tags=["Device Integrations"])
app.include_router(emergency_contact.router, prefix="/emergency_contacts", tags=["Emergency Contacts"])
app.include_router(fall_event.router, prefix="/fall_events", tags=["Fall Events"])
app.include_router(health.router, prefix="/health_data", tags=["Health Data"])
app.include_router(health_vital.router, prefix="/health_vitals", tags=["Health Vitals"])
app.include_router(medication.router, prefix="/medications", tags=["Medications"])
app.include_router(mental_health_log.router, prefix="/mental_health_logs", tags=["Mental Health Logs"])
app.include_router(reminder_log.router, prefix="/reminder_logs", tags=["Reminder Logs"])
app.include_router(suggestion.router, prefix="/suggestions", tags=["Suggestions"])
app.include_router(ui_preference.router, prefix="/ui_preferences", tags=["UI Preferences"])

#import dev
import HealthMonitoringCore.py as HealthMonitoring
import ToDoList.py as ToDoList

#import ai models
import anomalydetection.py as AnomalyDetection
import chatbot.py as ChatBot

#define variables with data

#call functions on variables#

#if user data/information records are empty
    #prompt login page/profile page
    #display message prompting them to fill in information

#else if user information is there
    #display home page from front end 
        #load data from backend to front end
        #load core functionality

#import the health screen
class HealthScreen(Screen):
    def on_enter(self, *args):
        # get the container by its KV id
        container = self.ids.vitals_graph_container
        container.clear_widgets()

        # get the Matplotlib Figure from your backend
        fig = HealthGraph.showVitals()

        # wrap it in a Kivy widget
        canvas_widget = FigureCanvasKivyAgg(fig)

        # add to the container
        container.add_widget(canvas_widget) 
    
class MedBuddyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(HealthScreen(name="health"))
        # … add other screens …
        return self.sm

if __name__ == "__main__":
    MyApp().run()

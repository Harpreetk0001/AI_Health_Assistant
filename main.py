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
import Updated_medbuddy

#import dev
import HealthMonitoringCore
import ToDoList

#define variables with data

#call functions on variables#

#if user data/information records are empty
    #prompt login page/profile page
    #display message prompting them to fill in information

#else if user information is there
    #display home page from front end 
        #load data from backend to front end
        #load core functionality


class HomeScreen(Screen): pass

#import the health screen
class HealthScreen(Screen):
    def on_enter(self, *args):
        self.ids.vitals_graph_container.clear_widgets()
        self.ids.vitals_graph_container.add_widget(HealthMonitoringCore.showVitals())
    
class MedBuddyApp(App):
    def build(self):
        self.title = "MedBuddy"
        # Make an emoji font available to KV
        self.emoji_font = find_emoji_font()
        self.sm = Builder.load_string(KV)
        return self.sm

    # Simple stub to show input flow on Chatbot
    def fake_send(self, user_input):
        txt = user_input.text.strip()
        if not txt:
            return
        user_input.text = ""
        self.sm.current = "chat"

class RoutineScreen(Screen): pass
class ChatbotScreen(Screen): pass
class SupportScreen(Screen): pass
class ProfileScreen(Screen): pass
class SettingsScreen(Screen): pass
class SOSConfirmScreen(Screen): pass

if __name__ == "__main__":
    MedBuddyApp().run()

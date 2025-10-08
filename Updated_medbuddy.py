from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.core.window import Window
import os, sys
import chatbot  # chatbot.py file
from threading import Thread
from kivy.clock import Clock
from anomalydetection import run_fall_detection # anomalydetection.py file
from datetime import datetime
from kivy.properties import StringProperty
import time
import webbrowser                               #imported webbrowser for yt exercise video links

from HealthMonitoringCore import HealthGraph    # for the vitals graph
from ToDoList import ToDoList                   # for the task manager
from kivy.uix.label import Label


# App-wide background color (DBE4E0)
Window.clearcolor = (219/255, 228/255, 224/255, 1)

def find_emoji_font() -> str:
    """Return a path to an installed emoji-capable font (best effort)."""
    candidates = []
    if sys.platform.startswith("win"):
        candidates += [
            r"C:\Windows\Fonts\seguiemj.ttf",       
            r"C:\Windows\Fonts\SegoeUIEmoji.ttf",
        ]
    elif sys.platform == "darwin":
        candidates += ["/System/Library/Fonts/Apple Color Emoji.ttc"]
    else:
        candidates += [
            "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
            "/usr/share/fonts/truetype/twemoji/TwitterColorEmoji-SVGinOT.ttf",
            "/usr/share/fonts/truetype/emojione/emojione-android.ttf",
        ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return ""  


KV = """
#:import dp kivy.metrics.dp

# ---------- Added Rounded button styles ----------

<RoundedField@TextInput>:
    background_normal: ""
    background_active: ""
    size_hint_y: None
    height: dp(44)
    font_size: "16sp"
    cursor_color: 0, 0, 0, 1
    foreground_color: 0, 0, 0, 1
    hint_text_color: 0.45, 0.48, 0.52, 1
    write_tab: False
    multiline: False
    disabled: False
    readonly: False
    halign: "center"

    # Centers text vertically by adjusting internal padding
    padding: [0, (self.height - self.line_height) / 2]

    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12), dp(12), dp(12), dp(12)]
        Color:
            rgba: (0.76, 0.79, 0.83, 1) if not self.focus else (0.16, 0.56, 0.96, 1)
        Line:
            width: 1.25
            rounded_rectangle: (self.x, self.y, self.width, self.height, dp(12))

<RoundedPrimaryButton@Button>:
    background_normal: ""
    background_down: ""
    background_color: 0.16, 0.56, 0.96, 1
    color: 1, 1, 1, 1
    font_size: "17sp"
    bold: True
    size_hint_y: None
    height: dp(48)
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(24), dp(24), dp(24), dp(24)]


# pill-style input just for chat
<ChatInputField@TextInput>:
    background_normal: ""
    background_active: ""
    multiline: False
    font_size: "16sp"
    size_hint_y: None
    height: dp(48)
    cursor_color: 0, 0, 0, 1
    foreground_color: 0, 0, 0, 1
    hint_text_color: 0.45, 0.48, 0.52, 1
    # left-align text, but center it vertically
    halign: "left"
    padding: [dp(14), (self.height - self.line_height) / 2]

    # draw everything behind the text so typing works
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(24), dp(24), dp(24), dp(24)]
        Color:
            rgba: (0.76, 0.79, 0.83, 1) if not self.focus else (0.16, 0.56, 0.96, 1)
        Line:
            width: 1.25
            rounded_rectangle: (self.x, self.y, self.width, self.height, dp(24))

# rounded primary button for Send
<SendButton@Button>:
    background_normal: ""
    background_down: ""
    background_color: 0.16, 0.56, 0.96, 1
    color: 1, 1, 1, 1
    bold: True
    font_size: "17sp"
    size_hint_y: None
    height: dp(48)
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(24), dp(24), dp(24), dp(24)]

<RoundedButton@Button>:
    background_normal: ""        # disable default square background
    background_down: ""          # disable pressed state image
    background_color: 0.43, 0.79, 0.94, 1
    color: 1, 1, 1, 1
    size_hint_y: None
    height: dp(44)
    font_size: "16sp"
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.height/2, self.height/2, self.height/2, self.height/2]

<RoundedToggleButton@ToggleButton>:
    background_normal: ""
    background_down: ""
    background_color: (0.43, 0.79, 0.94, 1) if self.state == "down" else (0.7, 0.7, 0.7, 1)
    color: 1, 1, 1, 1
    size_hint_y: None
    height: dp(44)
    font_size: "16sp"
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.height/2, self.height/2, self.height/2, self.height/2]

<RoundedSpinner@Spinner>:
    background_normal: ""
    background_down: ""
    background_color: 0.3, 0.5, 0.8, 1
    color: 1, 1, 1, 1
    font_size: "16sp"
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.height/2, self.height/2, self.height/2, self.height/2]


# ---------- Reusable building blocks ----------

<NavBar@FloatLayout>:
    size_hint_y: None
    height: dp(96)
    padding: dp(8), dp(8)
    spacing: dp(8)
    canvas.before:
        Color:
            rgba: 0.92, 0.94, 0.96, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(16), dp(16), 0, 0]
    RoundedButton:
        pos_hint: {'center_x': 0.16, 'center_y': 0.5}
        size_hint: (0.075, 0.7)
        background_normal: 'home_normal.png'
        background_down: 'home_down.png'
        on_release: app.sm.current = "home"
    RoundedButton:
        pos_hint: {'center_x': 0.32, 'center_y': 0.5}
        size_hint: (0.075, 0.7)
        background_normal: 'health_normal.png'
        background_down: 'health_down.png'
        on_release: app.sm.current = "health"
    RoundedButton:
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: (0.075, 0.7)
        background_normal: 'routine_normal.png'
        background_down: 'routine_down.png'
        on_release: app.sm.current = "routine"
    RoundedButton:
        pos_hint: {'center_x': 0.66, 'center_y': 0.5}
        size_hint: (0.075, 0.7)
        background_normal: 'chatbot_normal.png'
        background_down: 'chatbot_down.png'
        on_release: app.sm.current = "chat"
    RoundedButton:
        pos_hint: {'center_x': 0.82, 'center_y': 0.5}
        size_hint: (0.075, 0.7)
        background_normal: 'profile_normal.png'
        background_down: 'profile_down.png'
        on_release: app.sm.current = "profile"

<Card@BoxLayout>:
    orientation: "vertical"
    size_hint_y: None
    height: self.minimum_height
    padding: dp(12)
    spacing: dp(8)
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(16), dp(16), dp(16), dp(16)]
    Label:
        id: title_lbl
        text: root.title if hasattr(root, "title") else ""
        bold: True
        font_size: "18sp"
        color: 0.15,0.15,0.18,1
        size_hint_y: None
        height: self.texture_size[1]
    BoxLayout:
        id: body_box
        size_hint_y: None
        height: self.minimum_height

<ActionBtn@Button>:
    font_size: "18sp"
    size_hint_y: None
    height: dp(48)
    background_normal: ""
    background_color: 0.16, 0.56, 0.96, 1
    color: 1,1,1,1
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(15), dp(15), dp(15), dp(15)]

<Tag@Label>:
    size_hint_y: None
    height: dp(28)
    padding_x: dp(8)
    color: 1,1,1,1
    canvas.before:
        Color:
            rgba: 0.15,0.5,0.9,1
        RoundedRectangle:
            pos: self.x, self.y
            size: self.width, self.height
            radius: [dp(10), dp(10), dp(10), dp(10)]

<SOSBtn@Button>:
    size_hint: None, None
    size: dp(56), dp(56)
    text: "SOS"
    font_size: "16sp"
    bold: True
    # make the built-in background transparent so it won't cover our Ellipse
    background_normal: ""
    background_down: ""
    background_color: 0, 0, 0, 0
    color: 0, 0, 0, 1
    on_release: app.sm.current = "sos"
    canvas.before:
        Color:
            rgba: 0.90, 0.10, 0.10, 1
        Ellipse:
            pos: self.pos
            size: self.size

<SettingsBtn@Button>:
    size_hint: None, None
    size: dp(56), dp(56)
    text: "Settings"
    font_size: "12sp"
    bold: True
    background_normal: ""
    background_down: ""
    background_color: 0, 0, 0, 0
    color: 0, 0, 0, 1
    on_release: app.sm.current = "settings"
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Ellipse:
            pos: self.pos
            size: self.size


<Header@BoxLayout>:
    size_hint_y: None
    height: dp(64)
    padding: dp(12), dp(8)
    spacing: dp(12)
    canvas.before:
        Color:
            rgba: 0.96, 0.97, 0.98, 1
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: root.title if hasattr(root, "title") else "MedBuddy"
        font_size: "22sp"
        bold: True
        color: 0.1,0.1,0.13,1

# ---- Emoji-capable widgets ----
<EmojiLabel@Label>:
    # Use the emoji font if available
    font_name: app.emoji_font if app.emoji_font else self.font_name

<EmojiButton@Button>:
    font_name: app.emoji_font if app.emoji_font else self.font_name

<ActionButtons@BoxLayout>:       #---added this to every UI Screen>
    orientation: 'vertical'
    SOSBtn
    SettingsBtn

# ---------- Screens ----------


    

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)

        Header:
            title: "MedBuddy"

        # Reminders row with SOS and clearer typography on light background
        BoxLayout:
            size_hint_y: None
            spacing: dp(12)
            ActionButtons
            BoxLayout:
                orientation: "vertical"
                spacing: dp(4)
                canvas.before:
                    Color:
                        rgba: 1,1,1,1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(12), dp(12), dp(12), dp(12)]
                Label:
                    text: "Reminders"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(6)
                    bold: True
                    color: 0.12,0.12,0.15,1
                Label:
                    text: "Doctor's Appointment  •  11:30 AM"
                    color: 0.15,0.15,0.18,1
                    size_hint_y: None
                    height: self.texture_size[1] + dp(6)

        Card:
            title: "Alerts"
            BoxLayout:
                size_hint_y: None
                height: dp(40)
                spacing: dp(8)
                RoundedButton:
                    text: "Blood Pressure Spiked"
                    background_normal: ""
                    background_color: 0.95, 0.35, 0.35, 1
                    color: 1,1,1,1
                    size_hint_y: None
                    height: dp(40)
                    on_release: app.sm.current = "health"

        Card:
            title: "Vitals"
            GridLayout:
                cols: 5
                size_hint_y: None
                height: dp(128)
                padding: 0, dp(4)
                spacing: dp(8)

                EmojiLabel:
                    text: "❤️\\n72"
                    font_size: 40
                    color: 0, 0, 0, 1
                EmojiLabel:
                    text: "🩸\\n120/80"
                    font_size: 40
                    color: 0, 0, 0, 1
                EmojiLabel:
                    text: "💧\\nGood"
                    font_size: 40
                    color: 0, 0, 0, 1
                EmojiLabel:
                    text: "😴\\n7h"
                    font_size: 40
                    color: 0, 0, 0, 1
                EmojiLabel:
                    text: "🚶\\n3.2k"
                    font_size: 40
                    color: 0, 0, 0, 1

        Widget:

        # Expanded nav for all screens
        NavBar

<HealthScreen>:
    name: "health"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)

        Header:
            title: "Health Monitoring"

        BoxLayout:
            spacing: dp(12)
            size_hint_y: None
            height: dp(64)
            ActionButtons

        Card:
            title: "Trends"
            BoxLayout:
                id: vitals_graph_container
                size_hint_y: None
                height: dp(200)
                # we’ll inject the canvas here

        Card:
            title: "Alerts"
            Label:
                text: "Blood Pressure Spiked"
                size_hint_y: None
                height: dp(36)
                color: 0.8,0.1,0.1,1

        Card:
            title: "Exercise Videos"                                    #---Added yt video links>
            BoxLayout:
                size_hint_y: None
                height: dp(44)
                spacing: dp(8)

                ActionBtn:
                    text: "Stretching"
                    on_release: app.open_video("https://www.youtube.com/watch?v=yI4hnt0IXDw")

                ActionBtn:
                    text: "▶ Cardio"
                    on_release: app.open_video("https://www.youtube.com/watch?v=LYJ3U0Fs4dg")

                ActionBtn:
                    text: "⏭ Strength"
                    on_release: app.open_video("https://www.youtube.com/watch?v=0UaHYhBX6Rw")

        Widget:

        NavBar

<RoutineScreen>:
    name: "routine"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)

        Header:
            title: "Daily Routine"

        BoxLayout:
            spacing: dp(12)
            size_hint_y: None
            height: dp(64)
            ActionButtons

        ScrollView:
            size_hint_y: None
            height: dp(200)
            BoxLayout:
                id: tasks_container
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height

        Card:
            title: "Today (Mon)"
            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(6)
                # simple timeline items
                EmojiLabel:
                    text: "7:00  •  Take Medication  ✅"
                    color: 0.12,0.12,0.15,1
                    size_hint_y: None
                    height: self.texture_size[1] + dp(4)
                EmojiLabel:
                    text: "8:00  •  Hydration  ✅"
                    color: 0.12,0.12,0.15,1
                    size_hint_y: None
                    height: self.texture_size[1] + dp(4)
                EmojiLabel:
                    text: "10:00 •  Doctor Appointment  ⏳"
                    color: 0.12,0.12,0.15,1
                    size_hint_y: None
                    height: self.texture_size[1] + dp(4)

        Card:
            title: "Reminder Types"
            GridLayout:
                cols: 2
                size_hint_y: None
                height: dp(120)
                spacing: dp(8)
                RoundedToggleButton:
                    text: "Exercise (ON)" if self.state=="normal" else "Exercise (OFF)"
                    on_press: app.on_toggle_pressed(self)
                RoundedToggleButton:
                    text: "Sleep (ON)" if self.state=="normal" else "Sleep (OFF)"
                    on_press: app.on_toggle_pressed(self)
                RoundedToggleButton:
                    text: "Medication (ON)" if self.state=="normal" else "Medication (OFF)"
                    on_press: app.on_toggle_pressed(self)
                RoundedToggleButton:
                    text: "Hydration (ON)" if self.state=="normal" else "Hydration (OFF)"
                    on_press: app.on_toggle_pressed(self)

        Widget:

        NavBar

<ChatbotScreen>:
    name: "chat"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)
        Header:
            title: "AI Health Assistant"
        BoxLayout:
            spacing: dp(12)
            size_hint_y: None
            height: dp(64)
            ActionButtons
        Card:
            title: "Conversation"
            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: dp(220)
                spacing: dp(8)
                AsyncImage:
                    source: "https://t4.ftcdn.net/jpg/14/09/15/51/360_F_1409155154_pALBjHEVKuYFUrl9HJ9Q3zgpCuaHyFpI.jpg"
                    size_hint_y: None
                    height: dp(170)
                    allow_stretch: True
                    keep_ratio: True
                Label:
                    id: response_label
                    text: "Hello! This is a UI-only demo."
                    color: 0.12,0.12,0.15,1
                    size_hint_y: None
                    height: self.texture_size[1] + dp(6)
        BoxLayout:
            size_hint_y: None
            height: dp(56)
            spacing: dp(8)
            ChatInputField:
                id: user_input
                hint_text: "Type a message…"
                size_hint_x: 1
                
            ActionBtn:
                text: "Send"
                on_release: app.fake_send(user_input)
        Widget:
        
        NavBar

<SupportScreen>:
    name: "support"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)

        Header:
            title: "My Support Network"

        Card:
            title: "Contacts"
            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(8)

                BoxLayout:
                    size_hint_y: None
                    height: dp(56)
                    spacing: dp(8)
                    canvas.before:
                        Color:
                            rgba: 0.98,0.93,0.90,1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(12), dp(12), dp(12), dp(12)]
                    Label:
                        text: "Belinda Wen  •  Daughter"
                        color: 0.12,0.12,0.15,1
                    RoundedButton:
                        text: "Call"

                BoxLayout:
                    size_hint_y: None
                    height: dp(56)
                    spacing: dp(8)
                    canvas.before:
                        Color:
                            rgba: 0.92,0.96,0.99,1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(12), dp(12), dp(12), dp(12)]
                    Label:
                        text: "Anna Tanaka  •  Nurse"
                        color: 0.12,0.12,0.15,1
                    RoundedButton:
                        text: "Call"

                BoxLayout:
                    size_hint_y: None
                    height: dp(56)
                    spacing: dp(8)
                    canvas.before:
                        Color:
                            rgba: 0.90,0.95,0.98,1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(12), dp(12), dp(12), dp(12)]
                    Label:
                        text: "Jimmy Cole  •  Nephew"
                        color: 0.12,0.12,0.15,1
                    RoundedButton:
                        text: "Call"

        Widget:

        NavBar

<ProfileScreen>:
    name: "profile"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)

        Header:
            title: "User Profile"

        BoxLayout:
            spacing: dp(12)
            size_hint_y: None
            height: dp(64)
            ActionButtons

        Card:
            title: "Details"
            GridLayout:
                cols: 2
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(10)
                row_default_height: dp(44)
                row_force_default: True

                # Name
                Label:
                    text: "Name"
                    color: 0, 0, 0, 1
                    size_hint_x: .35
                    halign: "right"
                    valign: "middle"
                    text_size: self.size
                RoundedField:
                    id: fld_name
                    size_hint_x: .65
                    text: "Harry"
                    hint_text: "Full name"
                    write_tab: False

                # Age
                Label:
                    text: "Age"
                    color: 0, 0, 0, 1
                    size_hint_x: .35
                    halign: "right"
                    valign: "middle"
                    text_size: self.size
                RoundedField:
                    id: fld_age
                    size_hint_x: .65
                    text: "78"
                    hint_text: "Age"
                    input_filter: "int"
                    write_tab: False

                # Primary Caregiver
                Label:
                    text: "Primary Caregiver"
                    color: 0, 0, 0, 1
                    size_hint_x: .35
                    halign: "right"
                    valign: "middle"
                    text_size: self.size
                RoundedField:
                    id: fld_caregiver
                    size_hint_x: .65
                    text: "Belinda Wen"
                    hint_text: "Caregiver name"
                    write_tab: False

                # Caregiver Phone
                Label:
                    text: "Caregiver Phone"
                    color: 0, 0, 0, 1
                    size_hint_x: .35
                    halign: "right"
                    valign: "middle"
                    text_size: self.size
                RoundedField:
                    id: fld_phone
                    size_hint_x: .65
                    text: "+61 223 344 556"
                    hint_text: "Phone number"
                    write_tab: False

        BoxLayout:
            size_hint_y: None
            height: dp(64)
            padding: dp(8), 0
            RoundedPrimaryButton:
                text: "💬  Support"
                on_release: app.sm.current = "support"

        NavBar

<SettingsScreen>:
    name: "settings"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)

        Header:
            title: "Settings"

        Card:
            title: "Accessibility"
            GridLayout:
                cols: 2
                size_hint_y: None
                height: dp(120)
                spacing: dp(8)

                Label:
                    text: "Light Mode"
                    color: 0, 0, 0, 1 
                RoundedToggleButton:
                    text: "ON" if self.state == "down" else "OFF"
                    state: "down"

                Label:
                    text: "Speech to Text"
                    color: 0, 0, 0, 1
                RoundedToggleButton:
                    text: "ON" if self.state == "down" else "OFF"
                    state: "down"

                Label:
                    text: "Hearing Aid"
                    color: 0, 0, 0, 1
                RoundedToggleButton:
                    text: "OFF"

        Card:
            title: "Font Size"
            Slider:
                min: 14
                max: 28
                value: 22
                size_hint_y: None
                height: dp(36)

        Card:
            title: "Language"
            RoundedSpinner:
                text: "English"
                values: ["English","简体中文","Español","हिंदी"]
                size_hint_y: None
                height: dp(40)

        NavBar

<SOSConfirmScreen>:
    name: "sos"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)

        Header:
            title: "Emergency"

        BoxLayout:
            orientation: "vertical"
            padding: dp(16)
            spacing: dp(16)
            size_hint_y: None
            height: dp(280)
            canvas.before:
                Color:
                    rgba: 1, 0.92, 0.92, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(16), dp(16), dp(16), dp(16)]
            Label:
                id: help_label
                text: "HELP"
                font_size: "64sp"
                color: 0.9, 0.1, 0.1, 1
                bold: True
            Label:
                id: sos_log_label
                text: "Confirm call?"
                font_size: "20sp"
                color: 0.2, 0.2, 0.25, 1
            BoxLayout:
                size_hint_y: None
                height: dp(56)
                spacing: dp(12)
                ActionBtn:
                    text: "Yes"
                    background_color: 0.12, 0.65, 0.36, 1
                    on_release: app.sm.current = "home"
                ActionBtn:
                    text: "No"
                    background_color: 0.65, 0.12, 0.18, 1
                    on_release: app.sm.current = "home"

        ScrollView:
            size_hint_y: 1
            do_scroll_x: False

            Label:
                id: sos_log_label_2
                text: root.log_text
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
                valign: "top"
                padding: dp(10), dp(10)

        Widget:

        NavBar

# Root

ScreenManager:
    HomeScreen:
    HealthScreen:
    RoutineScreen:
    ChatbotScreen:
    SupportScreen:
    ProfileScreen:
    SettingsScreen:
    SOSConfirmScreen:
"""

class HomeScreen(Screen): pass
class HealthScreen(Screen): pass
class RoutineScreen(Screen): pass
class ChatbotScreen(Screen): pass
class SupportScreen(Screen): pass
class ProfileScreen(Screen): pass
class SettingsScreen(Screen): pass
class SOSConfirmScreen(Screen): 
    
    log_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_log_time = 0
        self.log_cooldown = 10  # seconds

    def update_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        new_entry = f"[{timestamp}] {message}"  # define new_entry
        max_entries = 10
        entries = self.log_text.strip().split('\n') if self.log_text.strip() else []
        entries.append(new_entry)
        if len(entries) > max_entries:
            entries = entries[-max_entries:]
        self.log_text = '\n'.join(entries) + '\n'

class MedBuddyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alert_count = 0
        self.max_alerts = 5
        self.last_log_time = 0
        self.log_cooldown = 10  # seconds

    def open_video(self, url):            #---Added Open Video webbrowser>
        webbrowser.open(url)

    def build(self):
        self.title = "MedBuddy"
        # Make an emoji font available to KV
        self.emoji_font = find_emoji_font()
        self.sm = Builder.load_string(KV)

         # Initialize chatbot here
        chatbot.initialize()

        # Start fall detection thread on app start:
        self.check_fall_and_log()
        Clock.schedule_interval(lambda dt: self.check_fall_and_log(), 30)  # every 30 seconds

        return self.sm

    def on_start(self):
         # 1) generate the FigureCanvas
         canvas = HealthGraph.showVitals()
         # 2) find the Health screen’s container and add it
         health_screen = self.sm.get_screen("health")
         health_screen.ids.vitals_graph_container.add_widget(canvas)

         # 3) (optional) set up your To-Do list
         self.init_todo_list()

    def init_todo_list(self):
        # instantiate the ToDoList
        self.todo = ToDoList()
        # get the Routine screen and its container
        routine = self.sm.get_screen("routine")
        container = routine.ids.tasks_container
        # add each task as a Label (or your custom widget)
        for task in self.todo.tasks:

            label1 = Label(
                text=f"{task.title} \n{task.description} \nDue: {task.dueDateTime} \nStatus: {task.status}",
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=dp(75)
            )
            
            container.add_widget(label1)


    #filtering to-do list
    def on_toggle_pressed(self, toggle_button):
        # get the Routine screen and its container
        routine = self.sm.get_screen("routine")
        container = routine.ids.tasks_container

        eList = self.todo.displayByTag("Exercise")
        sList = self.todo.displayByTag("Sleep")
        hList = self.todo.displayByTag("Hydration")
        mList = self.todo.displayByTag("Medication")

        filterList = []

        for e in eList:
            filterList.append(e)
        for s in sList:
            filterList.append(s)
        for h in hList:
            filterList.append(h)
        for m in mList:
            filterList.append(m)

        container.clear_widgets()

        if toggle_button.state == "down":
            if "Exercise" in toggle_button.text:
                print("EXERCISE BUTTON ON")
                for et in eList:
                    if et not in filterList:
                        filterList.append(et)

            if "Sleep" in toggle_button.text:
                print("SLEEP BUTTON ON")
                for st in sList:
                    if st not in filterList:
                        filterList.append(st)

            if "Hydration" in toggle_button.text:
                print("HYDRATION BUTTON ON")
                for ht in hList:
                    if ht not in filterList:
                        filterList.append(ht)

            if "Medication" in toggle_button.text:
                print("MEDICATION BUTTON ON")
                for mt in mList:
                    if mt not in filterList:
                        filterList.append(mt)
                        
        else:
            if "Exercise" in toggle_button.text:
                toggle_button.text = "Exercise (OFF)"
                print("EXERCISE BUTTON OFF")
                for e_t in eList:
                    if e_t in filterList:
                        filterList.remove(e_t)

            if "Sleep" in toggle_button.text:
                toggle_button.text = "Sleep (OFF)"
                print("SLEEP BUTTON OFF")
                for s_t in sList:
                    if s_t in filterList:
                        filterList.remove(s_t)

            if "Hydration" in toggle_button.text:
                toggle_button.text = "Hydration (OFF)"
                print("HYDRATION BUTTON OFF")
                for h_t in hList:
                    if h_t in filterList:
                        filterList.remove(h_t)

            if "Medication" in toggle_button.text:
                toggle_button.text = "Medication (OFF)"
                print("MEDICATION BUTTON OFF")
                for m_t in mList:
                    if m_t in filterList:
                        filterList.remove(m_t)


        #display filtered tasks
        for ftask in filterList:
            ftaskText = ftask.getTask()
             
            label2 = Label(
                text=ftaskText,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=dp(75)
            )

            container.add_widget(label2)



    #Anomalydetection.py

    def check_fall_and_log(self):
        # Run fall detection in a separate thread to avoid blocking UI
        def detection_thread():
            if self.alert_count >= self.max_alerts:
                return  # stop detection after max alerts
            result = run_fall_detection()
            if result:
                self.alert_count += 1
            Clock.schedule_once(lambda dt: self._update_sos_log(result))
        Thread(target=detection_thread, daemon=True).start()
    

    def _update_sos_log(self, result):
        current_time = time.time()
        if current_time - self.last_log_time < self.log_cooldown:
            return
        self.last_log_time = current_time

        sos_screen = self.sm.get_screen("sos")
        if result:
            sos_screen.update_log(f"ALERT: {result}")
             # self.sm.current = "sos"
        else:
            sos_screen.update_log("No fall detected.")
        
            #  switch to SOS screen if you want user to see it immediately:
            #self.sm.current = "sos"

    # Simple stub to show input flow on Chatbot
    def fake_send(self, user_input_widget):
        user_text = user_input_widget.text.strip()
        if not user_text:
            self.update_label("Please type something.")
            return
        user_input_widget.text = ""
        Thread(target=self.process_interaction, args=(user_text,)).start()

    def process_interaction(self, user_text):
        print(f"Generating response for: {user_text!r}")
        response = chatbot.generate_response(user_text)
        print(f"Got response: {response!r}")
        Clock.schedule_once(lambda dt: self.update_label(response), 0)
        chatbot.speak_response(response)
        

    def update_label(self, text):
        try:
            screen = self.sm.get_screen("chat")
            lbl = screen.ids.response_label
            lbl.text = text
            lbl.height = lbl.texture_size[1] + 10  # Add some padding
            print(f"Updated label to: {text}")
        except Exception as e:
            print("Could not update response label:", e)

if __name__ == "__main__":
    MedBuddyApp().run()











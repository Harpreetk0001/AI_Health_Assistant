import json
import numpy as np
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import smtplib

#import all the files from the backend

class ContactList:
    def __init__(self):
        self.contacts = []
        self.emergencyContacts = []

    def getAllContacts(self):
        for c in self.contacts:
            print(f"CONTACT {c}")
            c.getContact()

    def getEmergencyContacts(self):
        for ec in self.emergencyContacts:
            print(f"CONTACT {ec}")
            ec.getContact()
            
    def addContact(self, Contact):
        self.contacts.append(Contact)
        if Contact.favourite == True:
            self.emergencyContacts.append(Contact)

        print("AFTER ADDING CONTACT")

        #add contact to DB
        #possibly reformat as DB record

    def updateContact(self, Contact, attribute, new_value):
        if attribute == "Name":
            Contact.name = new_value
        elif attribute == "Relationship":
            Contact.relationship = new_value
        elif attribute == "Phone Number":
            Contact.phone_no = new_value
        elif attribute == "Email":
            Contact.email = new_value
        elif attribute == "Favourite":
            Contact.favourite = new_value
            self.checkFavourite(Contact)
        elif attribute == "Image":
            Contact.profile = new_value

        print("AFTER UPDATING CONTACT")

        #update contact in DB
        #possibly reformat as DB record

    def checkFavourite(self, Contact):
        if Contact.favourite == True:
            self.emergencyContacts.append(Contact)
            
        elif Contact.favourite == False:
            self.emergencyContacts.remove(Contact)

    def removeContact(self, Contact):
        if Contact in self.contacts:
            self.contacts.remove(Contact)
        if Contact in self.emergencyContacts:
            self.emergencyContacts.remove(Contact)

        print("AFTER REMOVING CONTACT")

        #remove from DB
        #update contact in DB
        #possibly reformat as DB record

    def callEmergencyContacts(self):

        callList = []
        
        for ec in self.emergencyContacts:
            number = ec.callContact()
            callList.append(number)

        print("CALL LIST: ", callList)

        return callList

    def emailContacts(self, message):
        for c in self.contacts:
            c.emailContact(message)
    
                
class Contact:
    def __init__(self, name, relationship, phone_no, email, pfp, favourite=False):
        self.name = name
        self.relationship = relationship
        self.phone_no = phone_no
        self.email = email
        self.profile = pfp
        self.favourite = favourite

    def getContact(self):
        
        print(
        f'''
        Image: {self.profile}
        Name: {self.name}
        Relationship: {self.relationship}
        Phone Number: {self.phone_no}
        Email: {self.email}
        Favourite: {self.favourite}
        '''
        )

    def setContact(self, name, relationship, phone_no, email, pfp, favourite):
        self.name = name
        self.relationship = relationship
        self.phone_no = phone_no
        self.email = email
        self.favourite = favourite
        self.profile = pfp

    def callContact(self):
        print(f'CONTACT {self.name}\'s PHONE NUMBER: {self.phone_no}')
        return self.phone_no

    def emailContact(self, alert_message):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("medbuddy.teaminnovators@gmail.com", "aaaf uszs zowh dxgo")
        message = f"Dear {self.name}, \n\nThis is an alert for your loved one. \n\n{alert_message} \n\nThis is an automated email from MedBuddy"
        s.sendmail("sender_email_id", self.email, message)
        s.quit()

        print("email sent!")

###TEST CASES###

#SET UP#
CL = ContactList()

c1 = Contact("Belinda Wen", "Daughter", "0435384765", "medbuddy.teaminnovators@gmail.com", "BelindaPFP.png", True)
c2 = Contact("Anna Tanaka", "Nurse", "0464911899", "medbuddy.teaminnovators@gmail.com", "AnnaPFP.png", False)
c3 = Contact("Jimmy Cole", "Son", "0463377211", "medbuddy.teaminnovators@gmail.com", "JimmyPFP.png", False)

CL.addContact(c1)
CL.addContact(c2)
CL.addContact(c3)

#ContactList FUNCTION TESTS#
CL.getAllContacts()
CL.getEmergencyContacts()

#CL.updateContact(c3, "Relationship", "nephew")
#CL.getAllContacts()
#CL.getEmergencyContacts()

#CL.updateContact(c2, "Favourite", True)
#CL.getAllContacts()
#CL.getEmergencyContacts()

#CL.removeContact(c3)
#CL.getAllContacts()
#CL.getEmergencyContacts()

#CL.callEmergencyContacts()
#CL.getAllContacts()
#CL.getEmergencyContacts()

#CL.emailContacts("BP spiked")
#CL.getAllContacts()
#CL.getEmergencyContacts()

#Contact FUNCTION TESTS#
#c3.callContact()

#print()

#c1.emailContact("hello")


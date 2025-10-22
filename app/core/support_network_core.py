from typing import List

class Contact:
    def __init__(self, name: str, relationship: str = "", phone_no: str = "", email: str = "", profile: str = "", favourite: bool = False):
        self.name = name
        self.relationship = relationship
        self.phone_no = phone_no
        self.email = email
        self.profile = profile
        self.favourite = favourite

class ContactList:
    def __init__(self):
        self.contacts: List[Contact] = []
        self.emergencyContacts: List[Contact] = []

    def addContact(self, c: Contact):
        self.contacts.append(c)
        if c.favourite:
            self.emergencyContacts.append(c)
        # TODO: persist to backend

    def updateContact(self, c: Contact, attribute: str, new_value):
        if c in self.contacts:
            setattr(c, attribute, new_value)
            self.emergencyContacts = [x for x in self.contacts if x.favourite]
            # TODO: persist to backend

    def deleteContact(self, c: Contact):
        if c in self.contacts:
            self.contacts.remove(c)
            if c in self.emergencyContacts:
                self.emergencyContacts.remove(c)
            # TODO: delete from backend

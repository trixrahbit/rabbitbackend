from sqlalchemy.orm import relationship

from models.models import Client, User
from models.projects.projects_model import Project, Task, Story

Client.projects = relationship("Project", order_by=Project.id, back_populates="client")
Project.client = relationship("Client", back_populates="projects")

# Relationship between Task and Checklist
from models.checklist_model import Checklist
Task.checklist = relationship("Checklist", back_populates="task", uselist=False)
Checklist.task = relationship("Task", back_populates="checklist", uselist=False)

# Relationship between Story and Checklist
Story.checklist = relationship("Checklist", uselist=False, back_populates="story")
Checklist.story = relationship("Story", uselist=False, back_populates="checklist")

#Relationship between User and Calendar
from models.calendar.calendar_model import CalendarEvent

User.calendar_events = relationship("CalendarEvent", back_populates="user")
CalendarEvent.user = relationship("User", back_populates="calendar_events")
Client.calendar_events = relationship("CalendarEvent", back_populates="client")
CalendarEvent.client = relationship("Client", back_populates="calendar_events")

#Relationship between User and NotificationSettings
from models.calendar.notificationsettings_model import NotificationSettings

User.notification_settings = relationship("NotificationSettings", back_populates="user")
NotificationSettings.user = relationship("User", back_populates="notification_settings")

#Relationship between User and BrandingSettings
from models.calendar.brandingsettings_model import BrandingSettings

User.branding_settings = relationship("BrandingSettings", back_populates="user")
BrandingSettings.user = relationship("User", back_populates="branding_settings")

#Relationship between User and BookingLink
from models.calendar.bookinglink_model import BookingLink

User.booking_links = relationship("BookingLink", back_populates="user")
BookingLink.user = relationship("User", back_populates="booking_links")


#Relationship bewteen client and branding settings
Client.branding_settings = relationship("BrandingSettings", back_populates="client")
BrandingSettings.client = relationship("Client", back_populates="branding_settings")


from models.clientModel.sla_model import SLA, SLACondition, Priority, Impact
from models.clientModel.billingagreement_model import BillingAgreement, BillingAgreementItem
from models.models import Client
from models.models import Organization
from models.clientModel.ticket_model import Ticket
from models.models  import User




import logging
import uuid
from datetime import datetime
import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.integrations.outlook.outlook_oauth import refresh_access_token_if_needed
from api.user.user_router import get_db
from core.calendar.calavail import fetch_user_available_times
from models import User
from models.calendar.calendar_model import CalendarEvent as CalendarEventModel
from models.models import BusinessHours
from root.root_elements import router
from schemas.calendar.calendar_schema import CalendarEventCreate, CalendarEventUpdate, \
    CalendarEvent as CalendarEventSchema, UserBookingUrlUpdate
from models.calendar.bookinglink_model import BookingLink as BookingLinkModel
from schemas.calendar.bookinglink_schema import BookingLinkCreate, BookingLink, EventRequest
from models.calendar.brandingsettings_model import BrandingSettings as BrandingSettingsModel, BrandingSettings
from schemas.calendar.brandsettings_schema import BrandingSettingsCreate, BrandingSettings as BrandingSettingsSchema
from models.calendar.notificationsettings_model import NotificationSettings as NotificationSettingsModel
from schemas.calendar.notification_schema import NotificationSettingsCreate, NotificationSettings
from schemas.schemas import BusinessHoursSchema, TimeZoneUpdate



# Events
@router.post("/calendar-events/", response_model=CalendarEventSchema)
def create_calendar_event(event: CalendarEventCreate, db: Session = Depends(get_db)):
    db_event = CalendarEventModel(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/calendar-events/{event_id}", response_model=CalendarEventSchema)
def get_calendar_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(CalendarEventModel).filter(CalendarEventModel.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event



@router.get("/users/{user_id}/calendar-events", response_model=List[CalendarEventSchema])
def get_user_calendar_events(user_id: int, db: Session = Depends(get_db)):
    return db.query(CalendarEventModel).filter(CalendarEventModel.user_id == user_id).all()




@router.get("/clients/{client_id}/calendar-events", response_model=List[CalendarEventSchema])
def get_client_calendar_events(client_id: int, db: Session = Depends(get_db)):
    return db.query(CalendarEventModel).filter(CalendarEventModel.client_id == client_id).all()


@router.put("/calendar-events/{event_id}", response_model=CalendarEventSchema)
def update_calendar_event(event_id: int, event: CalendarEventUpdate, db: Session = Depends(get_db)):
    db_event = db.query(CalendarEventModel).filter(CalendarEventModel.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in event.dict().items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)
    return db_event


@router.delete("/calendar-events/{event_id}", response_model=CalendarEventSchema)
def delete_calendar_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(CalendarEventModel).filter(CalendarEventModel.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(db_event)
    db.commit()
    return db_event


# Booking Links

@router.post("/users/{user_id}/booking-links", response_model=BookingLink)
def create_booking_link(user_id: int, link_data: BookingLinkCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a unique URL
    unique_url = f"https://yourdomain.com/booking/{uuid.uuid4()}"

    # Create and store the new booking link
    new_link = BookingLinkModel(
        user_id=user_id,
        name=link_data.name,
        duration=link_data.duration,
        url=unique_url
    )
    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    return new_link






@router.get("/users/{user_id}/booking-links", response_model=List[BookingLink])
def get_user_booking_links(user_id: int, db: Session = Depends(get_db)):
    return db.query(BookingLinkModel).filter(BookingLinkModel.user_id == user_id).all()


# Notification settings

@router.get("/users/{user_id}/notification-settings", response_model=NotificationSettings)
def get_user_notification_settings(user_id: int, db: Session = Depends(get_db)):
    settings = db.query(NotificationSettingsModel).filter(NotificationSettingsModel.user_id == user_id).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Notification settings not found")
    return settings


@router.put("/users/{user_id}/notification-settings", response_model=NotificationSettings)
def update_user_notification_settings(user_id: int, settings: NotificationSettingsCreate,
                                      db: Session = Depends(get_db)):
    db_settings = db.query(NotificationSettingsModel).filter(NotificationSettingsModel.user_id == user_id).first()
    if not db_settings:
        raise HTTPException(status_code=404, detail="Settings not found")

    for key, value in settings.dict().items():
        setattr(db_settings, key, value)

    db.commit()
    db.refresh(db_settings)
    return db_settings

# Branding Settings

@router.get("/clients/{client_id}/branding-settings", response_model=BrandingSettingsSchema)
def get_client_branding_settings(client_id: int, db: Session = Depends(get_db)):
    return db.query(BrandingSettingsModel).filter(BrandingSettingsModel.client_id == client_id).first()


@router.put("/clients/{client_id}/branding-settings", response_model=BrandingSettingsSchema)
def update_client_branding_settings(client_id: int, settings: BrandingSettingsCreate, db: Session = Depends(get_db)):
    db_settings = db.query(BrandingSettingsModel).filter(BrandingSettingsModel.client_id == client_id).first()
    if not db_settings:
        raise HTTPException(status_code=404, detail="Settings not found")

    for key, value in settings.dict().items():
        setattr(db_settings, key, value)

    db.commit()
    db.refresh(db_settings)
    return db_settings

@router.get("/users/{user_id}/branding-settings")
async def get_branding_settings(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    branding_settings = db.query(BrandingSettings).filter(BrandingSettings.user_id == user_id).first()
    if not branding_settings:
        return "No branding settings found for this user"

    return branding_settings

# Booking URL

@router.get("/users/{user_id}/booking-url", response_model=str)
def get_user_booking_url(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Handle the case where booking_url is None
    if user.booking_url is None:
        return "No booking URL set for this user"

    return user.booking_url


@router.put("/users/{user_id}/booking-url", response_model=str)
def update_user_booking_url(user_id: int, update: UserBookingUrlUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.booking_url = update.booking_url
    db.commit()
    return user.booking_url


#Availability
@router.get("/get-availability")
def get_availability(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    headers = {"Authorization": f"Bearer {user.outlook_access_token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me/calendarview", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch availability")

    return response.json()


@router.get("/users/{user_id}/available-times")
async def get_available_times(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.time_zone:
        raise HTTPException(status_code=400, detail="User timezone not set")

    try:
        business_hours = db.query(BusinessHours).filter(BusinessHours.user_id == user_id).all()

        # Log the type of business_hours to ensure they are correct
        for bh in business_hours:
            logging.debug(f"BusinessHour: {bh}, Start: {bh.start_time}, End: {bh.end_time}")
            logging.debug(f"Start Type: {type(bh.start_time)}, End Type: {type(bh.end_time)}")

        available_times = fetch_user_available_times(user, business_hours, user.time_zone, db)
        return {"available_times": available_times}
    except HTTPException as e:
        logging.error(f"Error fetching available times: {str(e.detail)}")
        raise e
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch available times")





# Schedule Meeting

@router.post("/schedule-meeting")
def schedule_meeting(user_id: int, event_details: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    headers = {"Authorization": f"Bearer {user.outlook_access_token}", "Content-Type": "application/json"}
    response = requests.post("https://graph.microsoft.com/v1.0/me/events", json=event_details, headers=headers)

    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail="Failed to schedule meeting")

    return response.json()


# Business Hours

@router.get("/users/{user_id}/business-hours")
async def get_business_hours(user_id: int, db: Session = Depends(get_db)):
    business_hours = db.query(BusinessHours).filter(BusinessHours.user_id == user_id).all()

    return business_hours

@router.post("/users/{user_id}/business-hours")
async def create_or_update_business_hours(user_id: int, hours: List[BusinessHoursSchema], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for bh in hours:
        existing_bh = db.query(BusinessHours).filter(
            BusinessHours.user_id == user_id,
            BusinessHours.day_of_week == bh.day_of_week
        ).first()

        if existing_bh:
            # Update the existing record
            existing_bh.start_time = bh.start_time
            existing_bh.end_time = bh.end_time
        else:
            # Insert a new record
            new_bh = BusinessHours(user_id=user_id, **bh.dict())
            db.add(new_bh)

    db.commit()
    return user.business_hours


# Time Zone

@router.get("/users/{user_id}/time-zone")
def get_user_time_zone(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.time_zone

@router.put("/users/{user_id}/time-zone")
def update_user_time_zone(user_id: int, time_zone_update: TimeZoneUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.time_zone = time_zone_update.time_zone
    db.commit()
    return user.time_zone




# Route vistior to the correct calendar
@router.get("/booking/{uuid}", response_model=dict)
def get_booking_details(uuid: str, db: Session = Depends(get_db)):
    # Find the booking link by UUID
    booking_link = db.query(BookingLinkModel).filter(BookingLinkModel.url.endswith(uuid)).first()

    if not booking_link:
        raise HTTPException(status_code=404, detail="Booking link not found")

    # Get the user associated with this booking link
    user = db.query(User).filter(User.id == booking_link.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.time_zone:
        raise HTTPException(status_code=400, detail="User timezone not set")

    try:
        # Fetch the business hours and available times for the user
        business_hours = db.query(BusinessHours).filter(BusinessHours.user_id == user.id).all()
        available_times = fetch_user_available_times(
            user=user,
            business_hours=business_hours,
            time_zone=user.time_zone,
            db=db,
            meeting_duration_minutes=booking_link.duration  # Pass the duration here
        )

        return {
            "available_times": available_times,
            "logo_url": user.client.logo if user.client else None,
        }
    except Exception as e:
        logging.error(f"Error fetching booking details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/users/{user_id}/available-times")
async def get_available_times(user_id: int, duration: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.time_zone:
        raise HTTPException(status_code=400, detail="User timezone not set")

    try:
        business_hours = db.query(BusinessHours).filter(BusinessHours.user_id == user_id).all()
        available_times = fetch_user_available_times(user, business_hours, user.time_zone, db, duration)
        return {"available_times": available_times}
    except HTTPException as e:
        logging.error(f"Error fetching available times: {str(e.detail)}")
        raise e
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch available times")


@router.post("/bookmeeting")
async def book_meeting(event_request: EventRequest, db: Session = Depends(get_db)):
    # Extract the UUID from the event_request
    meeting_uuid = event_request.meeting_uuid

    # Find the booking link by UUID
    booking_link = db.query(BookingLinkModel).filter(BookingLinkModel.url.endswith(meeting_uuid)).first()

    if not booking_link:
        logging.debug(f"Booking link not found: {meeting_uuid}")
        raise HTTPException(status_code=404, detail="Booking link not found")

    user = db.query(User).filter(User.id == booking_link.user_id).first()

    if not user:
        logging.debug(f"User not found")
        raise HTTPException(status_code=404, detail="User not found")

    try:
        logging.debug("Refreshing access token...")
        refresh_access_token_if_needed(user, db)
    except HTTPException as e:
        logging.error(f"Token refresh failed: {str(e.detail)}")
        raise HTTPException(status_code=400, detail="Could not refresh access token")

    headers = {
        "Authorization": f"Bearer {user.outlook_access_token}",
        "Content-Type": "application/json",
    }

    event = {
        "subject": f"Meeting with {event_request.visitor_name}",
        "body": {
            "contentType": "HTML",
            "content": event_request.notes or "No additional notes."
        },
        "start": {
            "dateTime": event_request.start_datetime.isoformat(),  # Convert to ISO 8601 string
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": event_request.end_datetime.isoformat(),  # Convert to ISO 8601 string
            "timeZone": "UTC"
        },
        "location": {
            "displayName": "Teams Meeting"
        },
        "attendees": [
            {
                "emailAddress": {
                    "address": event_request.visitor_email,
                    "name": event_request.visitor_name
                },
                "type": "Required"
            }
        ],
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "teamsForBusiness",
    }

    logging.debug(f"Attempting to schedule meeting with token: {user.outlook_access_token}")
    response = requests.post(
        "https://graph.microsoft.com/v1.0/me/events",
        headers=headers,
        json=event
    )

    logging.debug(f"Microsoft Graph API response: {response.status_code} - {response.text}")

    if response.status_code == 201:
        return {"message": "Meeting scheduled successfully."}
    else:
        logging.error(f"Failed to schedule meeting: {response.status_code} - {response.json()}")
        raise HTTPException(status_code=response.status_code, detail=response.json())



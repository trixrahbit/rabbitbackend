import logging
from typing import List

import requests
from datetime import datetime, timedelta, time

from fastapi import HTTPException
from pytz import timezone
import pytz

from app.api.integrations.outlook.outlook_oauth import refresh_access_token_if_needed
from app.models.models import BusinessHours, User
from app.schemas.settings.sessions_schema import Session


def fetch_user_available_times(user: User, business_hours: List[BusinessHours], time_zone: str, db: Session, meeting_duration_minutes: int):
    # Refresh the access token if needed
    refresh_access_token_if_needed(user, db)

    headers = {"Authorization": f"Bearer {user.outlook_access_token}"}
    start_time = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    end_time = (datetime.utcnow() + timedelta(weeks=24)).isoformat() + "Z"  # Extend to 6 months (24 weeks)

    response = requests.get(
        f"https://graph.microsoft.com/v1.0/me/calendarview?startDateTime={start_time}&endDateTime={end_time}",
        headers=headers,
    )

    if response.status_code == 200:
        events = response.json().get("value", [])
        # Process and return the available times based on the events and business hours
        return calculate_available_times(events, business_hours, time_zone, meeting_duration_minutes)
    else:
        logging.error(f"Failed to fetch events from Microsoft Graph: {response.status_code} - {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch available times")


def calculate_available_times(events, business_hours, user_time_zone, meeting_duration_minutes):
    try:
        available_times = []
        user_tz = pytz.timezone(user_time_zone)

        # Start iterating from the current date
        today = datetime.now(user_tz).replace(hour=0, minute=0, second=0, microsecond=0)

        logging.info(f"User's timezone: {user_time_zone}")
        logging.info(f"Today's date in user's timezone: {today}")

        # Iterate over the next 6 months (24 weeks)
        for week_offset in range(24):
            for bh in business_hours:
                # Validate that the business hours have start_time and end_time
                if bh.start_time is None or bh.end_time is None:
                    logging.warning(f"Skipping day {bh.day_of_week} due to missing start or end time.")
                    continue

                # Calculate the next occurrence of the business day (e.g., Monday)
                current_day = today + timedelta(days=(7 * week_offset))
                while current_day.strftime('%A') != bh.day_of_week:
                    current_day += timedelta(days=1)

                # Localize the business hours to the user's timezone
                bh_start = user_tz.localize(datetime.combine(current_day.date(), bh.start_time))
                bh_end = user_tz.localize(datetime.combine(current_day.date(), bh.end_time))

                logging.info(f"Business hours for {bh.day_of_week}: Start = {bh_start}, End = {bh_end}")

                # Generate all possible slots for the day based on meeting duration
                current_slot_start = bh_start
                while current_slot_start + timedelta(minutes=meeting_duration_minutes) <= bh_end:
                    slot_end = current_slot_start + timedelta(minutes=meeting_duration_minutes)

                    # Check if this slot overlaps with any events
                    slot_is_available = True
                    for event in events:
                        # Convert event start and end times from UTC to the user's timezone
                        event_start_utc = datetime.fromisoformat(event['start']['dateTime'])
                        event_end_utc = datetime.fromisoformat(event['end']['dateTime'])

                        # Ensure these times are timezone-aware
                        if event_start_utc.tzinfo is None:
                            event_start_utc = pytz.UTC.localize(event_start_utc)
                        if event_end_utc.tzinfo is None:
                            event_end_utc = pytz.UTC.localize(event_end_utc)

                        # Convert to user's timezone
                        event_start = event_start_utc.astimezone(user_tz)
                        event_end = event_end_utc.astimezone(user_tz)

                        logging.info(f"Processing event in user's timezone: Start = {event_start}, End = {event_end}")

                        # Check for overlap with business hours
                        if current_slot_start < event_end and slot_end > event_start:
                            slot_is_available = False
                            logging.info(f"Slot from {current_slot_start} to {slot_end} overlaps with event from {event_start} to {event_end}.")
                            break

                    if slot_is_available:
                        available_times.append({
                            "start": current_slot_start.isoformat(),
                            "end": slot_end.isoformat()
                        })
                        logging.info(f"Slot added: Start = {current_slot_start}, End = {slot_end}")

                    current_slot_start = slot_end

        logging.info(f"Final available times: {available_times}")
        return available_times

    except Exception as e:
        logging.error(f"Error in calculate_available_times: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating available times: {str(e)}")









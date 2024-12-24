import logging
import requests
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, HTMLResponse

from app.api.user.user_router import get_db
from app.auth.auth_util import get_current_user
from app.models import User
from app.models.calendar.bookinglink_model import BookingLink
from app.root.root_elements import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPES, AUTHORITY
import msal

from app.schemas.calendar.bookinglink_schema import EventRequest

router = APIRouter()

# MSAL confidential client setup
msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
)

def refresh_access_token_if_needed(user: User, db: Session):
    if not user.outlook_access_token or not user.outlook_refresh_token:
        raise HTTPException(status_code=400, detail="No valid tokens available")

    try:
        # Check if the token is about to expire within the next 5 minutes
        if user.outlook_token_expires_at is None or datetime.utcnow() > user.outlook_token_expires_at - timedelta(minutes=5):
            result = msal_app.acquire_token_by_refresh_token(
                user.outlook_refresh_token,
                scopes=SCOPES
            )

            if "access_token" in result:
                user.outlook_access_token = result["access_token"]
                user.outlook_refresh_token = result.get("refresh_token", user.outlook_refresh_token)
                expires_in = result.get("expires_in", 3600)
                user.outlook_token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
                db.commit()
            else:
                logging.error(f"Failed to refresh token: {result.get('error_description', 'Unknown error')}")
                raise HTTPException(status_code=400, detail="Failed to refresh token")

    except Exception as e:
        logging.exception("An error occurred while refreshing the access token.")
        raise HTTPException(status_code=500, detail="Token refresh failed. Please try again later.")


@router.get("/connect-to-outlook")
async def connect_to_outlook(state: str):
    try:
        auth_url = msal_app.get_authorization_request_url(
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
            response_type="code",
            state=state,  # Pass the state parameter (user ID)
        )
        return {"authUrl": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate authorization URL.")


@router.get("/oauth/callback")
async def oauth_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or not state:
        raise HTTPException(status_code=400, detail="Authorization code or state not found")

    # Acquire tokens
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    if "access_token" in result:
        user_id = state
        user = db.query(User).filter(User.id == user_id).first()

        if user:
            user.outlook_access_token = result["access_token"]
            user.outlook_refresh_token = result.get("refresh_token")
            expires_in = result.get("expires_in", 3600)  # Default to 1 hour if not provided
            user.outlook_token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="User not found")

        # Return HTML that actually closes the window
        return HTMLResponse("""
            <html>
            <body>
                <script type="text/javascript">
                    window.close();
                </script>
                <p>Connected to Outlook successfully. You can close this window.</p>
            </body>
            </html>
        """)
    else:
        raise HTTPException(status_code=400, detail="Failed to acquire token")

@router.get("/logout")
async def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        current_user.outlook_access_token = None
        current_user.outlook_refresh_token = None
        current_user.outlook_token_expires_at = None
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to log out")
    return {"message": "Logged out"}

@router.get("/validate-outlook-token")
async def validate_outlook_token(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        refresh_access_token_if_needed(current_user, db)
    except HTTPException as e:
        logging.error(f"Token refresh failed: {str(e)}")
        return {"isValid": False}

    headers = {"Authorization": f"Bearer {current_user.outlook_access_token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

    if response.status_code == 200:
        return {"isValid": True}
    else:
        return {"isValid": False}





from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.checklists import checklist_router
from app.api.calendar import calendar_router
from app.api.integrations.outlook import outlook_oauth
from app.api.subscription import subscription_router
from app.api.ticketing import ticket_router
from app.api.projects import project_router
from app.api.templates import template_router
import logging

from app.api.client import client_get, client_post
from app.api.organizations import organizations_api
from app.api.profile import user_profile
from app.api.role import role_get
from app.api.settings.usercreation import create
from app.api.settings.userlogin import login
from app.api.user import user_get, user_router, user_api

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows only requests from localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers from your application modules
app.include_router(ticket_router.router)
app.include_router(user_router.router)
app.include_router(client_get.router)
app.include_router(client_post.router)
app.include_router(role_get.router)
app.include_router(create.router)
app.include_router(login.router)
app.include_router(user_get.router)
app.include_router(user_profile.router)
app.include_router(organizations_api.router)
app.include_router(project_router.router)
app.include_router(template_router.router)

app.include_router(checklist_router.router)

app.include_router(subscription_router.router)

app.include_router(calendar_router.router)

app.include_router(outlook_oauth.router)

app.include_router(user_api.router)


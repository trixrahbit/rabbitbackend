from api.contracts import contractAPI
from logger_config import logger  # Import centralized logger
# Log startup message
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from account.user import profile_api
from api.checklists import checklist_router
from api.calendar import calendar_router
from api.integrations.outlook import outlook_oauth
from api.subscription import subscription_router
from api.ticketing import ticket_router
from api.ticketing import ticketinfo_router
from api.projects import project_router
from api.templates import template_router
from api.client import client_get, contact_api, sla_api
from api.organizations import organizations_api
from api.profile import user_profile
from api.role import role_get
from api.settings.usercreation import create
from api.settings.userlogin import login
from api.user import user_get, user_api
from fastapi.responses import JSONResponse


logger.info("🚀 FastAPI app is starting...")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Allows all headers
)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"📡 Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"🔹 Response Status: {response.status_code}")
    return response
@app.options("/{full_path:path}")
async def preflight_request(full_path: str):
    """Handle CORS preflight (OPTIONS) requests manually."""
    return JSONResponse(status_code=200, headers={"Access-Control-Allow-Origin": "*",
                                                  "Access-Control-Allow-Methods": "GET, POST, PATCH, DELETE, OPTIONS",
                                                  "Access-Control-Allow-Headers": "*"})
# Include routers from your application modules
app.include_router(ticket_router.router)
app.include_router(client_get.router)

app.include_router(contractAPI.router)
app.include_router(contact_api.router)
app.include_router(ticketinfo_router.router)
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

app.include_router(profile_api.router)

app.include_router(sla_api.router)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.admin.views import FriendsAdmin, UsersAdmin
from app.database import engine
from app.friends.router import router as router_friends
from app.groups.router import router as router_groups
from app.users.router import router as router_auth
from app.chat.router import router as router_chat

app = FastAPI()
admin = Admin(app, engine)

app.include_router(router_auth)
app.include_router(router_friends)
app.include_router(router_groups)
app.include_router(router_chat)

admin.add_view(UsersAdmin)
admin.add_view(FriendsAdmin)

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin", "Authorization"],
)
"""FastAPI entry-point for the Job Application Tracker API."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import applications, emails, stats, user_auth_routes

app = FastAPI(title="Job Application Tracker API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_auth_routes.router)

app.include_router(emails.router)
app.include_router(applications.router)
app.include_router(stats.router)

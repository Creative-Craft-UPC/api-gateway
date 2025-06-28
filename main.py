from fastapi import FastAPI
from routers import education_routes, profile_education_routes, profile_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Gateway API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O usa el dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(profile_education_routes.router, prefix="/gateway/profile-educatiton", tags=["Profile_education"])
app.include_router(profile_routes.router, prefix="/gateway/profile", tags=["Profile"])
app.include_router(education_routes.router, prefix="/gateway/education",tags=["Education"])

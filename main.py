from fastapi import FastAPI
from routers import education_routes, profile_education_routes, profile_routes

app = FastAPI(title="Gateway API")

app.include_router(profile_education_routes.router, prefix="/gateway/profile-educatiton", tags=["Profile_education"])
app.include_router(profile_routes.router, prefix="/gateway/profile", tags=["Profile"])
app.include_router(education_routes.router, prefix="/gateway/education",tags=["Education"])

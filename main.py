from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from routers import education_routes, profile_education_routes, profile_routes, progress_routes
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials

load_dotenv()


    # Lee la ruta del JSON de Firebase montado como secreto
firebase_sa_path = os.getenv("FIREBASE_SA_PATH", "secrets/socialfun-upc-firebase-adminsdk-fbsvc-d0d5b4e65c.json")
cred = credentials.Certificate(firebase_sa_path)
print(cred)
firebase_admin.initialize_app(cred)

app = FastAPI(title="Gateway API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O usa el dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(profile_education_routes.router, prefix="/gateway/profile-education", tags=["Profile_education"])
app.include_router(profile_routes.router, prefix="/gateway/profile", tags=["Profile"])
app.include_router(education_routes.router, prefix="/gateway/education",tags=["Education"])
app.include_router(progress_routes.router, prefix="/gateway/progress", tags=["Progress"])
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Middleware
# Adjust origins as needed for your frontend deployment
# origins = [
#     "http://localhost:3000", # Example for local React dev server
#     "http://localhost:5173", # Example for local Vite dev server
#     "https://your-frontend-domain.vercel.app", # Example for Vercel deployment
# ]
# For development, allow all origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

# Import the main v1 router
from app.api.v1 import api_router as api_v1_router # Ensure this alias is used if it was intended

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"} 
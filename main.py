
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routers import fish_counting, weight_prediction, food_prediction, disease_detection, summary_report


app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple token-based auth
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Replace with your token validation logic
    if token != "mysecrettoken":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
    return True


# Protect all routes
app.include_router(fish_counting.router, dependencies=[Depends(verify_token)])
app.include_router(weight_prediction.router, dependencies=[Depends(verify_token)])
app.include_router(food_prediction.router, dependencies=[Depends(verify_token)])
app.include_router(disease_detection.router, dependencies=[Depends(verify_token)])
app.include_router(summary_report.router, dependencies=[Depends(verify_token)])

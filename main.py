
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

# Protect all routes
# app.include_router(fish_counting.router, dependencies=[Depends(verify_token)])
app.include_router(weight_prediction.router)
# app.include_router(food_prediction.router, dependencies=[Depends(verify_token)])
# app.include_router(disease_detection.router, dependencies=[Depends(verify_token)])
# app.include_router(summary_report.router, dependencies=[Depends(verify_token)])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
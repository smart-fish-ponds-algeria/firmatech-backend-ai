
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routers import fish_counting, fish_farm_routes, weight_prediction, food_prediction, disease_detection


app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fish_counting.router)
app.include_router(weight_prediction.router)
# app.include_router(food_prediction.router, dependencies=[Depends(verify_token)])
app.include_router(disease_detection.router)
app.include_router(fish_farm_routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
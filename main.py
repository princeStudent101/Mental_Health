from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware


BASE_DIR = Path(__file__).resolve().parent
model = joblib.load(BASE_DIR / "Mental_Health_Model.pkl")
app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

COUNTRY_GROUPS = [
    "Other",
    "India",
    "USA",
    "Canada",
    "Australia",
    "UK",
    "Germany",
    "Mexico",
    "Turkey",
    "France",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)




class StudentData(BaseModel):
    age: int = Field(...,ge=10 , le = 100)
    gender: str = Literal["Male","Female"]
    country: str = Field(alias="Country")
    academic_level: str = Literal["High School" , "Undergraduate", "Graduate"]
    most_used_platform: str = Literal["Facebook", "Instagram", "Twitter", "Snapchat", "TikTok", "YouTube", "Reddit", "Other"]
    purpose_of_use: str = Literal["Networking", "Entertainment", "News"]
    avg_daily_usage_hours: float = Field(...,ge = 2 , le = 24)
    daily_unlocks: float = Field(..., ge = 1 , le = 100)
    study_hours: float = Field(..., ge = 4 , le = 24)
    physical_activity_hours: float = Field(..., ge = 2)
    sleep_hours_per_night: float = Field(..., ge = 6 , le = 10)
    stress_level: str | float = Literal["Low","Medium","High","Very High"]


class PredictionResponse(BaseModel):
    predict_mental_health_score : float
    


@app.get("/")
def read_root():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.post("/predict",response_model=PredictionResponse)
def predict(data: StudentData):
    group_country = data.country if data.country in COUNTRY_GROUPS else "Other"
    feature_row = pd.DataFrame([{
          
        "Study_Hours": data.study_hours,
        "Age": data.age,
        "Avg_Daily_Usage_Hours": data.avg_daily_usage_hours,
        "Sleep_Hours_Per_Night": data.sleep_hours_per_night,
        "Physical_Activity_Hours": data.physical_activity_hours,
        "Daily_Unlocks": data.daily_unlocks,
        "Stress_Level": data.stress_level,
        "Gender": data.gender,
        "Academic_Level": data.academic_level,
        "Most_Used_Platform": data.most_used_platform,
        "Purpose_Of_Use": data.purpose_of_use,
        "group_country": group_country
}])
      
    prediction = model.predict(feature_row)[0]
    return PredictionResponse(predict_mental_health_score = round(float(prediction),2))
    

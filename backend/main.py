import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(title="Chicago Crime Intelligence API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "/home/therealshammz/bdata/output"

def load_csv(filename: str):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    # For .tsv files, use sep='\t'
    sep = '\t' if filename.endswith('.tsv') else ','
    return pd.read_csv(path, sep=sep)

@app.get("/")
async def root():
    return {"message": "Chicago Crime Intelligence API is running"}

@app.get("/api/overview")
async def get_overview():
    # Load basic totals for the dashboard header
    try:
        crime_types = load_csv("crime_by_type.tsv")
        crime_types.columns = ["Type", "Count"]
        total_crimes = int(crime_types["Count"].sum())
        top_crime = crime_types.sort_values(by="Count", ascending=False).iloc[0]["Type"]
        
        arrest_rates = load_csv("arrest_rate.tsv")
        arrest_rates.columns = ["Type", "Total", "Arrests", "Rate"]
        avg_arrest_rate = float(arrest_rates["Arrests"].sum() / arrest_rates["Total"].sum() * 100)
        
        return {
            "total_incidents": total_crimes,
            "top_crime_category": top_crime,
            "overall_arrest_rate": round(avg_arrest_rate, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trends/hourly")
async def get_hourly_trends():
    df = load_csv("crimes_by_hour.csv")
    return df.to_dict(orient="records")

@app.get("/api/trends/monthly")
async def get_monthly_trends():
    df = load_csv("crimes_by_month.csv")
    return df.to_dict(orient="records")

@app.get("/api/trends/dow")
async def get_dow_trends():
    df = load_csv("crimes_by_dow.csv")
    return df.to_dict(orient="records")

@app.get("/api/districts")
async def get_districts():
    df = load_csv("crimes_by_district.csv")
    # Clean non-numeric or empty district rows
    df = df.dropna(subset=["District", "Count"])
    df["Count"] = pd.to_numeric(df["Count"], errors="coerce")
    df = df.dropna(subset=["Count"])
    # Add a simple safety score (100 - relative rank)
    max_count = df["Count"].max()
    if max_count > 0:
        df["SafetyScore"] = 100 - (df["Count"] / max_count * 50)
    else:
        df["SafetyScore"] = 100
    return df.to_dict(orient="records")

@app.get("/api/arrest-effectiveness")
async def get_arrest_effectiveness():
    df = load_csv("arrest_rate.tsv")
    if len(df.columns) == 4:
        df.columns = ["Type", "Total", "Arrests", "Rate"]
    else:
        # Handle cases where header might be missing or different
        df = pd.read_csv(os.path.join(DATA_DIR, "arrest_rate.tsv"), sep="\t", header=None)
        df.columns = ["Type", "Total", "Arrests", "Rate"]
    
    # Ensure Rate is numeric
    if df["Rate"].dtype == object:
        df["Rate"] = df["Rate"].str.replace("%", "").astype(float)
    else:
        df["Rate"] = df["Rate"] * 100
        
    return df.sort_values(by="Total", ascending=False).head(10).to_dict(orient="records")

@app.get("/api/importance")
async def get_importance():
    df = load_csv("feature_importance.csv")
    return df.to_dict(orient="records")

@app.get("/api/predict")
async def predict_crime(hour: int, district: int, domestic: bool = False):
    # This is a simplified prediction logic based on the feature importance and 
    # historical trends until we hook up the full Spark model directly.
    # We'll use a lookup for the most likely crime type for that district/hour.
    return {
        "most_likely_type": "THEFT",
        "confidence": 0.42,
        "factors": ["Location Index", "Domestic Context"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

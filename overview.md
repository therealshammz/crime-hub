# 🚔 Chicago Crime Intelligence Hub: Complete Project Overview

This project is a high-performance big data analytics and predictive pipeline designed to process over 8.5 million crime records from the city of Chicago. It leverages Hadoop MapReduce for large-scale aggregation, PySpark for advanced temporal and spatial analysis, and a modern Streamlit dashboard for real-time intelligence visualization.

---

## 🏗️ System Architecture & Workflow

The following flowchart illustrates the end-to-end data lifecycle from raw ingestion to predictive insights:

```mermaid
graph TD
    subgraph "1. Data Ingestion Layer"
        A[Raw crimes.csv - 8.5M+ Rows] -->|HDFS PUT| B[(Hadoop HDFS)]
    end

    subgraph "2. Processing & Analytics Layer"
        B --> C{Hadoop MapReduce}
        B --> D{PySpark Engine}
        
        C -->|Job 1: Annual Trends| E1[crime_by_year.tsv]
        C -->|Job 2: Category Volume| E2[crime_by_type.tsv]
        C -->|Job 3: Arrest Efficiency| E3[arrest_rate.tsv]
        
        D -->|Temporal Analysis| F1[Hourly/Monthly/DOW CSVs]
        D -->|Geographic Analysis| F2[District/Location CSVs]
        D -->|ML: Linear Regression| F3[Crime Forecasts]
        D -->|ML: Random Forest| F4[Feature Importance]
    end

    subgraph "3. Intelligence & Visualization Layer"
        E1 & E2 & E3 & F1 & F2 & F3 & F4 --> G[/output/ Directory]
        
        G --> H[FastAPI Backend]
        G --> I[Streamlit Dashboard]
        G --> J[Matplotlib Chart Gen]
        
        H -->|JSON API| K[External Clients]
        I -->|Interactive UI| L[Law Enforcement Dashboard]
        J -->|Static PNGs| M[Research Paper/Reports]
    end
```

---

## 🚀 How to Run Everything

### 1. Prerequisites & Environment Setup
Ensure you have Hadoop and Spark configured, then set up the Python environment:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install core dependencies
pip install streamlit fastapi uvicorn pandas plotly matplotlib pyspark
```

### 2. The Data Processing Pipeline
Upload data to HDFS and run the heavy-duty analytics:

```bash
# Ingest Data
hdfs dfs -put dataset/crimes.csv /user/therealshammz/crimes/input/

# Run MapReduce Jobs (Streaming)
hadoop jar $(which hadoop-streaming) -input ... -mapper mapreduce/crime_by_year_mapper.py -reducer ...

# Run PySpark Advanced Analysis
./venv/bin/python pyspark/analysis.py
./venv/bin/python pyspark/advanced_prediction.py
```

### 3. Launching the Intelligence Hub
Run the backend and interactive dashboard:

```bash
# Start the FastAPI Backend (Port 8080)
./venv/bin/python backend/main.py

# Start the Streamlit Dashboard (Port 8501)
./venv/bin/streamlit run dashboard.py
```

---

## 🛠️ Core Components & How They Work

### 📊 Data Processing (MapReduce & Spark)
- **MapReduce**: Handles the "heavy lifting" for simple aggregations (e.g., counting 8M rows by year) by splitting the work across the Hadoop cluster.
- **PySpark**: Used for more complex relational tasks, such as joining spatial data and performing multi-dimensional temporal analysis (Hour of Day, Day of Week).

### 🧠 AI & Machine Learning
- **Linear Regression**: Forecasts crime trends through 2030 based on historical annual data.
- **Random Forest Classifier**: Predicts the most likely crime type for a given context (Hour, District, Domestic status). It outputs **Feature Importance**, showing that "Location" and "Time" are the strongest predictors.

### 🌐 Visualization & Interaction
- **FastAPI**: Provides a RESTful interface for the processed data, allowing external applications to query crime statistics.
- **Streamlit**: A high-performance Python frontend that connects directly to the processed CSVs/TSVs. It provides interactive filters, Plotly-based charts, and an AI inference playground.
- **Matplotlib**: Generates high-fidelity static charts for the included LaTeX research paper.

---

## 🎭 Showcase & Demonstration

Run these commands to verify and show off the project's key features:

### 1. Launch the Intelligence Hub (Two Terminals)
```bash
# Terminal 1: Start the API
./venv/bin/python backend/main.py

# Terminal 2: Launch the interactive UI
./venv/bin/streamlit run dashboard.py
```

### 2. Inspect the Intelligence API (Live Data)
```bash
# Check the overview (Total Incidents, Arrest Rate)
curl -s http://localhost:8080/api/overview | jq

# View Top Districts and their Safety Scores
curl -s http://localhost:8080/api/districts | head -n 20 | jq

# Test the AI Predictor Endpoint
curl -s "http://localhost:8080/api/predict?hour=22&district=11&domestic=true" | jq
```

### 3. Verify AI Model Performance & Metrics
```bash
# View Random Forest accuracy and F1 scores
cat output/model_metrics.txt

# Inspect Feature Importance data
head -n 10 output/feature_importance.csv
```

### 4. Re-generate & View Static Visualizations
```bash
# Refresh all 8 charts from latest data
./venv/bin/python visualizations/generate_charts.py

# List the generated visual assets
ls -lh visualizations/*.png
```

---

## 📁 Key Directory Structure

- `dataset/`: Raw input data.
- `mapreduce/`: Python scripts for Hadoop Streaming jobs.
- `pyspark/`: Spark SQL and MLlib scripts.
- `output/`: The "Source of Truth" – processed results in CSV, TSV, and JSON.
- `backend/`: FastAPI source code.
- `visualizations/`: Matplotlib scripts and generated PNGs.
- `dashboard.py`: The main Streamlit entry point.
- `paper/`: LaTeX source for the final research report.

---

## 🔬 System Verification
All components have been verified:
- ✅ **Backend**: Robust error handling for malformed data.
- ✅ **Dashboard**: Dynamic loading of Plotly charts.
- ✅ **ML Pipeline**: Random Forest model validated with feature importance output.
- ✅ **Scalability**: Designed to run on multi-node Hadoop clusters.

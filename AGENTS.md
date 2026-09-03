# Chicago Crime Intelligence Hub - Agent Guidance

## Repository Purpose
Big data analytics platform for Chicago crime data (8.5M+ records) using Hadoop MapReduce, PySpark, and Streamlit dashboard.

## Quick Start Commands

### Environment Setup
```bash
source venv/bin/activate  # Virtual env already configured with all deps
```

### Data Pipeline (Full Run)
```bash
# 1. Upload data to HDFS
hdfs dfs -mkdir -p /user/therealshammz/crimes/input
hdfs dfs -put dataset/crimes.csv /user/therealshammz/crimes/input/

# 2. Run MapReduce jobs (Hadoop Streaming)
hadoop jar $(which hadoop-streaming) -input /user/therealshammz/crimes/input/crimes.csv \
  -output /user/therealshammz/crimes/output/crime_by_year \
  -mapper mapreduce/crime_by_year_mapper.py -reducer mapreduce/crime_by_year_reducer.py

# 3. Retrieve outputs
hdfs dfs -get /user/therealshammz/crimes/output/crime_by_year/part-00000 output/crime_by_year.tsv
```

### PySpark Analysis
```bash
python pyspark/analysis.py           # 6 aggregations (hour, month, DOW, location, district, domestic)
python pyspark/predict_crime.py      # Linear regression forecast through 2030
python pyspark/advanced_prediction.py # Random Forest crime type classifier
```

### Visualizations & Dashboard
```bash
python visualizations/generate_charts.py  # Generates 8 PNG charts
python backend/main.py                    # FastAPI backend (Port 8080)
streamlit run dashboard.py                # Streamlit dashboard (Port 8501)
```

## Critical Gotchas

### Output Directory Conflicts
Hadoop/Spark jobs **fail** if output directories exist. Always clean first:
```bash
rm -f output/*.csv output/*.tsv output/*.json output/*.txt
rm -f visualizations/*.png
hdfs dfs -rm -r /user/therealshammz/crimes/output
```

### Java Versions
- **Java 11** required for Hadoop
- **Java 17** required for Spark
- `JAVA_HOME` is set in `pyspark/analysis.py` and `pyspark/advanced_prediction.py`

### Data Paths
- HDFS input: `hdfs://127.0.0.1:9000/user/therealshammz/crimes/input/crimes.csv`
- Local output: `~/bdata/output/` (hardcoded in pyspark scripts)
- CSV column indices: Year=17, Primary Type=5, Arrest=8

## Project Structure
```
bdata/
├── backend/main.py          # FastAPI REST API (Port 8080)
├── dashboard.py             # Streamlit UI (Port 8501)
├── mapreduce/               # Hadoop Streaming jobs
│   ├── crime_by_year_*.py   # Annual crime counts
│   ├── crime_by_type_*.py   # Crime type frequencies
│   └── arrest_rate_*.py     # Arrest rates by type
├── pyspark/                 # Spark SQL & ML
│   ├── analysis.py          # 6 aggregations
│   ├── predict_crime.py     # Linear regression forecast
│   └── advanced_prediction.py # Random Forest classifier
├── visualizations/          # Chart generation
├── output/                  # Generated CSV/TSV files
├── paper/                   # LaTeX research paper
└── dataset/crimes.csv       # Raw data (8.5M records, 2.3GB)
```

## API Endpoints (FastAPI on Port 8080)
| Endpoint | Description |
|----------|-------------|
| `GET /` | Health check |
| `GET /api/overview` | Total incidents, top crime, arrest rate |
| `GET /api/trends/hourly` | Crimes by hour (0-23) |
| `GET /api/trends/monthly` | Crimes by month (1-12) |
| `GET /api/districts` | Crime stats by police district |
| `GET /api/arrest-effectiveness` | Arrest rates by crime type |
| `GET /api/predict?hour=12&district=11&domestic=false` | AI prediction |

## Testing & Verification
```bash
# Check API is running
curl -s http://localhost:8080/api/overview | jq

# View model metrics
cat output/model_metrics.txt

# Check feature importance
head output/feature_importance.csv
```

## Paper Compilation
```bash
cd paper && pdflatex chicago_crime_analysis.tex  # Run twice for references
```

## Dependencies (requirements.txt)
streamlit, fastapi, uvicorn, pandas, plotly, matplotlib, pyspark, scikit-learn, numpy
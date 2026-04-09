# Chicago Crime Hub

Big data analytics platform for Chicago crime data (8.5M+ records) using Hadoop MapReduce, PySpark, and a Streamlit dashboard.

## Features

- **Hadoop MapReduce** - Large-scale aggregation jobs for crime statistics
- **PySpark ML** - Crime prediction and forecasting with Random Forest and Linear Regression
- **FastAPI Backend** - REST API for crime intelligence data
- **Streamlit Dashboard** - Interactive visualization with Plotly charts

## Quick Start

### Prerequisites

- Python 3.10+
- Hadoop 3.x (for MapReduce jobs)
- Apache Spark 3.x (for PySpark analysis)

### Installation

```bash
# Clone and setup
git clone https://github.com/therealshammz/crime-hub.git
cd crime-hub
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Data Processing

```bash
# Upload data to HDFS
hdfs dfs -put dataset/crimes.csv /user/hadoop/crimes/input/

# Run MapReduce jobs
hadoop jar $(hadoop classpath | grep streaming) -input /user/hadoop/crimes/input/crimes.csv \
  -output /user/hadoop/crimes/output/by_year \
  -mapper mapreduce/crime_by_year_mapper.py \
  -reducer mapreduce/crime_by_year_reducer.py

# Run PySpark analysis
python pyspark/analysis.py
python pyspark/predict_crime.py
```

### Launch Dashboard

```bash
# Start FastAPI backend
python backend/main.py

# Start Streamlit dashboard (new terminal)
streamlit run dashboard.py
```

## Project Structure

```
crime-hub/
├── backend/          # FastAPI REST API
├── mapreduce/        # Hadoop Streaming jobs
├── pyspark/          # Spark SQL & MLlib analysis
├── output/           # Processed data (generated)
├── visualizations/   # Matplotlib charts (generated)
├── paper/            # LaTeX research paper
├── dataset/          # Raw data (not included)
├── dashboard.py      # Streamlit UI
└── requirements.txt  # Python dependencies
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/overview` | Total incidents, top crime, arrest rate |
| `GET /api/trends/hourly` | Crimes by hour of day |
| `GET /api/trends/monthly` | Crimes by month |
| `GET /api/districts` | Crime stats by district with safety scores |
| `GET /api/arrest-effectiveness` | Arrest rates by crime type |
| `GET /api/predict?hour=12&district=11&domestic=false` | AI crime prediction |

## Dataset

Source: [City of Chicago Data Portal - Crimes](https://data.cityofchicago.org/Public-Safety/Crimes/6zsd-86xi)

This project processes crime data from 2001 to present, updated regularly by the City of Chicago.

## License

MIT License - see [LICENSE](LICENSE) for details.

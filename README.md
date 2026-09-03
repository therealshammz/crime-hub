# Chicago Crime Intelligence Hub

[![CI/CD](https://github.com/therealshammz/crime-hub/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/therealshammz/crime-hub/actions/workflows/ci-cd.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)

Big data analytics platform for Chicago crime data (8.5M+ records) using Hadoop MapReduce, PySpark, and a Streamlit dashboard.

## Features

- **Hadoop MapReduce** - Large-scale aggregation jobs for crime statistics
- **PySpark ML** - Crime prediction and forecasting with Random Forest and Linear Regression
- **FastAPI Backend** - REST API for crime intelligence data
- **Streamlit Dashboard** - Interactive visualization with Plotly charts

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Data Pipeline](#data-pipeline)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Docker](#docker)
- [Dataset](#dataset)
- [License](#license)

## Prerequisites

- Python 3.10+
- Java 11 (for Hadoop) and Java 17 (for Spark)
- Hadoop 3.x (for MapReduce jobs)
- Apache Spark 3.x (for PySpark analysis)

## Installation

### Local Setup

```bash
# Clone the repository
git clone https://github.com/therealshammz/crime-hub.git
cd crime-hub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Using Makefile

```bash
# Setup environment
make setup

# Or use Docker
make docker-setup
```

## Quick Start

### 1. Download Data

```bash
# Download crime data from Chicago Data Portal
python scripts/download_data.py

# Or with a limit for testing
python scripts/download_data.py --limit 10000
```

### 2. Run Data Pipeline

```bash
# Using Makefile
make run-mapreduce  # Run MapReduce jobs
make run-spark      # Run PySpark analysis

# Or manually
hdfs dfs -put dataset/crimes.csv /user/therealshammz/crimes/input/
python pyspark/analysis.py
python pyspark/predict_crime.py
```

### 3. Launch Services

```bash
# Terminal 1: Start FastAPI backend (Port 8080)
make run-api

# Terminal 2: Start Streamlit dashboard (Port 8501)
make run-dashboard
```

## Data Pipeline

### Step 0: Cleanup (Important!)

Hadoop/Spark jobs **fail** if output directories exist. Always clean first:

```bash
make clean-all
```

### Step 1: Data Ingestion

```bash
# Upload data to HDFS
hdfs dfs -mkdir -p /user/therealshammz/crimes/input
hdfs dfs -put dataset/crimes.csv /user/therealshammz/crimes/input/
```

### Step 2: MapReduce Jobs

```bash
# Crime by Year
hadoop jar $(which hadoop-streaming) \
  -input /user/therealshammz/crimes/input/crimes.csv \
  -output /user/therealshammz/crimes/output/crime_by_year \
  -mapper mapreduce/crime_by_year_mapper.py \
  -reducer mapreduce/crime_by_year_reducer.py

# Crime by Type
hadoop jar $(which hadoop-streaming) \
  -input /user/therealshammz/crimes/input/crimes.csv \
  -output /user/therealshammz/crimes/output/crime_by_type \
  -mapper mapreduce/crime_by_type_mapper.py \
  -reducer mapreduce/crime_by_type_reducer.py

# Arrest Rate
hadoop jar $(which hadoop-streaming) \
  -input /user/therealshammz/crimes/input/crimes.csv \
  -output /user/therealshammz/crimes/output/arrest_rate \
  -mapper mapreduce/arrest_rate_mapper.py \
  -reducer mapreduce/arrest_rate_reducer.py
```

### Step 3: PySpark Analysis

```bash
# Temporal & Geographic Analysis
python pyspark/analysis.py

# Crime Forecasting (Linear Regression)
python pyspark/predict_crime.py

# Crime Type Classifier (Random Forest)
python pyspark/advanced_prediction.py
```

### Step 4: Generate Visualizations

```bash
python visualizations/generate_charts.py
```

## API Endpoints

FastAPI backend runs on port 8080 by default.

| Endpoint | Description |
|----------|-------------|
| `GET /` | Health check |
| `GET /api/overview` | Total incidents, top crime, arrest rate |
| `GET /api/trends/hourly` | Crimes by hour (0-23) |
| `GET /api/trends/monthly` | Crimes by month (1-12) |
| `GET /api/districts` | Crime stats by police district |
| `GET /api/arrest-effectiveness` | Arrest rates by crime type |
| `GET /api/predict?hour=12&district=11&domestic=false` | AI prediction |

### API Examples

```bash
# Check API health
curl -s http://localhost:8080/ | jq

# Get overview
curl -s http://localhost:8080/api/overview | jq

# Get hourly trends
curl -s http://localhost:8080/api/trends/hourly | jq

# Test AI predictor
curl -s "http://localhost:8080/api/predict?hour=22&district=11&domestic=true" | jq
```

## Project Structure

```
bdata/
├── backend/              # FastAPI REST API
│   └── main.py           # API server (Port 8080)
├── dashboard.py          # Streamlit UI (Port 8501)
├── mapreduce/            # Hadoop Streaming jobs
│   ├── crime_by_year_*.py # Annual crime counts
│   ├── crime_by_type_*.py # Crime type frequencies
│   └── arrest_rate_*.py   # Arrest rates by type
├── pyspark/              # Spark SQL & ML
│   ├── analysis.py       # 6 aggregations
│   ├── predict_crime.py  # Linear regression forecast
│   └── advanced_prediction.py # Random Forest classifier
├── visualizations/       # Chart generation
│   └── generate_charts.py
├── output/               # Processed data (generated)
├── paper/                # LaTeX research paper
├── dataset/              # Raw data
├── scripts/              # Utility scripts
│   └── download_data.py  # Data download script
├── tests/                # Unit tests
├── .github/workflows/    # CI/CD workflows
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose
├── Makefile              # Build automation
├── pyproject.toml        # Project configuration
├── requirements.txt      # Python dependencies
├── AGENTS.md             # Agent guidance
└── README.md             # This file
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run pre-commit hooks
pre-commit install

# Run linting
make lint
```

### Available Make Commands

```bash
make help           # Show all available commands
make setup          # Create virtual environment and install dependencies
make run-api        # Start FastAPI backend (Port 8080)
make run-dashboard  # Start Streamlit dashboard (Port 8501)
make run-spark      # Run PySpark analysis
make generate-charts # Generate visualization charts
make compile-paper  # Compile LaTeX research paper
make clean          # Clean local output files
make clean-hdfs     # Clean HDFS output directory
make clean-all      # Clean all outputs
make verify         # Verify API and outputs
make test           # Run tests
```

## Testing

```bash
# Run tests
make test

# Or with pytest directly
python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

## Docker

### Build and Run with Docker

```bash
# Build the image
docker build -t crime-hub:latest .

# Run with docker-compose
docker-compose up -d

# Stop services
docker-compose down
```

## Dataset

**Source:** [City of Chicago Data Portal - Crimes](https://data.cityofchicago.org/Public-Safety/Crimes/6zsd-86xi)

This project processes crime data from 2001 to present, updated regularly by the City of Chicago.

### Data Columns

- **Year** (Column 17) - Incident year
- **Primary Type** (Column 5) - Crime category
- **Arrest** (Column 8) - Whether arrest was made
- **Date** - Timestamp of incident
- **Location Description** - Physical location
- **District** - Police district number
- **Domestic** - Whether domestic incident

## License

MIT License - see [LICENSE](LICENSE) for details.
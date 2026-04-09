# Chicago Crime Analysis - Command Reference

A big data analytics pipeline for Chicago crime data (8.5M+ records) using Hadoop MapReduce, PySpark, and Python visualizations.

---

## Prerequisites

Ensure the following are running before executing commands:
- Hadoop HDFS (NameNode, DataNode)
- Hadoop YARN (ResourceManager, NodeManager)
- Java 11 (for Hadoop) and Java 17 (for Spark)

---

## 1. Data Ingestion

Upload the raw crime dataset to HDFS:

```bash
hdfs dfs -mkdir -p /user/therealshammz/crimes/input
hdfs dfs -put dataset/crimes.csv /user/therealshammz/crimes/input/
```

---

## 2. MapReduce Jobs

### Job 1: Crime Count by Year

Counts total crimes for each year (2001-2026).

```bash
hadoop jar $(which hadoop-streaming) \
  -input /user/therealshammz/crimes/input/crimes.csv \
  -output /user/therealshammz/crimes/output/crime_by_year \
  -mapper mapreduce/crime_by_year_mapper.py \
  -reducer mapreduce/crime_by_year_reducer.py
```

**Output:** Year-wise crime totals

---

### Job 2: Crime Count by Type

Counts crimes grouped by primary type (34 categories).

```bash
hadoop jar $(which hadoop-streaming) \
  -input /user/therealshammz/crimes/input/crimes.csv \
  -output /user/therealshammz/crimes/output/crime_by_type \
  -mapper mapreduce/crime_by_type_mapper.py \
  -reducer mapreduce/crime_by_type_reducer.py
```

**Output:** Crime type frequencies (e.g., Theft, Battery, Assault)

---

### Job 3: Arrest Rate by Crime Type

Computes arrest rate percentage for each crime type.

```bash
hadoop jar $(which hadoop-streaming) \
  -input /user/therealshammz/crimes/input/crimes.csv \
  -output /user/therealshammz/crimes/output/arrest_rate \
  -mapper mapreduce/arrest_rate_mapper.py \
  -reducer mapreduce/arrest_rate_reducer.py
```

**Output:** Per-type statistics: total incidents, arrests, arrest rate %

---

### Retrieve MapReduce Outputs

```bash
hdfs dfs -get /user/therealshammz/crimes/output/crime_by_year/part-00000 output/crime_by_year.tsv
hdfs dfs -get /user/therealshammz/crimes/output/crime_by_type/part-00000 output/crime_by_type.tsv
hdfs dfs -get /user/therealshammz/crimes/output/arrest_rate/part-00000 output/arrest_rate.tsv
```

---

## 3. PySpark Analyses

Run temporal, geographic, and categorical analyses using Spark.

```bash
python pyspark/analysis.py
```

**Outputs (CSV files in `output/`):**
| File | Description |
|------|-------------|
| `crimes_by_hour.csv` | Crime count by hour (0-23) |
| `crimes_by_month.csv` | Crime count by month (1-12) |
| `crimes_by_dow.csv` | Crime count by day of week (1=Sun, 7=Sat) |
| `crimes_by_location.csv` | Crime count by location type |
| `crimes_by_district.csv` | Crime count by police district |
| `domestic_vs_nondomestic.csv` | Domestic vs non-domestic split |

**Requires:** HDFS data at `hdfs://127.0.0.1:9000/user/therealshammz/crimes/input/crimes.csv`

---

## 4. Predictive Modeling

### Baseline Forecast (Linear Regression)
Train linear regression model and forecast crimes through 2030.
```bash
python pyspark/predict_crime.py
```

### Advanced Crime Type Classifier (Random Forest)
Uses Spark MLlib to predict the most likely crime type based on context.
```bash
./venv/bin/python pyspark/advanced_prediction.py
```

**Outputs:**
- `output/feature_importance.csv` - Key predictors of crime types
- `output/model_metrics.txt` - Accuracy and F1-score
- `visualizations/feature_importance.png` - Visual importance scores

---

## 5. Generate Visualizations

Create all charts from analysis outputs.

```bash
python visualizations/generate_charts.py
```

**Outputs (PNG files in `visualizations/`):**
| File | Description |
|------|-------------|
| `crime_by_year.png` | Annual crime trend (2001-2026) |
| `crime_by_type.png` | Top 15 crime types bar chart |
| `arrest_rate.png` | Arrest rate by crime type |
| `crimes_by_hour.png` | Hourly distribution bar chart |
| `crimes_by_month.png` | Monthly distribution bar chart |
| `crimes_by_dow.png` | Day-of-week distribution |
| `domestic_pie.png` | Domestic vs non-domestic pie chart |
| `crime_forecast.png` | Linear regression forecast chart |

---

## 6. Compile Research Paper
e
Build the LaTeX paper (requires `pdflatex`).

```bash
cd paper
pdflatex chicago_crime_analysis.tex
pdflatex chicago_crime_analysis.tex  # Run twice for references
```

**Output:** `paper/chicago_crime_analysis.pdf`

---

## Alternative: Standalone MRJob Execution

The `mapreduce/*.py` files can also be run directly using MRJob:

```bash
# Crime by Year
python mapreduce/crime_by_year.py dataset/crimes.csv > output/crime_by_year.json

# Crime by Type
python mapreduce/crime_by_type.py dataset/crimes.csv > output/crime_by_type.json

# Arrest Rate
python mapreduce/arrest_rate.py dataset/crimes.csv > output/arrest_rate.json
```

---

## Project Structure

```
bdata/
├── dataset/
│   └── crimes.csv              # Raw input data (8.5M records)
├── mapreduce/
│   ├── crime_by_year.py        # MRJob version
│   ├── crime_by_year_mapper.py # Streaming mapper
│   ├── crime_by_year_reducer.py# Streaming reducer
│   ├── crime_by_type.py        # MRJob version
│   ├── crime_by_type_mapper.py # Streaming mapper
│   ├── crime_by_type_reducer.py# Streaming reducer
│   ├── arrest_rate.py          # MRJob version
│   ├── arrest_rate_mapper.py   # Streaming mapper
│   └── arrest_rate_reducer.py  # Streaming reducer
├── pyspark/
│   ├── analysis.py             # 6 PySpark aggregations
│   └── predict_crime.py        # Linear regression forecast
├── visualizations/
│   └── generate_charts.py      # Chart generation script
├── output/                     # CSV/TSV/JSON outputs
├── paper/                      # LaTeX research paper
└── COMMANDS.md                 # This file
```

---

## Quick Start (Full Pipeline)

```bash
# 1. Upload data to HDFS
hdfs dfs -mkdir -p /user/therealshammz/crimes/input
hdfs dfs -put dataset/crimes.csv /user/therealshammz/crimes/input/

# 2. Run MapReduce jobs
hadoop jar $(which hadoop-streaming) -input /user/therealshammz/crimes/input/crimes.csv -output /user/therealshammz/crimes/output/crime_by_year -mapper mapreduce/crime_by_year_mapper.py -reducer mapreduce/crime_by_year_reducer.py
hadoop jar $(which hadoop-streaming) -input /user/therealshammz/crimes/input/crimes.csv -output /user/therealshammz/crimes/output/crime_by_type -mapper mapreduce/crime_by_type_mapper.py -reducer mapreduce/crime_by_type_reducer.py
hadoop jar $(which hadoop-streaming) -input /user/therealshammz/crimes/input/crimes.csv -output /user/therealshammz/crimes/output/arrest_rate -mapper mapreduce/arrest_rate_mapper.py -reducer mapreduce/arrest_rate_reducer.py

# 3. Retrieve outputs
hdfs dfs -get /user/therealshammz/crimes/output/crime_by_year/part-00000 output/crime_by_year.tsv
hdfs dfs -get /user/therealshammz/crimes/output/crime_by_type/part-00000 output/crime_by_type.tsv
hdfs dfs -get /user/therealshammz/crimes/output/arrest_rate/part-00000 output/arrest_rate.tsv

# 4. Run PySpark analysis
python pyspark/analysis.py

# 5. Run prediction model
python pyspark/predict_crime.py

# 6. Generate visualizations
python visualizations/generate_charts.py
```

# 🚀 Chicago Crime Analysis: Complete Pipeline Guide

This document provides a step-by-step walkthrough of the entire data pipeline, from raw ingestion to the interactive dashboard. It includes essential **Cleanup** commands to ensure the pipeline doesn't fail due to existing output files.

---

## 🧹 Step 0: Cleanup & Reset
Hadoop and Spark jobs often fail if the target output directory already exists. Run these commands before starting a new run to clear old data.

### 1. Clear Local Output Folders
```bash
# Remove all processed CSV/TSV/JSON files
rm -f output/*.csv output/*.tsv output/*.json output/*.txt

# Remove all generated charts
rm -f visualizations/*.png
```

### 2. Clear Hadoop HDFS Output
```bash
# Remove the entire output directory in HDFS
hdfs dfs -rm -r /user/therealshammz/crimes/output
```

---

## 📥 Step 1: Data Ingestion
Upload the raw crime dataset to the Hadoop Distributed File System (HDFS).

```bash
# Create input directory in HDFS
hdfs dfs -mkdir -p /user/therealshammz/crimes/input

# Upload the CSV (8.5M+ records)
hdfs dfs -put dataset/crimes.csv /user/therealshammz/crimes/input/
```

---

## ⚙️ Step 2: MapReduce Aggregations
These jobs handle the massive initial aggregation of 25 years of crime data.

### Job 1: Crime Count by Year
*Calculates total incidents per year (2001–2026).*
```bash
hadoop jar $(which hadoop-streaming) \
  -input /user/therealshammz/crimes/input/crimes.csv \
  -output /user/therealshammz/crimes/output/crime_by_year \
  -mapper mapreduce/crime_by_year_mapper.py \
  -reducer mapreduce/crime_by_year_reducer.py
```

### Job 2: Crime Count by Type
*Groups all crimes by their primary category (Theft, Battery, etc.).*
```bash
hadoop jar $(which hadoop-streaming) \
  -input /user/therealshammz/crimes/input/crimes.csv \
  -output /user/therealshammz/crimes/output/crime_by_type \
  -mapper mapreduce/crime_by_type_mapper.py \
  -reducer mapreduce/crime_by_type_reducer.py
```

### Job 3: Arrest Rate by Crime Type
*Calculates the percentage of incidents that resulted in an arrest.*
```bash
hadoop jar $(which hadoop-streaming) \
  -input /user/therealshammz/crimes/input/crimes.csv \
  -output /user/therealshammz/crimes/output/arrest_rate \
  -mapper mapreduce/arrest_rate_mapper.py \
  -reducer mapreduce/arrest_rate_reducer.py
```

---

## 📤 Step 3: Retrieve Results
Fetch the aggregated data from HDFS back to your local `output/` folder for further analysis.

```bash
# Retrieve MapReduce results and rename to .tsv
hdfs dfs -get /user/therealshammz/crimes/output/crime_by_year/part-00000 output/crime_by_year.tsv
hdfs dfs -get /user/therealshammz/crimes/output/crime_by_type/part-00000 output/crime_by_type.tsv
hdfs dfs -get /user/therealshammz/crimes/output/arrest_rate/part-00000 output/arrest_rate.tsv
```

---

## 🧠 Step 4: PySpark Advanced Analytics & ML
Run Spark SQL and MLlib for complex temporal analysis and predictive modeling.

### 1. Temporal & Geographic Analysis
*Generates CSVs for Hour of Day, Day of Week, Month, and District analysis.*
```bash
python pyspark/analysis.py
```

### 2. Crime Trend Forecasting (Linear Regression)
*Trains a model to predict annual crime counts through 2030.*
```bash
python pyspark/predict_crime.py
```

### 3. Crime Type Classifier (Random Forest)
*Predicts the most likely crime type based on context and calculates feature importance.*
```bash
python pyspark/advanced_prediction.py
```

---

## 📊 Step 5: Visualizations
Generate high-fidelity static charts for reports and the research paper.

```bash
python visualizations/generate_charts.py
```
*Check the `visualizations/` folder for 8+ generated PNG files.*

---

## 🌐 Step 6: Intelligence Hub (Live Dashboard)
Launch the backend API and the interactive Streamlit dashboard.

### 1. Start the FastAPI Backend
*Provides JSON endpoints for the dashboard (Port 8080).*
```bash
python backend/main.py
```

### 2. Launch the Streamlit Dashboard
*The interactive UI for exploring the data (Port 8501).*
```bash
streamlit run dashboard.py
```

---

## 📝 Step 7: Research Paper (Optional)
Compile the LaTeX research report if you have `pdflatex` installed.

```bash
cd paper
pdflatex chicago_crime_analysis.tex
pdflatex chicago_crime_analysis.tex  # Run twice to resolve references
```
*Output: `paper/chicago_crime_analysis.pdf`*

---

## 📝 Troubleshooting
- **"Output directory already exists"**: See Step 0 and ensure HDFS `/output` is deleted.
- **Java/Spark Errors**: Ensure `JAVA_HOME` is set to Java 17 for Spark and Java 11 for Hadoop.
- **Missing Dependencies**: Run `pip install -r requirements.txt` (or install Streamlit, FastAPI, PySpark, Pandas, Matplotlib).

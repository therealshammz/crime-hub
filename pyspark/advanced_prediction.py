import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, month, dayofweek, to_timestamp, when
from pyspark.ml.feature import StringIndexer, VectorAssembler, OneHotEncoder
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
import pandas as pd

# Initialize Spark
spark = SparkSession.builder \
    .appName("ChicagoCrimeAdvancedPrediction") \
    .config("spark.driver.memory", "8g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("Loading dataset for advanced prediction...")
df = spark.read.csv(
    "hdfs://127.0.0.1:9000/user/therealshammz/crimes/input/crimes.csv",
    header=True,
    inferSchema=True
)

# Take a 20% sample to ensure it fits in memory while still being "Big Data" (~1.7M rows)
df = df.sample(withReplacement=False, fraction=0.2, seed=42)

# 1. Data Cleaning & Feature Engineering
# Filter for top 10 crime types to improve model focus and accuracy
top_10_crimes = [
    "THEFT", "BATTERY", "CRIMINAL DAMAGE", "NARCOTICS", "ASSAULT",
    "OTHER OFFENSE", "BURGLARY", "MOTOR VEHICLE THEFT", "DECEPTIVE PRACTICE", "ROBBERY"
]

df = df.filter(col("Primary Type").isin(top_10_crimes))
df = df.withColumn("ParsedDate", to_timestamp(col("Date"), "MM/dd/yyyy hh:mm:ss a"))
df = df.withColumn("Hour", hour("ParsedDate"))
df = df.withColumn("DayOfWeek", dayofweek("ParsedDate"))
df = df.withColumn("Month", month("ParsedDate"))

# Handle missing values in important columns
df = df.na.drop(subset=["District", "Ward", "Community Area", "Location Description"])

# 2. String Indexing & Encoding
# Convert categorical strings to numeric indices
loc_indexer = StringIndexer(inputCol="Location Description", outputCol="LocDescIndex", handleInvalid="skip")
label_indexer = StringIndexer(inputCol="Primary Type", outputCol="label")

# Convert Boolean 'Domestic' to Integer
df = df.withColumn("DomesticInt", when(col("Domestic") == "true", 1).otherwise(0))

# 3. Vector Assembler
# Combine all features into a single vector
feature_cols = ["Hour", "DayOfWeek", "Month", "District", "Ward", "Community Area", "LocDescIndex", "DomesticInt"]
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")

# 4. Model Training
print("Training Random Forest Classifier (this may take a few minutes)...")
rf = RandomForestClassifier(labelCol="label", featuresCol="features", numTrees=100, maxDepth=10, maxBins=150, seed=42)

# Create and Fit Pipeline
pipeline = Pipeline(stages=[loc_indexer, label_indexer, assembler, rf])
train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

model = pipeline.fit(train_df)

# 5. Evaluation
print("Evaluating model performance...")
predictions = model.transform(test_df)

evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)

f1_evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1")
f1_score = f1_evaluator.evaluate(predictions)

# Baseline: Always predict the most common class (Theft)
# Theft is index 0 (usually) after StringIndexer on these 10 classes
print(f"\nModel Accuracy: {accuracy:.4f}")
print(f"Model F1-Score: {f1_score:.4f}")

# 6. Extract Feature Importance
rf_model = model.stages[-1]
importances = rf_model.featureImportances.toArray()
feature_importance_df = pd.DataFrame({
    "Feature": feature_cols,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

feature_importance_df.to_csv("/home/therealshammz/bdata/output/feature_importance.csv", index=False)
print("\nFeature importance saved to output/feature_importance.csv")

# 7. Sample Predictions Output
print("\nSample Predictions:")
predictions.select("Primary Type", "prediction").show(10)

# Save metrics for paper
with open("/home/therealshammz/bdata/output/model_metrics.txt", "w") as f:
    f.write(f"Accuracy: {accuracy:.4f}\n")
    f.write(f"F1-Score: {f1_score:.4f}\n")

spark.stop()

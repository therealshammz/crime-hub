import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, month, dayofweek, count, to_timestamp

spark = SparkSession.builder \
    .appName("ChicagoCrimeAnalysis") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("Loading dataset...")
df = spark.read.csv(
    "hdfs://127.0.0.1:9000/user/therealshammz/crimes/input/crimes.csv",
    header=True,
    inferSchema=True
)

# Parse the date column explicitly - format is MM/dd/yyyy hh:mm:ss aa
df = df.withColumn("ParsedDate", to_timestamp(col("Date"), "MM/dd/yyyy hh:mm:ss a"))

print(f"Total records: {df.count()}")

# Analysis 1: Crimes by hour
print("\nCrimes by Hour of Day:")
df_hour = df.withColumn("Hour", hour("ParsedDate")) \
    .groupBy("Hour").agg(count("*").alias("Count")) \
    .orderBy("Hour")
df_hour.show(24)
df_hour.toPandas().to_csv("/home/therealshammz/bdata/output/crimes_by_hour.csv", index=False)

# Analysis 2: Crimes by month
print("\nCrimes by Month:")
df_month = df.withColumn("Month", month("ParsedDate")) \
    .groupBy("Month").agg(count("*").alias("Count")) \
    .orderBy("Month")
df_month.show(12)
df_month.toPandas().to_csv("/home/therealshammz/bdata/output/crimes_by_month.csv", index=False)

# Analysis 3: Crimes by day of week
print("\nCrimes by Day of Week (1=Sunday, 7=Saturday):")
df_dow = df.withColumn("DayOfWeek", dayofweek("ParsedDate")) \
    .groupBy("DayOfWeek").agg(count("*").alias("Count")) \
    .orderBy("DayOfWeek")
df_dow.show(7)
df_dow.toPandas().to_csv("/home/therealshammz/bdata/output/crimes_by_dow.csv", index=False)

# Analysis 4: Top 10 locations
print("\nTop 10 Crime Locations:")
df_loc = df.groupBy("Location Description") \
    .agg(count("*").alias("Count")) \
    .orderBy(col("Count").desc())
df_loc.show(10)
df_loc.toPandas().to_csv("/home/therealshammz/bdata/output/crimes_by_location.csv", index=False)

# Analysis 5: Crimes by district
print("\nCrimes by District:")
df_dist = df.groupBy("District") \
    .agg(count("*").alias("Count")) \
    .orderBy(col("Count").desc())
df_dist.show(25)
df_dist.toPandas().to_csv("/home/therealshammz/bdata/output/crimes_by_district.csv", index=False)

# Analysis 6: Domestic vs non-domestic
print("\nDomestic vs Non-Domestic:")
df_dom = df.groupBy("Domestic") \
    .agg(count("*").alias("Count"))
df_dom.show()
df_dom.toPandas().to_csv("/home/therealshammz/bdata/output/domestic_vs_nondomestic.csv", index=False)

print("\nAll analyses complete. CSVs saved to ~/bdata/output/")
spark.stop()

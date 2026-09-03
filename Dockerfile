FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    openjdk-17-jdk \
    wget \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Set Java environments
ENV JAVA_HOME_11=/usr/lib/jvm/java-11-openjdk-amd64
ENV JAVA_HOME_17=/usr/lib/jvm/java-17-openjdk-amd64

# Install Hadoop
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop

RUN mkdir -p $HADOOP_HOME && \
    cd /tmp && \
    wget -q https://archive.apache.org/dist/hadoop/core/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzf hadoop-$HADOOP_VERSION.tar.gz -C $HADOOP_HOME --strip-components=1 && \
    rm -rf /tmp/hadoop-$HADOOP_VERSION.tar.gz

# Install Spark
ENV SPARK_VERSION=3.5.3
ENV SPARK_HOME=/opt/spark

RUN mkdir -p $SPARK_HOME && \
    cd /tmp && \
    wget -q https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz && \
    tar -xzf spark-$SPARK_VERSION-bin-hadoop3.tgz -C $SPARK_HOME --strip-components=1 && \
    rm -rf /tmp/spark-$SPARK_VERSION-bin-hadoop3.tgz

# Set PATH
ENV PATH=$PATH:$HADOOP_HOME/bin:$SPARK_HOME/bin

# Set JAVA_HOME for different tools
ENV JAVA_HOME=$JAVA_HOME_17

# Create working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/output /app/visualizations /app/dataset /app/hdfs

# Set proper permissions
RUN chmod +x mapreduce/*.py

# Default command
CMD ["bash"]
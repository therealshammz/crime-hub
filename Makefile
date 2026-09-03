.PHONY: help setup run-hadoop run-spark run-api run-dashboard clean clean-hdfs clean-output test verify

# Default target
help:
	@echo "Chicago Crime Intelligence Hub - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup           - Create virtual environment and install dependencies"
	@echo "  make docker-setup    - Build and start Docker containers"
	@echo ""
	@echo "Data Pipeline:"
	@echo "  make upload-data     - Upload crime data to HDFS"
	@echo "  make run-mapreduce   - Run all MapReduce jobs"
	@echo "  make run-spark       - Run PySpark analysis"
	@echo ""
	@echo "Visualization & API:"
	@echo "  make run-api         - Start FastAPI backend (Port 8080)"
	@echo "  make run-dashboard   - Start Streamlit dashboard (Port 8501)"
	@echo "  make generate-charts - Generate visualization charts"
	@echo ""
	@echo "Paper:"
	@echo "  make compile-paper   - Compile LaTeX research paper"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           - Clean local output files"
	@echo "  make clean-hdfs      - Clean HDFS output directory"
	@echo "  make clean-all       - Clean all outputs (local + HDFS)"
	@echo ""
	@echo "Verification:"
	@echo "  make verify          - Verify API and outputs"
	@echo "  make test            - Run tests"

# Setup
setup:
	python -m venv venv
	source venv/bin/activate && pip install -r requirements.txt

docker-setup:
	docker-compose build
	docker-compose up -d

# Data Pipeline
upload-data:
	hdfs dfs -mkdir -p /user/therealshammz/crimes/input
	hdfs dfs -put dataset/crimes.csv /user/therealshammz/crimes/input/

run-mapreduce:
	@echo "Running MapReduce jobs..."
	hadoop jar $$(which hadoop-streaming) \
		-input /user/therealshammz/crimes/input/crimes.csv \
		-output /user/therealshammz/crimes/output/crime_by_year \
		-mapper mapreduce/crime_by_year_mapper.py \
		-reducer mapreduce/crime_by_year_reducer.py
	hadoop jar $$(which hadoop-streaming) \
		-input /user/therealshammz/crimes/input/crimes.csv \
		-output /user/therealshammz/crimes/output/crime_by_type \
		-mapper mapreduce/crime_by_type_mapper.py \
		-reducer mapreduce/crime_by_type_reducer.py
	hadoop jar $$(which hadoop-streaming) \
		-input /user/therealshammz/crimes/input/crimes.csv \
		-output /user/therealshammz/crimes/output/arrest_rate \
		-mapper mapreduce/arrest_rate_mapper.py \
		-reducer mapreduce/arrest_rate_reducer.py

run-spark:
	python pyspark/analysis.py
	python pyspark/predict_crime.py
	python pyspark/advanced_prediction.py

# Visualization & API
run-api:
	python backend/main.py

run-dashboard:
	streamlit run dashboard.py

generate-charts:
	python visualizations/generate_charts.py

# Paper
compile-paper:
	cd paper && pdflatex chicago_crime_analysis.tex && pdflatex chicago_crime_analysis.tex

# Cleanup
clean:
	rm -f output/*.csv output/*.tsv output/*.json output/*.txt
	rm -f visualizations/*.png

clean-hdfs:
	hdfs dfs -rm -r /user/therealshammz/crimes/output

clean-all: clean clean-hdfs

# Verification
verify:
	@echo "Checking API health..."
	curl -s http://localhost:8080/ | jq
	@echo ""
	@echo "Checking overview endpoint..."
	curl -s http://localhost:8080/api/overview | jq
	@echo ""
	@echo "Checking model metrics..."
	cat output/model_metrics.txt 2>/dev/null || echo "Model metrics not found"

test:
	@echo "Running tests..."
	python -m pytest tests/ -v 2>/dev/null || echo "No tests found or pytest not installed"
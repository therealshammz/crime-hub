"""Tests for Chicago Crime Intelligence Hub."""

import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestBackend:
    """Tests for the FastAPI backend."""

    def test_import_backend(self):
        """Test that backend module can be imported."""
        try:
            from backend import main

            assert main is not None
        except ImportError:
            pytest.skip("Backend module not available")

    def test_app_exists(self):
        """Test that FastAPI app exists."""
        try:
            from backend.main import app

            assert app is not None
        except ImportError:
            pytest.skip("Backend module not available")


class TestPySpark:
    """Tests for PySpark analysis scripts."""

    def test_analysis_script_exists(self):
        """Test that analysis script exists."""
        assert os.path.exists("pyspark/analysis.py")

    def test_predict_script_exists(self):
        """Test that prediction script exists."""
        assert os.path.exists("pyspark/predict_crime.py")

    def test_advanced_prediction_exists(self):
        """Test that advanced prediction script exists."""
        assert os.path.exists("pyspark/advanced_prediction.py")


class TestMapReduce:
    """Tests for MapReduce scripts."""

    def test_crime_by_year_mapper_exists(self):
        """Test that crime by year mapper exists."""
        assert os.path.exists("mapreduce/crime_by_year_mapper.py")

    def test_crime_by_year_reducer_exists(self):
        """Test that crime by year reducer exists."""
        assert os.path.exists("mapreduce/crime_by_year_reducer.py")

    def test_crime_by_type_mapper_exists(self):
        """Test that crime by type mapper exists."""
        assert os.path.exists("mapreduce/crime_by_type_mapper.py")

    def test_crime_by_type_reducer_exists(self):
        """Test that crime by type reducer exists."""
        assert os.path.exists("mapreduce/crime_by_type_reducer.py")

    def test_arrest_rate_mapper_exists(self):
        """Test that arrest rate mapper exists."""
        assert os.path.exists("mapreduce/arrest_rate_mapper.py")

    def test_arrest_rate_reducer_exists(self):
        """Test that arrest rate reducer exists."""
        assert os.path.exists("mapreduce/arrest_rate_reducer.py")


class TestVisualizations:
    """Tests for visualization scripts."""

    def test_generate_charts_exists(self):
        """Test that chart generation script exists."""
        assert os.path.exists("visualizations/generate_charts.py")


class TestDashboard:
    """Tests for Streamlit dashboard."""

    def test_dashboard_exists(self):
        """Test that dashboard file exists."""
        assert os.path.exists("dashboard.py")


class TestDocumentation:
    """Tests for documentation files."""

    def test_readme_exists(self):
        """Test that README exists."""
        assert os.path.exists("README.md")

    def test_commands_md_exists(self):
        """Test that COMMANDS.md exists."""
        assert os.path.exists("COMMANDS.md")

    def test_pipeline_md_exists(self):
        """Test that PIPELINE.md exists."""
        assert os.path.exists("PIPELINE.md")

    def test_agents_md_exists(self):
        """Test that AGENTS.md exists."""
        assert os.path.exists("AGENTS.md")


class TestConfiguration:
    """Tests for configuration files."""

    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        assert os.path.exists("requirements.txt")

    def test_gitignore_exists(self):
        """Test that .gitignore exists."""
        assert os.path.exists(".gitignore")

    def test_license_exists(self):
        """Test that LICENSE exists."""
        assert os.path.exists("LICENSE")

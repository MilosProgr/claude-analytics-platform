# claude-analytics-platform
End-to-end telemetry analytics platform for Claude Code sessions, featuring structured data ingestion, SQL-based storage, interactive dashboards, and AI-assisted development workflow.

## 🎯 Purpose

This project simulates a real-world telemetry analytics pipeline for AI coding sessions.  
It demonstrates data engineering fundamentals including parsing, relational modeling, aggregation logic, testing, and interactive visualization.

## 🚀 Features

- JSONL telemetry parsing
- Relational data modeling with SQLAlchemy
- Token and cost analytics
- Model usage analysis
- Tool success & error rate tracking
- Time-series token trends
- Interactive dashboard (Streamlit)
- Fake data generator for testing


## 🏗 Architecture

JSONL Logs → Parsing → SQLite (SQLAlchemy ORM) → Analytics Layer → Streamlit Dashboard

## Core Components
- `database/` – ORM models and DB setup
- `analytics/` – Business metrics & aggregations
- `dashboard/` – Streamlit UI
- `generate_fake_data.py` – Synthetic dataset generator
- `explore.ipynb` – Exploratory Data Analysis

## 📂 Project Structure
```text
data/
├── events/
│   └── parsed_events.csv        # Parsed telemetry logs
├── output/
│   ├── employees.csv            # Employee CSV
│   └── telemetry_logs.jsonl     # Original tele    metry logs

src/
├── analytics/
│   ├── metrics_validation.py   # Manual validation of analytics results         
│   └── metrics.py              # Analytics functions
├── dashboard/
│   └── app.py                  # Streamlit dashboard
├── database/
│   ├── db.py                   # SQLAlchemy engine and session
│   ├── models.py               # Employee and Event models
│   ├── setup.py                # Database table creation
│   └── telemetry.db            # SQLite database file
└── ingestion/
    ├── load_data.py            # Data ingestion script
    └── parser.py               # Parser for raw JSONL logs
        
explore.ipynb
generate_fake_data.py             # Synthetic dataset generator
LLM_USAGE.md 
requirements.txt                  # Required Python libraries
technical_assessment_presentation.pdf # Insights presentation
```
    
## ⚙️ Setup

### 1.📥 Clone the repository

    ```bash
    git clone <repo_url>
    cd claude-analytics-platform
    ```

### 2. 🧩 Create a virtual environment
    ```bash
        python -m venv env
        # Linux / Mac
        source env/bin/activate   
        # Windows
        env\Scripts\activate    
    ```

### 3. 📦 Install dependencies
        pip install -r requirements.txt
        Required packages include:
            pandas
            sqlalchemy
            streamlit
            seaborn
            matplotlib

### 4. 🗄 Database Setup
        Initialize the SQLite database:
            python src/database/setup.py

        This creates the following tables:
            employees
            events

### 5 🧪 Synthetic Data Generation
        For testing and demonstration purposes:
            python generate_fake_data.py --num-users 100 --num-sessions 5000 --days 60 --output-dir data/output/  #Output for generated files
        This generates synthetic employees and telemetry events that can be loaded into the database.

### 6 📥 Data ingestion
        Load employees and telemetry events
            python src/ingestion/load_data.py
        Stores the data in SQLite for analytics.

### 7 🔎 Parser
        Transforms raw JSONL telemetry logs into structured event records:
        python src/ingestion/parser.py

        Output:
            Structured CSV file (optional)

### 8 📊 Analytics Layer

    Performs all analytical computations and aggregation logic:
        Token usage by practice
        Cost by practice
        Model usage distribution
        Peak usage hours
        Tool success rate
        Error rate by model
        Average session duration
        Token usage over time
        Filter options loader
    metrics_validation.py  
    This module is used for manual validation of analytical computations.

    Purpose:
        Cross-check aggregated metrics against raw SQL queries
        Validate filtering logic
        Ensure consistency between database and analytics layer

### 9.🖥 Streamlit dashboard

        Runs the dashboard:
            streamlit run src/dashboard/app.py

        Sidebar filters: practice, level, model, date range
        Tabs:
            Overview: token usage, model distribution, peak hours
            Cost Analytics: cost and average session duration
            Token Analytics: token trends over time
            Tool Usage: tool success rates
            Errors: error rate by model

### 10.📓 explore.ipynb
        Used for analyzing raw telemetry logs before ingestion. Demonstrates:
            JSONL parsing
            Event extraction from log batches
            Attribute normalization
            Basic usage statistics
            Model and tool distribution analysis




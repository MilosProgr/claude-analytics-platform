# claude-analytics-platform
End-to-end telemetry analytics platform for Claude Code sessions, featuring structured data ingestion, SQL-based storage, interactive dashboards, and AI-assisted development workflow.

Features

JSONL telemetry parsing
Relational data modeling with SQLAlchemy
Token and cost analytics
Model usage analysis
Tool success & error rate tracking
Time-series token trends
Interactive dashboard (Streamlit)
Fake data generator for testing
Struktura projekta.
Architecture

JSONL Logs → Parsing → SQLite (SQLAlchemy ORM) → Analytics Layer → Streamlit Dashboard

Core Components:
database/ – ORM models and DB setup
analytics/ – Business metrics & aggregations
dashboard/ – Streamlit UI
generate_fake_data.py – Synthetic dataset generator
explore.ipynb – Exploratory Data Analysis

dataflow

data/
├── events/
│   └── parsed_events.csv        # Parsed telemetry logs
├── output/
│   ├── employees.csv            # Employee CSV
│   └── telemetry_logs.jsonl     # Original telemetry logs

src/
├── analytics/
│   ├── metrics.py               # Analytics functions
│   └── test_metrics.py          # Unit tests / average session duration
├── database/
│   ├── db.py                    # SQLAlchemy engine and session
│   ├── models.py                # Employee and Event models
│   └── setup_db.py              # Database table creation
├── dashboard/
│   └── app.py                   # Streamlit dashboard
├── load_data.py                 # Data ingestion script
└── ingestion/
    └── parser/
        └── parse_telemetry.py  # Parser for raw JSONL logs
explore.ipynb
generate_fake_data.py             # Fake data 
requirements.txt                  # Required Python libraries


## Setup

### 1. Clone the repository

    ```bash
    git clone <repo_url>
    cd claude-analytics-platform


    2.Create a virtual environment
        python -m venv env
        source env/bin/activate   # Linux / Mac
        env\Scripts\activate      # Windows

    3. Install dependencies
        pip install -r requirements.txt
        Required packages include:
            pandas
            sqlalchemy
            streamlit
            seaborn
            matplotlib

    4. Database Setup
        Initialize the SQLite database:
            python src/database/setup_db.py

        This creates the following tables:
            employees
            events

    5 Synthetic Data Generation
        For testing and demonstration purposes:
            python generate_fake_data.py --num-users 100 --num-sessions 5000 --days 60

    This generates synthetic employees and telemetry events that can be loaded into the database.

    6 Data ingestion
    Load employees and telemetry events
        python src/load_data.py
    Stores the data in SQLite for analytics.

    7 Parser
        Transforms raw JSONL telemetry logs into structured event records:

        python src/ingestion/parser/parse_telemetry.py

    Output:
        Structured CSV file (optional)

    8 Analytics Layer

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
    test_metrics.py
    This module contains unit tests for validating analytical computations.

    Purpose:
        Ensure correctness of aggregations
        Validate filtering logic

        Detect regressions when metrics evolve

        Guarantee consistency between database and analytics layer

    9. **Streamlit dashboard**

        Runs the dashboard:
            streamlit run src/dashboard/app.py

        Sidebar filters: practice, level, model, date range
        Tabs:
            Overview: token usage, model distribution, peak hours

            Cost Analytics: cost and average session duration

            Token Analytics: token trends over time

            Tool Usage: tool success rates

            Errors: error rate by model

    10. **explore.ipynb**
    Used for analyzing raw telemetry logs before ingestion. Demonstrates:
        JSONL parsing

        Event extraction from log batches

        Attribute normalization

        Basic usage statistics

        Model and tool distribution analysis




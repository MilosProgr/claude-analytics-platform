import pandas as pd
from sqlalchemy import create_engine, text

DB_PATH = "sqlite:///src/database/telemetry.db"

def get_engine():
    return create_engine(DB_PATH)


# -------------------------------
# Helper: Safe filter builder
# -------------------------------
def build_filters(practice=None, level=None, model=None, date_range=None,include_model=True):
    conditions = []
    params = {}

    if practice:
        placeholders = ", ".join([f":practice_{i}" for i in range(len(practice))])
        conditions.append(f"e.practice IN ({placeholders})")
        for i, val in enumerate(practice):
            params[f"practice_{i}"] = val
    if level:
        placeholders = ", ".join([f":level_{i}" for i in range(len(level))])
        conditions.append(f"e.level IN ({placeholders})")
        for i, val in enumerate(level):
            params[f"level_{i}"] = val

    if include_model and model:
        placeholders = ", ".join([f":model_{i}" for i in range(len(model))])
        conditions.append(f"ev.model IN ({placeholders})")
        for i, val in enumerate(model):
            params[f"model_{i}"] = val

    if date_range and len(date_range) == 2:
        conditions.append("DATE(ev.timestamp) BETWEEN :start_date AND :end_date")
        params["start_date"] = str(date_range[0])
        params["end_date"] = str(date_range[1])

    where_clause = ""
    if conditions:
        where_clause = " AND " + " AND ".join(conditions)

    return where_clause, params


# -------------------------------
# 1️⃣ Token consumption by practice
# -------------------------------
def get_token_usage_by_practice(practice=None, level=None, model=None, date_range=None):
    engine = get_engine()

    base_query = """
    SELECT e.practice,
           SUM(ev.input_tokens + ev.output_tokens) AS total_tokens
    FROM events ev
    JOIN employees e ON ev.user_email = e.email
    WHERE ev.event_type = 'claude_code.api_request'
    """

    filters, params = build_filters(practice, level, model, date_range)

    final_query = base_query + filters + """
    GROUP BY e.practice
    ORDER BY total_tokens DESC
    """

    return pd.read_sql(text(final_query), engine, params=params)


# -------------------------------
# 2️⃣ Cost by practice
# -------------------------------
def get_cost_by_practice(practice=None, level=None, model=None, date_range=None):
    engine = get_engine()

    base_query = """
    SELECT e.practice,
           SUM(ev.cost_usd) AS total_cost
    FROM events ev
    JOIN employees e ON ev.user_email = e.email
    WHERE ev.event_type = 'claude_code.api_request'
    """

    filters, params = build_filters(practice, level, model, date_range)

    final_query = base_query + filters + """
    GROUP BY e.practice
    ORDER BY total_cost DESC
    """

    return pd.read_sql(text(final_query), engine, params=params)


# -------------------------------
# 3️⃣ Model usage distribution
# -------------------------------
def get_model_distribution(practice=None, level=None, model=None, date_range=None):
    engine = get_engine()

    base_query = """
    SELECT ev.model,
           COUNT(*) AS usage_count
    FROM events ev
    JOIN employees e ON ev.user_email = e.email
    WHERE ev.event_type = 'claude_code.api_request'
    """

    filters, params = build_filters(practice, level, model, date_range)

    final_query = base_query + filters + """
    GROUP BY ev.model
    ORDER BY usage_count DESC
    """

    return pd.read_sql(text(final_query), engine, params=params)


# -------------------------------
# 4️⃣ Peak usage hours
# -------------------------------
def get_peak_usage_hours(practice=None, level=None, model=None, date_range=None):
    engine = get_engine()

    base_query = """
    SELECT ev.timestamp, e.practice
    FROM events ev
    JOIN employees e ON ev.user_email = e.email
    WHERE ev.event_type = 'claude_code.api_request'
    """

    filters, params = build_filters(practice, level, model, date_range)

    df = pd.read_sql(text(base_query + filters), engine, params=params)

    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour

    return df.groupby(["hour", "practice"]).size().reset_index(name="request_count")


# -------------------------------
# 5️⃣ Tool success rate
# -------------------------------
def get_tool_success_rate(practice=None, level=None, model=None, date_range=None):
    engine = get_engine()

    base_query = """
    SELECT ev.tool_name, ev.success
    FROM events ev
    JOIN employees e ON ev.user_email = e.email
    WHERE ev.event_type = 'claude_code.tool_result'
    """

    # 👇 include_model=False jer tool_result nema model
    filters, params = build_filters(
        practice, level, model, date_range, include_model=False
    )

    df = pd.read_sql(text(base_query + filters), engine, params=params)

    if df.empty:
        return df

    # 👇 success je 0/1 integer
    df["success"] = df["success"].astype(int)

    result = df.groupby("tool_name")["success"].agg(["count", "sum"]).reset_index()
    result["success_rate"] = result["sum"] / result["count"]

    

    return result[["tool_name", "success_rate"]].sort_values(
        "success_rate", ascending=False
    )


# -------------------------------
# 6️⃣ Error rate by model
# -------------------------------
def get_error_rate_by_model(practice=None, level=None, model=None, date_range=None):
    engine = get_engine()

    filters, params = build_filters(practice, level, model, date_range)

    req_query = """
    SELECT ev.model,
           COUNT(*) as request_count
    FROM events ev
    JOIN employees e ON ev.user_email = e.email
    WHERE ev.event_type = 'claude_code.api_request'
    """ + filters + """
    GROUP BY ev.model
    """

    err_query = """
    SELECT ev.model,
           COUNT(*) as error_count
    FROM events ev
    JOIN employees e ON ev.user_email = e.email
    WHERE ev.event_type = 'claude_code.api_error'
    """ + filters + """
    GROUP BY ev.model
    """

    requests = pd.read_sql(text(req_query), engine, params=params)
    errors = pd.read_sql(text(err_query), engine, params=params)

    df = requests.merge(errors, on="model", how="left")
    df["error_count"] = df["error_count"].fillna(0)
    df["error_rate"] = df["error_count"] / df["request_count"]

    return df[["model", "error_rate"]].sort_values("error_rate", ascending=False)


# -------------------------------
# 7️⃣ Average session duration
# -------------------------------
def get_avg_session_duration(practice=None, level=None, model=None, date_range=None):
    engine = get_engine()

    base_query = """
    SELECT ev.session_id, ev.timestamp
    FROM events ev
    JOIN employees e ON ev.user_email = e.email
    WHERE 1=1
    """

    filters, params = build_filters(practice, level, model, date_range)

    df = pd.read_sql(text(base_query + filters), engine, params=params)

    if df.empty:
        return 0

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    session_duration = df.groupby("session_id")["timestamp"].agg(["min", "max"]).reset_index()
    session_duration["duration_seconds"] = (
        session_duration["max"] - session_duration["min"]
    ).dt.total_seconds()

    return session_duration["duration_seconds"].mean() / 60  # minutes


# -------------------------------
# 8️⃣ Token usage over time
# -------------------------------
def get_token_usage_over_time(practice=None, level=None, model=None, date_range=None):
    engine = get_engine()

    base_query = """
    SELECT ev.timestamp,
           e.practice,
           (ev.input_tokens + ev.output_tokens) AS tokens
    FROM events ev
    JOIN employees e ON ev.user_email = e.email
    WHERE ev.event_type = 'claude_code.api_request'
    """

    filters, params = build_filters(practice, level, model, date_range)

    return pd.read_sql(text(base_query + filters), engine, params=params)


# -------------------------------
# 9️⃣ Load filter options
# -------------------------------
def get_filter_options():
    engine = get_engine()

    practices = pd.read_sql(
        text("SELECT DISTINCT practice FROM employees ORDER BY practice"),
        engine
    )["practice"].dropna().tolist()

    levels = pd.read_sql(
        text("SELECT DISTINCT level FROM employees ORDER BY level"),
        engine
    )["level"].dropna().tolist()

    models = pd.read_sql(
        text("""
            SELECT DISTINCT model
            FROM events
            WHERE event_type = 'claude_code.api_request'
            ORDER BY model
        """),
        engine
    )["model"].dropna().tolist()

    dates = pd.read_sql(
        text("SELECT MIN(timestamp) as min_date, MAX(timestamp) as max_date FROM events"),
        engine
    )

    min_date = pd.to_datetime(dates["min_date"][0])
    max_date = pd.to_datetime(dates["max_date"][0])

    return practices, levels, models, min_date, max_date
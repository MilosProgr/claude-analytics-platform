import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.analytics.metrics import (
    get_token_usage_by_practice,
    get_cost_by_practice,
    get_model_distribution,
    get_peak_usage_hours,
    get_tool_success_rate,
    get_error_rate_by_model,
    get_avg_session_duration,
    get_token_usage_over_time,
    get_filter_options
)

# ---------------- Page Config ----------------
st.set_page_config(page_title="Claude Code Analytics", layout="wide")
st.title("Claude Code Telemetry Analytics Platform")

# ---------------- Sidebar Filters ----------------
st.sidebar.header("Filters")

# Zameni sa dinamičkim df-om iz baze ako želiš
practices, levels, models, min_date, max_date = get_filter_options()

selected_practice = st.sidebar.multiselect("Practice", practices, default=practices)
selected_level = st.sidebar.multiselect("Level", levels, default=levels)
selected_model = st.sidebar.multiselect("Model", models, default=models)
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

# ---------------- Tabs ----------------
tab_overview, tab_cost, tab_token, tab_tool, tab_errors = st.tabs([
    "Overview",
    "Cost Analytics",
    "Token Analytics",
    "Tool Usage",
    "Errors"
])

# ---------------- Tab 1: Overview ----------------
with tab_overview:
    st.header("Usage Overview")
    col1, col2 = st.columns(2)

    # Token Usage by Practice
    with col1:
        st.subheader("Token Usage by Practice")
        df_tokens = get_token_usage_by_practice(
            practice=selected_practice,
            level=selected_level,
            model=selected_model,
            date_range=date_range
        )
        if not df_tokens.empty:
            df_tokens_plot = df_tokens.set_index('practice')
            st.bar_chart(df_tokens_plot['total_tokens'])

    # Peak Usage Hours (Heatmap)
    with col2:
        st.subheader("Peak Usage Hours")
        df_peak = get_peak_usage_hours(
            practice=selected_practice,
            level=selected_level,
            model=selected_model,
            date_range=date_range
        )
        if not df_peak.empty:
            df_heat = df_peak.pivot(index='hour', columns='practice', values='request_count').fillna(0)
            fig, ax = plt.subplots(figsize=(6,4))
            sns.heatmap(df_heat, annot=True, fmt="g", cmap="YlGnBu", ax=ax)
            st.pyplot(fig)

    # Model Distribution
    st.subheader("Model Distribution")
    df_models = get_model_distribution(
        practice=selected_practice,
        level=selected_level,
        model=selected_model,
        date_range=date_range
    )
    if not df_models.empty:
        df_models_plot = df_models.set_index('model')
        st.bar_chart(df_models_plot['usage_count'])

# ---------------- Tab 2: Cost Analytics ----------------
with tab_cost:
    st.header("Cost Analytics")
    col1, col2 = st.columns(2)

    # Cost by Practice
    with col1:
        st.subheader("Cost by Practice")
        df_cost = get_cost_by_practice(
            practice=selected_practice,
            level=selected_level,
            model=selected_model,
            date_range=date_range
        )
        if not df_cost.empty:
            df_cost_plot = df_cost.set_index('practice')
            st.bar_chart(df_cost_plot['total_cost'])

    # Average Session Duration
    with col2:
        st.subheader("Average Session Duration")
        avg_duration = get_avg_session_duration(
            practice=selected_practice,
            level=selected_level,
            model=selected_model,
            date_range=date_range
        )
        st.metric("Avg Session Duration (min)", round(avg_duration, 2))

# ---------------- Tab 3: Token Analytics ----------------
with tab_token:
    st.header("Token Analytics Over Time")
    df_time = get_token_usage_over_time(
        practice=selected_practice,
        level=selected_level,
        model=selected_model,
        date_range=date_range
    )
    if not df_time.empty:
        st.subheader("Tokens Over Time")
        df_time_plot = df_time.set_index('timestamp')
        st.line_chart(df_time_plot['tokens'])

        st.subheader("Tokens by Practice")
        df_tokens_practice = df_time.groupby('practice')['tokens'].sum().reset_index()
        df_tokens_practice_plot = df_tokens_practice.set_index('practice')
        st.bar_chart(df_tokens_practice_plot['tokens'])

# ---------------- Tab 4: Tool Usage ----------------
with tab_tool:
    st.header("Tool Usage")
    df_tools = get_tool_success_rate(
        practice=selected_practice,
        level=selected_level,
        model=selected_model,
        date_range=date_range
    )
    if not df_tools.empty:
        st.subheader("Tool Success Rate")
        st.dataframe(df_tools)
        for idx, row in df_tools.iterrows():
            st.metric(f"{row['tool_name']}", f"{row['success_rate']*100:.2f}%")

# ---------------- Tab 5: Errors ----------------
with tab_errors:
    st.header("Error Analytics")
    df_errors = get_error_rate_by_model(
        practice=selected_practice,
        level=selected_level,
        model=selected_model,
        date_range=date_range
    )
    if not df_errors.empty:
        st.subheader("Error Rate by Model")
        df_errors_plot = df_errors.set_index('model')
        st.bar_chart(df_errors_plot['error_rate'])
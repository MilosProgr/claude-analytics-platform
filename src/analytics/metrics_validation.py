from src.analytics.metrics import *

print(get_token_usage_by_practice())
print(get_cost_by_practice())
print(get_model_distribution())
print(get_peak_usage_hours())
print(get_tool_success_rate())
print(get_error_rate_by_model())
print("Avg session duration (seconds):", get_avg_session_duration())
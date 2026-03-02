import json
from pathlib import Path
import csv

# ------------------------
# Helper functions
# ------------------------
def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

# ------------------------
# Parser function
# ------------------------
def parse_telemetry_file(file_path: str):
    events = []
    file_path = Path(file_path)

    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            batch = json.loads(line)

            for log_event in batch.get("logEvents", []):
                try:
                    event = json.loads(log_event["message"])
                    attributes = event.get("attributes", {})

                    parsed_event = {
                        "event_type": event.get("body"),
                        "timestamp": attributes.get("event.timestamp"),
                        "session_id": attributes.get("session.id"),
                        "user_email": attributes.get("user.email"),
                        "model": attributes.get("model"),
                        "input_tokens": safe_int(attributes.get("input_tokens")),
                        "output_tokens": safe_int(attributes.get("output_tokens")),
                        "tokens": None,  # ovo ćemo popuniti kasnije
                        "cost_usd": safe_float(attributes.get("cost_usd")),
                        "tool_name": attributes.get("tool_name"),
                        "success": attributes.get("success"),
                        "duration_ms": safe_int(attributes.get("duration_ms")),
                    }

                    # Popuni total tokens ako postoje input/output
                    input_tokens = parsed_event["input_tokens"] or 0
                    output_tokens = parsed_event["output_tokens"] or 0
                    parsed_event["tokens"] = input_tokens + output_tokens

                    events.append(parsed_event)

                except Exception as e:
                    print(f"Skipping corrupted event: {e}")

    return events

# ------------------------
# Main
# ------------------------
if __name__ == "__main__":
    # Parsiranje fajla
    data = parse_telemetry_file("data/output/telemetry_logs.jsonl")
    print(f"Parsed {len(data)} events")

    # Putanja gde ćemo sačuvati CSV
    output_csv_path = "data/events/parsed_events.csv"

    # Definiši kolone koje želimo da sačuvamo
    fieldnames = [
        "event_type",
        "timestamp",
        "session_id",
        "user_email",
        "model",
        "input_tokens",
        "output_tokens",
        "tokens",
        "cost_usd",
        "tool_name",
        "success",
        "duration_ms"
    ]

    # Upisi sve parsed evente u CSV
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for e in data:
            writer.writerow(e)

    print(f"Saved parsed events to {output_csv_path}")
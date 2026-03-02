import csv
import json
from datetime import datetime
from src.database.db import SessionLocal
from src.database.models import Employee, Event 

session = SessionLocal()

# --- Employees ---
with open("data/output/employees.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        emp = Employee(
            email=row["email"],
            practice=row["practice"],
            level=row["level"],
            location=row["location"]
        )
        session.merge(emp)  # merge -> update ili insert
session.commit()
print("Employees loaded.")

# --- Events ---
with open("data/output/telemetry_logs.jsonl") as f:
    for line in f:
        batch = json.loads(line)
        for log in batch["logEvents"]:
            msg = json.loads(log["message"])
            attrs = msg["attributes"]
            e = Event(
                event_type=msg.get("body"),
                timestamp=datetime.strptime(attrs["event.timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                session_id=attrs.get("session.id"),
                user_email=attrs.get("user.email"),
                model=attrs.get("model"),
                input_tokens=int(attrs.get("input_tokens") or 0),
                output_tokens=int(attrs.get("output_tokens") or 0),
                cost_usd=float(attrs.get("cost_usd") or 0),
                tool_name=attrs.get("tool_name"),
                success=attrs.get("success") == "true",
                duration_ms=int(attrs.get("duration_ms") or 0)
            )
            session.add(e)
session.commit()
print("Events loaded.")
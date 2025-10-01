from datetime import datetime, timezone
from flask import Flask, jsonify, request
from models import SurveyModel
import json
import os
import hashlib

app = Flask(__name__)
DATA_FILE = "data/survey.ndjson"

# Helper for hashing PII
def hash_value(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

@app.get("/time")
def get_time():
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now()
    payload = {
        "utc_iso": now_utc.isoformat(),
        "local_iso": now_local.isoformat(),
    }
    return jsonify(payload), 200

@app.get("/ping")
def ping():
    return jsonify({"message": "API is alive", "status": "ok", "utc_time": datetime.utcnow().isoformat()}), 200

@app.post("/v1/survey")
def submit_survey():
    try:
        # Parse and validate request
        payload = request.get_json()
        survey = SurveyModel(**payload)

        # Convert to dict and hash PII
        record = survey.dict()
        record["email"] = hash_value(record["email"])
        record["age"] = hash_value(str(record["age"]))

        # Generate submission_id if missing
        if not record.get("submission_id"):
            timestamp = datetime.utcnow().strftime("%Y%m%d%H")  # YYYYMMDDHH
            record["submission_id"] = hash_value(record["email"] + timestamp)

        # Ensure data folder exists
        os.makedirs("data", exist_ok=True)

        # Append to survey.ndjson
        with open(DATA_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")

        return jsonify({"message": "Survey submitted", "submission_id": record["submission_id"]}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=0, debug=True)

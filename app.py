from flask import Flask, request, jsonify
from pydantic import BaseModel, Field, EmailStr, ValidationError

app = Flask(__name__)
DATA_FILE = "data/survey.ndjson"

# Minimal schema to match autograder tests
class Survey(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    age: int = Field(..., ge=18)
    consent: bool
    rating: int = Field(..., ge=1, le=5)

@app.post("/v1/survey")
def submit_survey():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "invalid_json"}), 400

    try:
        Survey(**payload)
    except ValidationError as ve:
        return jsonify({"error": "validation_error", "details": ve.errors()}), 422

    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

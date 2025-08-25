import os

DATA_PATH = os.path.join("data")
RAW_DATA_PATH = os.path.join(DATA_PATH, "raw", "admission.csv")
PROCESSED_DATA_DIR = os.path.join(DATA_PATH, "processed")
SCALER_PATH = os.path.join("models", "scaler.joblib")

PROCESSED_DATA_DIR = os.path.join("data", "processed")
MODEL_NAME = "student_admission"

MODEL_TAG = f"{MODEL_NAME}:latest"
JWT_SECRET = "your_jwt_secret_key_here"
JWT_ALGO = "HS256"
JWT_TTL_SECONDS = 3600

USERS = {"user123": "password123", "user456": "password456"}

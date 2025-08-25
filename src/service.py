import asyncio
from typing import Optional
import time
import numpy as np
import bentoml
from pydantic import BaseModel, Field
import jwt
import pandas as pd
import joblib

from src.constants import (
    MODEL_TAG,
    SCALER_PATH,
    USERS,
    JWT_ALGO,
    JWT_SECRET,
    JWT_TTL_SECONDS,
)


class LoginModel(BaseModel):
    username: str
    password: str


class InputModel(BaseModel):
    university_rating: float = Field(
        description="Note de l'université (notée sur 5)", ge=0, le=5
    )
    sop: float = Field(description="Statement of Purpose (noté sur 5)", ge=0, le=5)
    lor: float = Field(description="Letter of Recommendation (noté sur 5)", ge=0, le=5)
    cgpa: float = Field(
        description="Cumulative Grade Point Average (noté sur 10)", ge=0, le=10
    )
    research: bool = Field(description="Expérience de recherche")

    def to_numpy_array(self):
        return pd.DataFrame(
            {
                "University Rating": [self.university_rating],
                "SOP": [self.sop],
                "LOR": [self.lor],
                "CGPA": [self.cgpa],
                "Research": [self.research],
            }
        ).to_numpy()


@bentoml.service(name="pons_student_admission")
class StudentAdmissionService:
    _model = bentoml.models.BentoModel(MODEL_TAG)

    def __init__(self) -> None:
        self.model = bentoml.sklearn.load_model(self._model)
        self.scaler = joblib.load(SCALER_PATH)

    @bentoml.api(route="/login")
    def login(self, credentials: LoginModel, ctx: bentoml.Context) -> dict:
        if not (
            credentials.username in USERS.keys()
            and credentials.password in USERS.values()
            and USERS[credentials.username] == credentials.password
        ):
            ctx.response.status_code = 401
            return {"detail": "Invalid credentials"}
        payload = {
            "sub": credentials.username,
            "exp": int(time.time()) + JWT_TTL_SECONDS,
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": JWT_TTL_SECONDS,
        }

    def _require_jwt(self, ctx: bentoml.Context) -> Optional[dict]:
        # Read request headers from Context
        auth = ctx.request.headers.get("authorization")
        if not auth or not auth.lower().startswith("bearer "):
            ctx.response.status_code = 401
            return {"error": "Missing or malformed Authorization header"}
        token = auth.split(" ", 1)[1].strip()
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        except jwt.ExpiredSignatureError:
            ctx.response.status_code = 401
            return {"error": "Token expired"}
        except jwt.PyJWTError:
            ctx.response.status_code = 401
            return {"error": "Invalid token"}

    @bentoml.api(route="/predict")
    async def predict(self, input_data: InputModel, ctx: bentoml.Context) -> dict:
        claims = self._require_jwt(ctx)
        if isinstance(claims, dict) and "error" in claims:
            # _require_jwt already set status = 401
            return {"detail": claims["error"]}

        # Convert the input data to a numpy array and scale them
        input_series = input_data.to_numpy_array()
        input_series = self.scaler.transform(input_series)

        preds = await asyncio.to_thread(self.model.predict, input_series.reshape(1, -1))

        return {
            "prediction": preds.tolist()[0],
            "user": (
                ctx.request.stat.user if hasattr(ctx.request.state, "user") else None
            ),
        }

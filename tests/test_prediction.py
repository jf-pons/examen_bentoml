import pytest
import requests
from tests.constants import PREDICT_URL


class TestPrediction:
    """
    Vérifiez que l'API renvoie une erreur 401 si le jeton JWT est manquant ou invalide.
    Vérifiez que l'API renvoie une prédiction valide pour des données d'entrée correctes.
    Vérifiez que l'API renvoie une erreur pour des données d'entrée invalides.
    """

    def test_succesful_prediction(self, token, input_data):
        response = requests.post(
            PREDICT_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json=input_data,
            timeout=20,
        )

        assert response.status_code == 200
        assert "prediction" in response.json()

        prediction = response.json()["prediction"]
        assert prediction >= 0 and prediction <= 10

    @pytest.mark.parametrize(
        "data",
        [
            {
                "university_rating": 5.1,  # Too high
                "sop": 1,
                "lor": 4.5,
                "cgpa": 9.5,
                "research": True,
            },
            {
                "university_rating": -0.1,  # Too low
                "sop": 1,
                "lor": 4.5,
                "cgpa": 9.5,
                "research": True,
            },
            {
                "university_rating": 3,
                "sop": 6,  # Too high
                "lor": 4.5,
                "cgpa": 9.5,
                "research": True,
            },
            {
                "university_rating": 3,
                "sop": -1,  # Too low
                "lor": 4.5,
                "cgpa": 9.5,
                "research": True,
            },
            {
                "university_rating": 3,
                "sop": 1,
                "lor": 10,  # Too high
                "cgpa": 9.5,
                "research": True,
            },
            {
                "university_rating": 3,
                "sop": 1,
                "lor": -4.5,  # Too low
                "cgpa": 9.5,
                "research": True,
            },
            {
                "university_rating": 3,
                "sop": 1,
                "lor": 4.5,
                "cgpa": 10.1,  # Too high
                "research": True,
            },
            {
                "university_rating": 3,
                "sop": 1,
                "lor": 4.5,
                "cgpa": -0.5,  # Too low
                "research": True,
            },
            {
                "university_rating": 3,
                "sop": 1,
                "lor": 4.5,
                "cgpa": 9.5,
                "research": 3,  # Wrong type
            },
            {
                "university_rating": "True",  # Wrong type
                "sop": 1,
                "lor": 4.5,
                "cgpa": 9.5,
                "research": True,
            },
            {
                "university_rating": 3,
                "sop": "False",  # Wrong type
                "lor": 4.5,
                "cgpa": 9.5,
                "research": True,
            },
            {
                "university_rating": 3,
                "sop": 3.0,
                "lor": "4.5z",
                "cgpa": 9.5,
                "research": True,
            },
            {
                "university_rating": 3,
                "sop": 3.0,
                "lor": 4.5,
                "cgpa": "9.5%",
                "research": True,
            },
        ],
    )
    def test_failed_prediction(self, token, data):
        input_data = {"input_data": data}
        response = requests.post(
            PREDICT_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json=input_data,
            timeout=20,
        )

        assert response.status_code == 400

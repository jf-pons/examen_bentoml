import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
import bentoml

from src.constants import PROCESSED_DATA_DIR, MODEL_NAME


def load_data(dir_path: str):
    X_train = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "X_train.csv"))
    X_test = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "X_test.csv"))
    y_train = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "y_train.csv"))
    y_test = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "y_test.csv"))

    return X_train, X_test, y_train, y_test


def train_model(
    X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series
):
    model = RandomForestRegressor(
        n_estimators=100, criterion="squared_error", max_depth=10
    )

    model.fit(X_train, y_train)

    print(
        f"RMSE on validation set: {root_mean_squared_error(y_test, model.predict(X_test))}"
    )

    return model


def save_model(model, name: str):
    model_ref = bentoml.sklearn.save_model(name, model)

    print(f"Modèle enregistré sous : {model_ref}")

    # Check the model was correctly stored
    bentoml.sklearn.load_model(model_ref)


def main(
    processed_data_directory_path: str = PROCESSED_DATA_DIR,
):
    X_train, X_test, y_train, y_test = load_data(dir_path=processed_data_directory_path)

    model = train_model(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)

    save_model(model=model, name=MODEL_NAME)


if __name__ == "__main__":
    main()

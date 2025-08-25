import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = os.path.join("data")
RAW_DATA_PATH = os.path.join(DATA_PATH, "raw", "admission.csv")
PROCESSED_DATA_DIR = os.path.join(DATA_PATH, "processed")


def load_data(file_path: str):
    df = pd.read_csv(file_path, index_col=0)
    print(df.head())
    features = df.drop(columns=["Chance of Admit "])
    target = df["Chance of Admit "]
    return features, target


def remove_correlated_features(
    features: pd.DataFrame, threshold: float, features_to_keep=["CGPA"]
):
    # Note: Here we decided to drop features that are too much correlated together.
    # We could also have decided to drop features that are not enough correlated to the
    # target variable, but we did not implemented it.

    NB_FEATURES = features.shape[1]
    FEATURE_NAMES = features.columns

    corr = features.corr(method="pearson")
    print(f"Features correlation matrix:\n{corr}")

    features_to_drop = []
    for i in range(NB_FEATURES):
        for j in range(NB_FEATURES):
            # We could have used range(i + 1, NB_FEATURES) but since we need to keep some features through
            # `features_to_keep`, we loop over all features to be sure to filter them properly
            if (
                i != j
                and corr.iloc[i, j] >= threshold
                and FEATURE_NAMES[j] not in features_to_keep
                and FEATURE_NAMES[j] not in features_to_drop
            ):
                features_to_drop.append(FEATURE_NAMES[j])

    features.drop(columns=features_to_drop, inplace=True)
    print(f"Features kept: {features.columns}")

    return features


def split_data(features: pd.DataFrame, target: pd.Series, test_size: float):
    return train_test_split(features, target, test_size=test_size)


def normalize_features(X_train: pd.DataFrame, X_test: pd.DataFrame):
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)
    return X_train, X_test


def store_data(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    include_index: bool = False,
):
    X_train.to_csv(os.path.join(PROCESSED_DATA_DIR, "X_train.csv"), index=include_index)
    X_test.to_csv(os.path.join(PROCESSED_DATA_DIR, "X_test.csv"), index=include_index)
    y_train.to_csv(os.path.join(PROCESSED_DATA_DIR, "y_train.csv"), index=include_index)
    y_test.to_csv(os.path.join(PROCESSED_DATA_DIR, "y_test.csv"), index=include_index)


def main(
    raw_data_file_path: str = RAW_DATA_PATH,
    correlation_threshold: float = 0.8,
    test_size: float = 0.2,
):
    features, target = load_data(file_path=raw_data_file_path)

    features = remove_correlated_features(
        features=features, threshold=correlation_threshold
    )

    X_train, X_test, y_train, y_test = split_data(
        features=features, target=target, test_size=test_size
    )

    X_train, X_test = normalize_features(X_train=X_train, X_test=X_test)
    store_data(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)


if __name__ == "__main__":
    main()

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error


# ==============================
# LOAD DATASET
# ==============================

data = pd.read_csv("guzo_dataset.csv")


# ==============================
# CHECK REQUIRED COLUMNS
# ==============================

required_columns = [
    "distance_km",
    "traffic_level",
    "hour",
    "passenger_count",
    "eta_min"
]

missing_columns = [
    column for column in required_columns
    if column not in data.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns in dataset: {missing_columns}"
    )


# ==============================
# INPUT FEATURES
# ==============================

X = data[
    [
        "distance_km",
        "traffic_level",
        "hour",
        "passenger_count"
    ]
]


# ==============================
# TARGET
# ==============================

y = data["eta_min"]


# ==============================
# SPLIT DATA
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==============================
# TRAIN ETA MODEL
# ==============================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)


# ==============================
# TEST MODEL
# ==============================

predictions = model.predict(X_test)

r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)


# ==============================
# SAVE MODEL
# ==============================

joblib.dump(model, "eta_model.pkl")


# ==============================
# RESULTS
# ==============================

print("ETA model trained successfully!")
print(f"R² Score: {r2:.2f}")
print(f"Mean Absolute Error: {mae:.2f} minutes")
print("Saved as: eta_model.pkl")

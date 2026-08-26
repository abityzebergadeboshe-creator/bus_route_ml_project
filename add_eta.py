import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# Load dataset
data = pd.read_csv("guzo_dataset.csv")

# Input features
X = data[[
    "distance_km",
    "traffic_level",
    "hour",
    "passenger_count"
]]

# Target
y = data["eta_min"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Test model
predictions = model.predict(X_test)

r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)

# Save model
joblib.dump(model, "eta_model.pkl")

print("ETA model trained successfully!")
print(f"R² Score: {r2:.2f}")
print(f"Mean Absolute Error: {mae:.2f} minutes")
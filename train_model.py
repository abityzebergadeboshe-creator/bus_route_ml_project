import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# Load dataset
data = pd.read_csv("guzo_dataset.csv")

# Input features
X = data[[
    "distance_km",
    "duration_min",
    "traffic_level",
    "hour",
    "passenger_count"
]]

# Target
y = data["fare"]

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

# Test accuracy
predictions = model.predict(X_test)
score = r2_score(y_test, predictions)

# Save model
joblib.dump(model, "model.pkl")

print("Model trained successfully!")
print(f"R² Score: {score:.2f}")
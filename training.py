import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# -----------------------------
# Load dataset
# -----------------------------

df = pd.read_csv(r"C:\Users\agarw\OneDrive\Desktop\Infosys\data\visa_encoded.csv")

print("Dataset shape:", df.shape)


# -----------------------------
# Target variable
# -----------------------------

y = df["processing_time"]


# -----------------------------
# Remove leakage columns
# (because processing_time was derived from them)
# -----------------------------

X = df.drop(
    ["processing_time", "CASE_STATUS", "Wage_Category_Low",
     "Wage_Category_Medium", "Wage_Category_High",
     "Wage_Category_Very High"],
    axis=1,
    errors="ignore"
)


# -----------------------------
# Train Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


# =====================================
# Model 1 : Linear Regression
# =====================================

lr = LinearRegression()

lr.fit(X_train, y_train)

lr_pred = lr.predict(X_test)

lr_mae = mean_absolute_error(y_test, lr_pred)
lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))

print("\n----- Linear Regression -----")
print("MAE :", lr_mae)
print("RMSE:", lr_rmse)


# =====================================
# Model 2 : Random Forest
# =====================================

rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)

rf_mae = mean_absolute_error(y_test, rf_pred)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))

print("\n----- Random Forest -----")
print("MAE :", rf_mae)
print("RMSE:", rf_rmse)


# =====================================
# Model Comparison
# =====================================

print("\n----- Model Comparison -----")

if rf_rmse < lr_rmse:
    print("Random Forest performs better")
    best_model = rf
else:
    print("Linear Regression performs better")
    best_model = lr


# =====================================
# Fine Tune Random Forest
# =====================================

rf_tuned = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

rf_tuned.fit(X_train, y_train)

tuned_pred = rf_tuned.predict(X_test)

tuned_mae = mean_absolute_error(y_test, tuned_pred)
tuned_rmse = np.sqrt(mean_squared_error(y_test, tuned_pred))

print("\n----- Tuned Random Forest -----")
print("MAE :", tuned_mae)
print("RMSE:", tuned_rmse)


# =====================================
# Save Model
# =====================================

model_dir = r"C:\Users\agarw\OneDrive\Desktop\Infosys\models"

os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, "visa_model.pkl")

joblib.dump(rf_tuned, model_path)

print("\nModel saved at:", model_path)

print("\nMilestone 3 Completed Successfully!")
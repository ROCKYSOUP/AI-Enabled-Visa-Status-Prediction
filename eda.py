import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10,6)

# ---------------- LOAD CLEAN DATA ----------------
df = pd.read_csv(r"C:\Users\agarw\OneDrive\Desktop\Infosys\data\visa_cleaned.csv")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print(df.head())

# =========================================================
# 1. PROCESSING TIME DISTRIBUTION
# =========================================================

plt.figure()
sns.histplot(df["processing_time"], bins=30, kde=True)
plt.title("Distribution of Visa Processing Time")
plt.xlabel("Processing Time (Days)")
plt.ylabel("Number of Applications")
plt.show()

# Approved vs Rejected
plt.figure()
sns.boxplot(x="CASE_STATUS", y="processing_time", data=df)
plt.xticks([0,1],["Denied","Certified"])
plt.title("Processing Time vs Visa Decision")
plt.show()


# =========================================================
# 2. REGION ANALYSIS (STATE)
# =========================================================

top_states = df["State"].value_counts().head(10)

plt.figure()
top_states.plot(kind="bar")
plt.title("Top 10 States by Visa Applications")
plt.ylabel("Applications")
plt.xlabel("State")
plt.show()

# Avg processing time by state
avg_state_time = df.groupby("State")["processing_time"].mean().sort_values(ascending=False).head(10)

plt.figure()
avg_state_time.plot(kind="bar")
plt.title("Average Processing Time by State")
plt.ylabel("Days")
plt.xlabel("State")
plt.show()


# =========================================================
# 3. WORKLOAD & YEAR TREND
# =========================================================

# Applications per year
applications_year = df["YEAR"].value_counts().sort_index()

plt.figure()
applications_year.plot(marker="o")
plt.title("Number of Visa Applications per Year (Workload)")
plt.xlabel("Year")
plt.ylabel("Applications")
plt.show()

# Processing time trend
year_processing = df.groupby("YEAR")["processing_time"].mean()

plt.figure()
year_processing.plot(marker="o")
plt.title("Average Processing Time Over Years")
plt.xlabel("Year")
plt.ylabel("Processing Time")
plt.show()

# Workload vs processing time
combined = pd.DataFrame({
    "applications": applications_year,
    "processing": year_processing
})

plt.figure()
sns.scatterplot(x="applications", y="processing", data=combined)
plt.title("Workload vs Processing Time")
plt.xlabel("Applications")
plt.ylabel("Processing Time")
plt.show()


# =========================================================
# 4. FEATURE IMPORTANCE (VERY IMPORTANT)
# =========================================================

encoded = pd.read_csv(r"C:\Users\agarw\OneDrive\Desktop\Infosys\data\visa_encoded.csv")

X = encoded.drop("CASE_STATUS", axis=1)
y = encoded["CASE_STATUS"]

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

importances = pd.Series(model.feature_importances_, index=X.columns)
top_features = importances.sort_values(ascending=False).head(15)

plt.figure()
top_features.plot(kind="barh")
plt.title("Top Features Affecting Visa Approval")
plt.xlabel("Importance Score")
plt.show()

print("Milestone 2 (EDA) Completed Successfully!")
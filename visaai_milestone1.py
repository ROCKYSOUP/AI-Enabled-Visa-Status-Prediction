import pandas as pd

df = pd.read_csv("/content/h1b_kaggle.csv", low_memory=False)
df = df.head(100000)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
df.head()

df = df[[
    "CASE_STATUS",
    "SOC_NAME",
    "JOB_TITLE",
    "FULL_TIME_POSITION",
    "PREVAILING_WAGE",
    "YEAR",
    "WORKSITE"
]]

df.head()

df.isnull().sum()

df["PREVAILING_WAGE"] = df["PREVAILING_WAGE"].fillna(df["PREVAILING_WAGE"].median())

df["SOC_NAME"] = df["SOC_NAME"].fillna("Unknown")
df["JOB_TITLE"] = df["JOB_TITLE"].fillna("Unknown")
df["WORKSITE"] = df["WORKSITE"].fillna("Unknown")
df["FULL_TIME_POSITION"] = df["FULL_TIME_POSITION"].fillna("Y")

df = df[df["CASE_STATUS"].isin(["CERTIFIED","DENIED"])]

df["State"] = df["WORKSITE"].apply(lambda x: x.split(",")[-1].strip())

df["Wage_Category"] = pd.cut(
    df["PREVAILING_WAGE"],
    bins=[0,50000,90000,150000,1000000],
    labels=["Low","Medium","High","Very High"]
)

def processing_time(row):
    base = 30

    if row["CASE_STATUS"] == "DENIED":
        base += 25
    else:
        base -= 5

    if row["Wage_Category"] == "Low":
        base += 10
    elif row["Wage_Category"] == "High":
        base -= 5

    if row["YEAR"] <= 2014:
        base += 5

    return base

df["processing_time"] = df.apply(processing_time, axis=1)

df["CASE_STATUS"] = df["CASE_STATUS"].map({
    "CERTIFIED":1,
    "DENIED":0
})

df_encoded = pd.get_dummies(df, columns=[
    "State",
    "SOC_NAME",
    "Wage_Category",
    "FULL_TIME_POSITION"
])

df_encoded.to_csv("visa_encoded.csv", index=False)
print("Milestone 1 Completed Successfully!")

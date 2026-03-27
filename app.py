from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
from datetime import datetime, timedelta

app = Flask(__name__)

# ── Load model & data ──
model = joblib.load(r"C:\Users\agarw\OneDrive\Desktop\Infosys\models\visa_model.pkl")
model_columns = model.feature_names_in_
df = pd.read_csv(r"C:\Users\agarw\OneDrive\Desktop\Infosys\data\visa_cleaned.csv")

STATE_LIST = sorted(df["State"].dropna().unique().tolist())
SOC_LIST   = sorted(df["SOC_NAME"].dropna().unique().tolist())

# ── Stats for hero section ──
AVG_DAYS       = int(df["processing_time"].mean()) if "processing_time" in df.columns else 0
TOTAL_RECORDS  = f"{len(df):,}"
STATES_COVERED = int(df["State"].nunique())


def preprocess_input(data):
    df_input = pd.DataFrame([data])
    df_input["Wage_Category"] = pd.cut(
        df_input["PREVAILING_WAGE"],
        bins=[0, 50000, 90000, 150000, 1_000_000],
        labels=["Low", "Medium", "High", "Very High"]
    )
    df_input = pd.get_dummies(df_input)
    for col in model_columns:
        if col not in df_input.columns:
            df_input[col] = 0
    return df_input[model_columns]


@app.route("/")
def index():
    return render_template(
        "index.html",
        states=STATE_LIST,
        occupations=SOC_LIST,
        avg_days=AVG_DAYS,
        total_records=TOTAL_RECORDS,
        states_covered=STATES_COVERED,
    )


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        wage             = float(data["wage"])
        state            = data["state"]
        occupation       = data["occupation"]
        application_date = datetime.strptime(data["application_date"], "%Y-%m-%d")

        input_data = {
            "PREVAILING_WAGE":   wage,
            "YEAR":              application_date.year,
            "FULL_TIME_POSITION": "Y",
            "State":             state,
            "SOC_NAME":          occupation,
        }

        days            = int(model.predict(preprocess_input(input_data))[0])
        completion_date = application_date + timedelta(days=days)
        weeks           = days // 7
        rem_days        = days % 7
        pct             = min(round(days / 365 * 100), 100)

        return jsonify({
            "success":        True,
            "days":           days,
            "weeks":          weeks,
            "rem_days":       rem_days,
            "pct":            pct,
            "completion":     completion_date.strftime("%b %d, %Y"),
            "start":          application_date.strftime("%b %d, %Y"),
            "state":          state,
            "occupation":     occupation[:42] + ("…" if len(occupation) > 42 else ""),
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)

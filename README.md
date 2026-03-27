# 🌍 AI-Enabled Visa Status Prediction

🔗 **Live Demo:** https://ai-enabled-visa-status-prediction-6ycn.onrender.com/

---

## 📌 Overview

AI-Enabled Visa Status Prediction is a machine learning-powered web application that predicts visa processing time based on various factors such as wage, state, occupation, and application date.

The system uses a trained machine learning model integrated with a Flask web application to provide real-time predictions through a user-friendly interface.

---

## 🚀 Features

* 🔮 Predict visa processing time (in days & weeks)
* 📅 Estimated completion date calculation
* 📊 Dynamic input handling (state, occupation, wage)
* ⚡ Fast and responsive UI
* 🌐 Fully deployed and accessible online

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask

### Machine Learning

* Scikit-learn
* XGBoost
* Pandas, NumPy

### Frontend

* HTML
* CSS
* JavaScript

### Deployment

* Render

---

## 🧠 How It Works

1. User inputs:

   * Wage
   * State
   * Occupation
   * Application Date

2. Data is preprocessed:

   * Feature engineering (Wage categories)
   * One-hot encoding

3. Model predicts:

   * Processing time (in days)

4. Output includes:

   * Total days
   * Weeks + remaining days
   * Completion date

---

## 📂 Project Structure

```
AI-Enabled-Visa-Status-Prediction/
│── app.py
│── requirements.txt
│── Procfile
│
├── models/
│   └── visa_model.pkl
│
├── data/
│   └── visa_cleaned.csv
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   └── js/
```

---

## ⚙️ Installation (Run Locally)

```bash
git clone https://github.com/ROCKYSOUP/AI-Enabled-Visa-Status-Prediction.git
cd AI-Enabled-Visa-Status-Prediction

pip install -r requirements.txt
python app.py
```

Open: http://127.0.0.1:10000/

---

## 📈 Future Improvements

* 📊 Add interactive charts and analytics
* 🤖 Improve model accuracy with more features
* 🌍 Multi-country visa predictions
* 🎨 Enhanced UI/UX design

---

## 👨‍💻 Author

**Dev Agarwal**

* 💼 B.Tech IT Student
* 🌐 Passionate about AI & Full Stack Development


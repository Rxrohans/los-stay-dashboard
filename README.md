# 📊 Hospital LOS & KPI Dashboard

A Streamlit Web Application using Publicly Available Healthcare Data
view live at [streamlit webapp] https://hospitalkpidb.streamlit.app/

# 🩺 Overview

This project is an interactive Streamlit dashboard designed to analyze hospital inpatient data—specifically:
- Length of Stay (LOS)
- Hospital Charges & Costs
- Admission Trends
- Top Diagnoses & Clinical Patterns

It uses publicly available, de-identified hospital discharge datasets and is meant purely for personal learning, analytics practice, and AI/ML experimentation.

Note: This does not contains any private or patient-identifiable information.

#  Features
# 📌 Interactive KPIs
- Total admissions
- Average length of stay
- Total charges & costs

# 📌 Drill-down Filters
- Facility
- Diagnosis (CCS)
- Admission type
- Emergency indicator

# 📌 Visualizations

Bar charts for facility-level KPIs

Pie charts for case mix distribution

Scatter analysis for LOS vs cost

Top diagnosis chart

Trend graphs (optional regression lines)

📌 Streamlit Dashboard

Clean UI

Responsive layout

Works directly on Streamlit Cloud

📂 Dataset Information

This dashboard uses publicly available, de-identified data such as:

SPARCS Hospital Inpatient Discharge Data (NY State) – 2017

Or equivalent Kaggle mirror dataset

📌 No private or sensitive patient data is used.
📌 All data is openly licensed for public use and educational analytics.
📌 The dashboard is built for personal learning, not for regulatory, clinical, or business decision-making.

# 🧑‍💻 Tech Stack and libraries

- Python 3.10+
- Streamlit
- Pandas
- NumPy
- Plotly
- Statsmodels (for trendlines)
- GitHub + Streamlit Cloud deployment

# ⚙️ Installation & Running Locally
1️⃣ Clone the repository
git clone https://github.com/rxrohans/los-stay-dashboard
cd los-stay-dashboard

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run Streamlit
streamlit run app.py


# 📸 Screenshots
loading.....

# 📌 Future Improvements
- Add predictive models (LOS prediction, cost forecasting)
- Add NLP module for diagnosis grouping
- Add ICD → CCS mapping

Add multi-year trend analysis

Add drill-down pages for each hospital

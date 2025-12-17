# IPL Dream Team Predictor 🏏

A Streamlit-based web application that predicts expected fantasy points
for IPL players and automatically selects:

- Dream Team (Top 11)
- Captain
- Vice-Captain

## Model
- CatBoost Regressor
- Uses pre-match features only
- Handles high-cardinality categorical variables safely

## Input CSV Columns
fullName, Role, venue, Against Team, batting_innings

## How to Run Locally
pip install -r requirements.txt
streamlit run app.py


## Deployment
Deployed using Streamlit Cloud.

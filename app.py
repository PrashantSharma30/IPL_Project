import streamlit as st
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor

# -----------------------------
# CONFIG
# -----------------------------
FEATURES = [
    "fullName",
    "Role",
    "venue",
    "Against Team",
    "batting_innings"
]

CAT_FEATURES = [
    "fullName",
    "Role",
    "venue",
    "Against Team"
]

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_model():
    model = CatBoostRegressor()
    model.load_model("model/catboost_model.cbm")
    return model

model = load_model()

# -----------------------------
# UI
# -----------------------------
st.title("🏏 IPL Dream Team Predictor")
st.write(
    "Upload playing XI for **both teams**. "
    "The app predicts fantasy points, Dream Team, Captain & Vice-Captain."
)

home_team = st.text_input("Home Team Name", value="MI")
away_team = st.text_input("Away Team Name", value="CSK")

uploaded_file = st.file_uploader(
    "Upload CSV with 22 players",
    type=["csv"]
)

st.markdown("""
### Required CSV Columns
- batting_innings = 1 → Home team  
- batting_innings = 2 → Away team
""")

# -----------------------------
# PREDICTION
# -----------------------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Basic validation
    missing_cols = set(FEATURES) - set(df.columns)
    if missing_cols:
        st.error(f"Missing columns: {missing_cols}")
        st.stop()

    # Predict points
    df["predicted_points"] = model.predict(df[FEATURES])

    # Assign team for output
    df["team"] = np.where(
        df["batting_innings"] == 1,
        home_team,
        away_team
    )

    # Sort & select Dream Team
    dream_team = df.sort_values(
        "predicted_points",
        ascending=False
    ).head(11).reset_index(drop=True)

    captain = dream_team.iloc[0]
    vice_captain = dream_team.iloc[1]

    # -----------------------------
    # OUTPUT
    # -----------------------------
    st.subheader("🏆 Predicted Dream Team")

    st.dataframe(
        dream_team[
            ["fullName", "Role", "team", "predicted_points"]
        ]
    )

    st.success(f"🏏 Captain: {captain['fullName']} ({captain['team']})")
    st.info(f"🥈 Vice-Captain: {vice_captain['fullName']} ({vice_captain['team']})")

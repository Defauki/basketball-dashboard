import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Basketball Team Dashboard",
    layout="centered"
)

# -----------------------------
# CSV laden
# -----------------------------
df = pd.read_csv("basketball_stats.csv")
print(df.head())

# -----------------------------
# Berechnete Stats
# -----------------------------
df["PPG"] = df["Punkte"] / df["Spiele"]
df["Effizienz_pro_Spiel"] = df["Effizienz"] / df["Spiele"]
df["Fouls_pro_Spiel"] = df["Fouls"] / df["Spiele"]
df["FT_Quote_num"] = (
    df["FT_Getroffen"] / df["FT_Versuche"].replace(0, pd.NA) * 100 
)

df["2P_Punkte"] = df["Zweier"] * 2
df["3P_Punkte"] = df["Dreier"] * 3
df["FT_Punkte"] = df["FT_Getroffen"]

# -----------------------------
# Titel
# -----------------------------
st.title("Team Dashboard")

# -----------------------------
# Tabelle
# -----------------------------
st.subheader("Spielerübersicht")
st.dataframe(
    df[[
        "Spieler", "Spiele", "PPG", "Dreier", "Effizienz_pro_Spiel",
        "Fouls_pro_Spiel", "FT_Quote_num"
    ]].round(2)
    .rename(columns={
        "PPG": "Punkte / Spiel",
        "Effizienz_pro_Spiel": "Effizienz",
        "Fouls_pro_Spiel": "Fouls / Spiel",
        "FT_Quote_num": "Freiwurfquote"
    })
    .style.format({
        "Punkte / Spiel": "{:.2f}",
        "Effizienz": "{:.2f}",
        "Fouls / Spiel": "{:.2f}",
        "Freiwurfquote": "{:.2f}%"
    })
)

# -----------------------------
# TOP Spieler
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    best_ppg = df.loc[df["PPG"].idxmax()]
    st.markdown(f"""
    <div style='background-color:#e6f2e6;  /* leichtes grün */
                padding:20px;
                border-radius:20px;
                text-align:center;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>
        <h4 style='margin:0; color:#2c6f2c;'>Top Scorer</h4>
        <h2 style='margin:5px 0; font-size:20px; color:#1b4d1b;
            position:relative; top:10px; left:15px;'>{best_ppg['Spieler']}</h2>
        <p style='font-size:16px; margin:0; color:#1b4d1b'>{best_ppg['PPG']:.2f} PPG</p>
    </div>
    """, unsafe_allow_html=True)

# --- Bester Freiwurf ---
with col2:
    best_ft = df.loc[df["FT_Quote_num"].idxmax()]
    st.markdown(f"""
    <div style='background-color:#e6f2e6;  /* leichtes grün */
                padding:20px;
                border-radius:20px;
                text-align:center;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>
        <h4 style='margin:0; color:#2c6f2c;'>Bester Freiwerfer</h4>
        <h2 style='margin:5px 0; font-size:20px; color:#1b4d1b;
            position:relative; top:10px; left:15px;'>{best_ft['Spieler']}</h2>
        <p style='font-size:16px; margin:0; color:#1b4d1b'>{best_ft['FT_Quote_num']:.2f}%</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Effizienz pro Spiel
# -----------------------------
st.subheader("Effizienz pro Spiel")
st.metric("Effizienz pro Spiel (Team)", f"{df['Effizienz_pro_Spiel'].mean():.2f}")



# -----------------------------
# Team Punkteverteilung
# -----------------------------
st.subheader("Scoring Verteilung")

team_points = [
    df["2P_Punkte"].sum(),
    df["3P_Punkte"].sum(),
    df["FT_Punkte"].sum()
]

labels = ["2P", "3P", "FT"]

st.table(
    pd.DataFrame({
        "Punktequelle": labels,
        "Punkte": team_points
    })
)

# -----------------------------
# Freiwurfquote pro Spieler
# -----------------------------
st.subheader("Freiwurfquote pro Spieler")
df_sorted = df.sort_values(
    by="FT_Quote_num",
    ascending=False
)

st.table(
    df_sorted[["Spieler", "FT_Quote_num"]]
        .rename(columns={"FT_Quote_num": "Freiwurfquote (%)"})
        .style.format({"Freiwurfquote (%)": "{:.2f}%"})
)


#--------------------------------
# Dreier pro Spiel
#-------------------------------
df["3P_pro_Spiel"] = df["Dreier"] / df["Spiele"]
st.subheader("Dreier pro Spiel")
df_sorted = df.sort_values(
    by="3P_pro_Spiel",
    ascending=False
)

st.table(
    df_sorted[["Spieler", "3P_pro_Spiel"]]
        .rename(columns={"3P_pro_Spiel": "Dreier pro Spiel"})
        .style.format({"Dreier pro Spiel": "{:.2f}"})
)



top5 = df.sort_values(by="Effizienz_pro_Spiel", ascending=False).head(5)

st.subheader("Effektivsten 5 Spieler")
st.table(
    top5[["Spieler", "Effizienz_pro_Spiel"]]
        .rename(columns={"Effizienz_pro_Spiel": "Effizienz pro Spiel"})
    .style.format({"Effizienz pro Spiel": "{:.2f}"})
)
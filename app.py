import pandas as pd
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="IPL 2025 Data Analysis", layout="wide")

st.title("🏏 IPL 2025 Data Analysis")

# ---------------- LOAD DATA ----------------
bat = pd.read_csv("IPL2025Batters.csv")
bowl = pd.read_csv("IPL2025Bowlers.csv")

# ---------------- CLEAN DATA ----------------
bat.drop_duplicates(inplace=True)
bowl.drop_duplicates(inplace=True)

# ---------------- SIDEBAR ----------------
option = st.sidebar.radio(
    "📊 Select Analysis",
    ["Home", "Top Batters", "Top Bowlers", "Batting Strike Rate", "Bowling Strike Rate"]
)

# ================= HOME =================
if option == "Home":
    st.title("🏏 IPL 2025 Dashboard Overview")

    # KPI CARDS
    col1, col2, col3 = st.columns(3)

    total_players = bat['Player Name'].nunique()
    total_runs = bat['Runs'].sum()
    total_wickets = bowl['WKT'].sum()

    col1.metric("👤 Total Players", total_players)
    col2.metric("🏏 Total Runs", total_runs)
    col3.metric("🎯 Total Wickets", total_wickets)

    st.markdown("---")

    # TOP PERFORMERS
    col1, col2 = st.columns(2)

    top_batsman = bat.sort_values(by='Runs', ascending=False).iloc[0]
    col1.subheader("🔥 Top Batsman")
    col1.write(f"**{top_batsman['Player Name']}**")
    col1.write(f"Runs: {top_batsman['Runs']}")
    col1.write(f"Strike Rate: {top_batsman['SR']}")

    top_bowler = bowl.sort_values(by='WKT', ascending=False).iloc[0]
    col2.subheader("🎯 Top Bowler")
    col2.write(f"**{top_bowler['Player Name']}**")
    col2.write(f"Wickets: {top_bowler['WKT']}")
    col2.write(f"Economy: {top_bowler['ECO']}")

    st.markdown("---")

    # QUICK CHART
    st.subheader("📊 Top 5 Run Scorers")
    top5 = bat.sort_values(by='Runs', ascending=False).head(5)
    st.bar_chart(top5.set_index("Player Name")["Runs"])


# ================= TOP BATTERS =================
elif option == "Top Batters":
    st.subheader("Top 10 Batters by Runs")

    top_scorer = bat.sort_values(by='Runs', ascending=False).head(10)
    st.dataframe(top_scorer[['Player Name', 'Runs', 'SR']])
    st.bar_chart(top_scorer.set_index("Player Name")["Runs"])


# ================= TOP BOWLERS =================
elif option == "Top Bowlers":
    st.subheader("Top 10 Bowlers by Wickets")

    top_wicket = bowl.sort_values(by="WKT", ascending=False).head(10)
    st.dataframe(top_wicket[['Player Name', 'WKT', 'ECO']])
    st.bar_chart(top_wicket.set_index("Player Name")["WKT"])


# ================= BATTING STRIKE RATE =================
elif option == "Batting Strike Rate":
    st.subheader("Top 10 Batting Strike Rate (Min 10 Innings)")

    # ⚠️ Make sure column name matches your dataset (Inn / INN / Inns)
    filtered_bat = bat[bat['Inn'] >= 10]

    strike_rate = filtered_bat.sort_values(by="SR", ascending=False).head(10)

    st.dataframe(strike_rate[["Player Name", "Inn", "SR", "Runs"]])
    st.bar_chart(strike_rate.set_index("Player Name")["SR"])


# ================= BOWLING STRIKE RATE =================
elif option == "Bowling Strike Rate":
    st.subheader("Top 10 Bowling Strike Rate (Min 10 Innings & 4 Wickets)")

    filtered_bowl = bowl[(bowl['INN'] >= 10) & (bowl['WKT'] >= 4)]

    strike_rate = filtered_bowl.sort_values(by="SR", ascending=False).head(10)

    st.dataframe(strike_rate[["Player Name", "INN", "SR", "WKT"]])
    st.bar_chart(strike_rate.set_index("Player Name")["SR"])
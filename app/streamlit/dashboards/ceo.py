import streamlit as st
import requests
import pandas as pd

API = "http://backend:8000"

def ceo_dashboard():
    st.sidebar.title("👑 CEO Panel")
    st.title("🏆 Team Rankings")

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    res = requests.get(f"{API}/ceo/team-performance", headers=headers)
    teams = res.json()

    df = pd.DataFrame(teams)
    df["performance_%"] = (df["tasks_reached"] / df["total_tasks"]) * 100

    st.dataframe(df.sort_values("performance_%", ascending=False))

    if st.button("⬇ Download Report"):
        export = requests.get(
            f"{API}/ceo/export-data",
            headers=headers
        )
        st.download_button(
            "Download CSV",
            export.text,
            file_name="sales_report.csv"
        )

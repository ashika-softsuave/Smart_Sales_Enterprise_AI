import streamlit as st
import requests
from components.charts import sales_table, bar_chart

API = "http://backend:8000"

def manager_dashboard():
    st.sidebar.title("👨‍💼 Manager Panel")
    st.title("📊 Team Performance")

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    res = requests.get(f"{API}/manager/salesmen", headers=headers)
    salesmen = res.json()

    st.subheader("Salesmen Overview")
    sales_table(salesmen)

    st.subheader("Target vs Achieved")
    bar_chart(
        salesmen,
        x="name",
        y="tasks_reached"
    )




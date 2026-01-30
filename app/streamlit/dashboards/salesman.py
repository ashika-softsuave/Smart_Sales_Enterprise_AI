import streamlit as st
from api_client import get_daily_task
from components.map_view import render_map

def salesman_dashboard():
    st.sidebar.title("👤 Salesman")
    st.title("📍 Today's Task")

    if st.button("Get Today's Task"):
        task = get_daily_task(st.session_state.token)

        st.metric("🎯 Target", task["assigned_target"])
        st.metric("🟢 Completed", task["tasks_reached"])
        st.metric("🔴 Pending", task["tasks_pending"])

        st.subheader("🛣️ Optimized Route")
        render_map(task["route_assigned"]["polyline"])
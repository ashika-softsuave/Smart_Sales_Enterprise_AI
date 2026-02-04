import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ================== CONFIG ==================
BASE_URL = "http://127.0.0.1:8000"
# -------- CHAT BUBBLE HELPER (PASTE HERE) --------
def chat_bubble(message, sender="ai"):
    if sender == "user":
        st.markdown(
            f"""
            <div style="text-align:right; padding:10px; margin:6px;
                        background-color:#DCF8C6; border-radius:10px;">
                🧑 {message}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="text-align:left; padding:10px; margin:6px;
                        background-color:#F1F0F0; border-radius:10px;">
                🤖 {message}
            </div>
            """,
            unsafe_allow_html=True
        )


st.set_page_config(
    page_title="Smart Sales Enterprise System",
    layout="wide",
    page_icon="📊"
)

# ================== SESSION STATE ==================
if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.user = None
    st.session_state.chat_history = []

# ================== API HELPERS ==================
def api_post(endpoint, payload):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }
    return requests.post(
        f"{BASE_URL}{endpoint}",
        json=payload,
        headers=headers,
        timeout=20
    )


def api_get(endpoint):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }
    return requests.get(
        f"{BASE_URL}{endpoint}",
        headers=headers,
        timeout=20
    )

# ================== LOGIN ==================
def login_ui():
    st.title("🔐 Smart Sales Login")

    col1, col2 = st.columns([2, 1])

    with col1:
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login"):
            res = requests.post(
                f"{BASE_URL}/auth/login",
                json={"email": email, "password": password}
            )

            if res.status_code == 200:
                data = res.json()

                st.session_state.token = data["access_token"]
                st.session_state.role = data.get("role")

                # ✅ SAFE FIX (no KeyError)
                st.session_state.user = data.get("name") or data.get("email")

                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

    with col2:
        st.info(
            """
            **Demo Commands (Salesman):**
            - What is my task today?
            - Guindy Chennai
            - I have 3 pending items
            - I am done for today
            """
        )


# ================== SALESMAN UI ==================
def salesman_ui():
    st.title(f"🧑‍💼 Salesman Dashboard")

    # ---------- SESSION STATE ----------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    tab1, tab2 = st.tabs(["💬 AI Assistant", "📊 My Performance"])

    # ---------- SIDEBAR (SUMMARY ONLY) ----------
    with st.sidebar:
        st.header("🕘 Conversation Summary")

        for sender, text in st.session_state.chat_history[-6:]:
            icon = "🧑" if sender == "You" else "🤖"
            st.write(f"{icon} {text[:35]}...")

        st.divider()

        if st.button("🧹 Clear History", key="clear_history"):
            st.session_state.chat_history = []
            st.rerun()

        st.button(
            "🚪 Logout",
            key="logout_btn",
            on_click=lambda: st.session_state.clear()
        )

    # ---------- CHAT TAB ----------
    with tab1:
        st.subheader("💬 Chat with Sales AI")

        # Render full chat flow (CENTER)
        for sender, text in st.session_state.chat_history:
            chat_bubble(text, "user" if sender == "You" else "ai")

        st.divider()

        msg = st.text_input("Type your message", key="chat_input")

        if st.button("Send", key="send_btn"):
            if not msg.strip():
                st.warning("Type something first")
            else:
                res = api_post("/chat", {"message": msg})

                if res.status_code == 200:
                    response = res.json()

                    # Save chat
                    st.session_state.chat_history.append(("You", msg))
                    st.session_state.chat_history.append(
                        ("AI", response.get("reply", ""))
                    )

                    # ---------- SHOW OPTIMIZED PLAN INLINE ----------
                    task_data = response.get("data")

                    if task_data:
                        st.session_state.chat_history.append(
                            ("AI", "📋 Here’s your optimized plan:")
                        )

                        if "route_assigned" in task_data:
                            for i, stop in enumerate(task_data["route_assigned"], 1):
                                st.session_state.chat_history.append(
                                    ("AI", f"{i}. 📍 {stop['location']}")
                                )

                        if "assigned_products" in task_data:
                            for p in task_data["assigned_products"]:
                                st.session_state.chat_history.append(
                                    ("AI", f"📦 {p['product']} → Target: {p['daily_target']}")
                                )

                        if "summary" in task_data:
                            st.session_state.chat_history.append(
                                (
                                    "AI",
                                    f"🚗 Distance: {task_data['summary']['distance_km']} km | "
                                    f"⏱️ {task_data['summary']['duration_minutes']} mins"
                                )
                            )

                    st.rerun()

                else:
                    st.error("Chat failed")

    # ---------- PERFORMANCE TAB ----------
    with tab2:
        st.subheader("📈 Daily Performance")

        res = api_get("/ceo/summary")
        if res.status_code == 200:
            data = res.json()

            col1, col2, col3 = st.columns(3)
            col1.metric("🎯 Total Tasks", data.get("total_tasks", 0))
            col2.metric("✅ Tasks Reached", data.get("tasks_reached", 0))
            col3.metric(
                "📊 Completion %",
                f"{(data.get('tasks_reached',0)/max(data.get('total_tasks',1),1))*100:.2f}%"
            )

# ================== MANAGER UI ==================
def manager_ui():
    st.title(f"👨‍💼 Manager Dashboard – {st.session_state.user}")

    res = api_get("/ceo/dashboard")
    if res.status_code == 200:
        df = pd.DataFrame(res.json()["leaderboard"])

        st.subheader("📋 Team Performance Table")
        st.dataframe(df)

        fig = px.bar(
            df,
            x="team_name",
            y="performance_percent",
            color="performance_percent",
            title="📊 Team Performance (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Manager dashboard data not available yet")

# ================== CEO UI ==================
def ceo_ui():
    st.title("🏢 CEO Dashboard")

    tab1, tab2, tab3 = st.tabs(
        ["📊 Company Summary", "🏆 Leaderboard", "📁 Export"]
    )

    # -------- SUMMARY --------
    with tab1:
        res = api_get("/ceo/summary")
        if res.status_code == 200:
            data = res.json()

            col1, col2, col3 = st.columns(3)
            col1.metric("🏢 Teams", data["total_teams"])
            col2.metric("🧑‍💼 Salesmen", data["total_salesmen"])
            col3.metric(
                "📈 Overall Performance",
                f"{(data['tasks_reached']/max(data['total_tasks'],1))*100:.2f}%"
            )

    # -------- LEADERBOARD --------
    with tab2:
        res = api_get("/ceo/dashboard")
        if res.status_code == 200:
            df = pd.DataFrame(res.json()["leaderboard"])
            st.dataframe(df)

            fig = px.pie(
                df,
                values="tasks_reached",
                names="team_name",
                title="🏆 Contribution by Team"
            )
            st.plotly_chart(fig, use_container_width=True)

    # -------- EXPORT --------
    with tab3:
        st.subheader("📥 Export Reports")

        if st.button("Generate CSV Export"):
            res = api_get("/ceo/export")
            if res.status_code == 200:
                files = res.json()["files"]
                st.success("Export generated successfully")
                st.write(files)
            else:
                st.error("Export failed")

# ================== MAIN ROUTER ==================
if st.session_state.token is None:
    login_ui()
else:
    role = st.session_state.role

    if role == "salesman":
        salesman_ui()
    elif role == "manager":
        manager_ui()
    elif role == "ceo":
        ceo_ui()

    st.sidebar.divider()
    st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.clear())

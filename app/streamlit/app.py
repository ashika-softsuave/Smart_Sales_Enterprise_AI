# import streamlit as st
# from api_client import login
# from dashboards.salesman import salesman_dashboard
# from dashboards.manager import manager_dashboard
# from dashboards.ceo import ceo_dashboard
#
# st.set_page_config(page_title="Sales AI Assistant", layout="wide")
#
# if "token" not in st.session_state:
#     st.session_state.token=None
#     st.session_state.role=None
#
# st.title("🔐 Sales AI Assistant Login")
#
# if not st.session_state.token:
#     email=st.text_input("Email")
#     password=st.text_input("Password", type="password")
#
#     if st.button("Login"):
#         data=login(email,password)
#         st.session_state.token=data["access_token"]
#         st.session_state.role=data["role"]
#         st.rerun()
#
# else:
#     if st.session_state.role=="salesman":
#         salesman_dashboard()
#     elif st.session_state.role=="manager":
#         manager_dashboard()
#     elif st.session_state.role"ceo":
#         ceo_dashboard()
import streamlit as st

st.set_page_config(page_title="Test Page", layout="wide")

st.title("✅ Streamlit is Working")
st.write("If you see this, rendering is fine.")
st.button("Test Button")

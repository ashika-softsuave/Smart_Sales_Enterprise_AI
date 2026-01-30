import requests
import streamlit as st

API_BASE="https://loalhost:8000"

def login(email,password):
    res=requests.post
       f"{API_BASE}/auth/login",
        json={"email":email, "password":password}
    )
    return res.json()

def get_dailt_task(token):
    return requests.post(
        f"{API_BASE}/ai/get-daily-task",
        headers={"Authorization":f"Bearer {token}"}
    ).json()
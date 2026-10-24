
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="SLEEPGUARD",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ SLEEPGUARD")
st.subheader("Smart Anti-Drowsiness Jacket for Cyclists")
st.info("DEMO MODE — values are simulated, not live sensor data.")

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.header("Sensor Simulation")

eye_closed = st.sidebar.slider(
    "Eye closure duration (seconds)", 0.0, 5.0, 0.2, 0.1
)

movement = st.sidebar.slider(
    "Head movement index", 0, 100, 12
)

if st.sidebar.button("Check Rider Status"):
    if eye_closed >= 3 or movement >= 80:
        status = "CRITICAL"
        alert = "Escalation alert simulated"
        stage = 2
    elif eye_closed >= 1.5 or movement >= 45:
        status = "WARNING"
        alert = "First-stage vibration alert simulated"
        stage = 1
    else:
        status = "NORMAL"
        alert = "No warning in this demo"
        stage = 0

    st.session_state.history.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Eye Closure (s)": eye_closed,
        "Movement Index": movement,
        "Status": status,
        "Alert Stage": stage
    })

    st.session_state.status = status
    st.session_state.alert = alert
    st.session_state.stage = stage

status = st.session_state.get("status", "NOT TESTED")
alert = st.session_state.get(
    "alert", "Move the sliders and check rider status."
)
stage = st.session_state.get("stage", 0)

a, b, c = st.columns(3)
a.metric("Rider Status", status)
b.metric("Vibration Stage", stage)
c.metric("Eye Closure", f"{eye_closed:.1f} s")

st.subheader("Movement Monitoring")
st.progress(movement / 100)
st.write(f"Movement index: {movement}/100")

if status == "CRITICAL":
    st.error(alert)
elif status == "WARNING":
    st.warning(alert)
elif status == "NORMAL":
    st.success(alert)
else:
    st.info(alert)

st.subheader("Alert History")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

    st.line_chart(
        df.set_index("Time")[["Movement Index"]]
    )
else:
    st.write("No test events yet.")

if st.button("Clear Alert History"):
    st.session_state.history = []
    st.rerun()

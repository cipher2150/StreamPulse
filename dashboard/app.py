import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

st.title("Streaming Health Dashboard")

# Fetching data
metrics = requests.get("http://127.0.0.1:5000/metrics").json()
network_data = requests.get("http://127.0.0.1:5000/network").json()

df_net = pd.DataFrame(network_data)

# Helper function to determine status
def get_status(value, good, bad):
    if value <= good:
        return "🟢 Good"
    elif value <= bad:
        return "🟡 Moderate"
    else:
        return "🔴 Critical"

# -----------------------------
# 🔝 Top Metrics Section
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Avg Bitrate",
    round(metrics["avg_bitrate"], 2),
    help="Higher bitrate = better video quality"
)

col2.metric(
    "Startup Delay",
    round(metrics["startup_delay"], 2),
    help="Time taken for video to start"
)

col3.metric(
    "Buffer Ratio",
    round(metrics["buffer_ratio"], 3),
    help="Time spent buffering vs watching"
)

col4.metric(
    "Error Rate",
    round(metrics["error_rate"], 3),
    help="Playback failures percentage"
)

# System Health Overview
st.subheader("System Health Overview")

c1, c2, c3 = st.columns(3)

c1.write(f"Buffer Health: {get_status(metrics['buffer_ratio'], 0.1, 0.3)}")
c2.write(f"Error Health: {get_status(metrics['error_rate'], 0.02, 0.05)}")
c3.write(f"Startup Health: {get_status(metrics['startup_delay'], 2, 5)}")

# Network Performance Analysis
st.subheader("📡 Network Performance Analysis")

st.bar_chart(df_net.set_index("network_type")["avg_bitrate"])

# Insights & Recommendations section
st.subheader("📉 Insights & Recommendations")

if metrics["error_rate"] > 0.05:
    st.error("High error rate detected! Possible server or playback issue.")
elif metrics["error_rate"] > 0.02:
    st.warning("Moderate errors detected. Monitor closely.")
else:
    st.success("Error rate is under control.")

if metrics["buffer_ratio"] > 0.3:
    st.error("Users are experiencing heavy buffering!")
elif metrics["buffer_ratio"] > 0.1:
    st.warning("Some buffering issues detected.")
else:
    st.success("Smooth playback experience.")

if metrics["startup_delay"] > 5:
    st.error("High startup delay! Users may leave early.")
elif metrics["startup_delay"] > 2:
    st.warning("Startup delay is moderate.")
else:
    st.success("Fast video startup time.")

# Summary
st.subheader("🧾 Overall Summary")

if (
    metrics["error_rate"] < 0.02
    and metrics["buffer_ratio"] < 0.1
    and metrics["startup_delay"] < 2
):
    st.success("System is performing optimally!")
else:
    st.warning("⚠️ System needs optimization in some areas.")
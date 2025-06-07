
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Tension Monitor - Interactive", layout="wide")
st.title("🧠 Smart Tension Monitor for Patient Transfer")

st.markdown("""
Upload a CSV file with tension data. The system will detect and highlight any abnormal tension values (less than 100N or greater than 400N),
and prompt the operator to take appropriate action.
""")

uploaded_file = st.file_uploader("📤 Upload a Tension CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Is_Anomaly'] = df['Tension(N)'].apply(lambda x: 1 if x < 100 or x > 400 else 0)

    total = len(df)
    abnormal = df['Is_Anomaly'].sum()

    st.success(f"✅ Total Records: {total}")
    st.warning(f"⚠️ Anomalies Detected: {abnormal}")

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df['Timestamp'], df['Tension(N)'], label='Tension (N)', color='blue', linewidth=2)
    ax.scatter(df[df['Is_Anomaly'] == 1]['Timestamp'],
               df[df['Is_Anomaly'] == 1]['Tension(N)'],
               color='red', label='Anomaly', zorder=5)
    ax.set_title("Tension Over Time with Anomalies")
    ax.set_xlabel("Time")
    ax.set_ylabel("Tension (N)")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("📋 Operator Confirmation Panel")

    if abnormal > 0:
        action = st.radio("Abnormal tension detected. What would you like to do?",
                          ["🔴 Pause Transfer", "⚠️ Proceed with Caution"])
        if action == "🔴 Pause Transfer":
            st.error("Transfer paused. Please inspect the sling immediately.")
        elif action == "⚠️ Proceed with Caution":
            st.success("Proceeding with caution. Stay alert.")
    else:
        st.success("🟢 All readings normal. Safe to proceed.")

else:
    st.info("Upload a CSV file to begin.")

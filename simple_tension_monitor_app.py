
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Tension Monitor", layout="wide")
st.title("🧠 Smart Tension Monitor for Patient Transfer")

st.markdown("""
Upload a CSV file with tension data. The system will detect and highlight any abnormal tension values (less than 100N or greater than 400N).
""")

# Upload CSV
uploaded_file = st.file_uploader("📤 Upload a Tension CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Add anomaly column
    df['Is_Anomaly'] = df['Tension(N)'].apply(lambda x: 1 if x < 100 or x > 400 else 0)

    # Display stats
    st.success(f"✅ Total Records: {len(df)}")
    st.warning(f"⚠️ Anomalies Detected: {df['Is_Anomaly'].sum()}")

    # Line chart with anomalies highlighted
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df['Timestamp'], df['Tension(N)'], label='Tension (N)', color='blue', linewidth=2)
    ax.scatter(df[df['Is_Anomaly'] == 1]['Timestamp'],
               df[df['Is_Anomaly'] == 1]['Tension(N)'],
               color='red', label='Anomaly', zorder=5)
    ax.set_title("Tension Over Time with Anomaly Markers")
    ax.set_xlabel("Time")
    ax.set_ylabel("Tension (N)")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45, fontsize=9)
    st.pyplot(fig)

else:
    st.info("Upload a CSV file to begin. Recommended: 'Tension_Data_75kg_150s.csv' or 'Tension_Data_75kg_150s_Smooth.csv'")

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

# Set seaborn style
sns.set(style="whitegrid")

# Streamlit app title
st.title("🛡️ CVSS & CWE Risk Prioritization Dashboard")

# File uploader for vulnerabilities JSON
uploaded_file = st.file_uploader("Upload vulnerability.json", type=["json"])

if uploaded_file is not None:
    # Load and parse JSON data
    data = json.load(uploaded_file)

    # 🩵 Fix: Convert dict-of-dicts to list of dicts
    if isinstance(data, dict):
        data = list(data.values())

    if not data:
        st.warning("Uploaded file is empty.")
    else:
        # Convert to DataFrame
        df = pd.DataFrame(data)

        if df.empty:
            st.warning("No vulnerabilities found in the file.")
        else:
            # Ensure expected columns exist
            required_cols = ['cwe_id', 'cvss_score', 'severity']
            if not all(col in df.columns for col in required_cols):
                st.error("Missing required columns in the uploaded file.")
            else:
                st.success("Vulnerabilities loaded successfully 💥")

                # Severity count plot
                st.subheader("Severity Count")
                plt.figure(figsize=(8, 4))
                sns.countplot(x='severity', data=df, palette="coolwarm")
                st.pyplot(plt.gcf())

                # CVSS Score distribution
                st.subheader("CVSS Score Distribution")
                plt.figure(figsize=(8, 4))
                sns.histplot(df['cvss_score'], kde=True, bins=10, color="teal")
                st.pyplot(plt.gcf())

                # CWE ID frequency
                st.subheader("Top CWE IDs")
                top_cwes = df['cwe_id'].value_counts().head(10)
                st.bar_chart(top_cwes)

                # High risk vulnerabilities
                high_risk = df[df['cvss_score'] >= 7]
                st.subheader("🔴 High-Risk Vulnerabilities (CVSS ≥ 7)")
                st.dataframe(high_risk)

                # Download button for filtered data
                st.download_button(
                    label="📥 Download High-Risk Vulnerabilities",
                    data=high_risk.to_csv(index=False).encode('utf-8'),
                    file_name='high_risk_vulnerabilities.csv',
                    mime='text/csv'
                )
else:
    st.info("Please upload a `vulnerabilities.json` file to continue.")

import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="SignalDesk Workflow Health Check", layout="wide")

st.title("SignalDesk Workflow Health Check 📊")
st.markdown("A lightweight analysis of AI-assisted workflow usage, focusing on what is working, what looks suspicious, and recent changes.")

@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("sample-data/product_usage_events.csv")
    
    # Clean data
    # Fix casing issues
    df['team'] = df['team'].str.capitalize()
    
    # Handle duplicates
    df = df.drop_duplicates()
    
    # Handle missing/invalid data
    df['median_confidence'] = pd.to_numeric(df['median_confidence'], errors='coerce')
    
    # Create derived metrics
    df['acceptance_rate'] = df['accepted_output'] / df['completed']
    df['flag_rate'] = df['flagged_for_review'] / df['completed']
    
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_and_clean_data()

st.sidebar.header("Filters")
selected_workflow = st.sidebar.multiselect("Select Workflows", df['workflow'].unique(), default=df['workflow'].unique())
filtered_df = df[df['workflow'].isin(selected_workflow)]

st.subheader("1. What's Working: The Aug 4th Prompt Update")
st.markdown("On **August 4th**, a new prompt version was rolled out. Let's see if it helped.")

col1, col2 = st.columns(2)
with col1:
    pre_aug4 = filtered_df[filtered_df['date'] < '2026-08-04']
    post_aug4 = filtered_df[(filtered_df['date'] >= '2026-08-04') & (filtered_df['date'] <= '2026-08-06')] # Excluding aug 7 for noise
    
    pre_acc = pre_aug4['acceptance_rate'].mean()
    post_acc = post_aug4['acceptance_rate'].mean()
    st.metric("Avg Acceptance Rate (Pre-Aug 4)", f"{pre_acc:.0%}")
    st.metric("Avg Acceptance Rate (Post-Aug 4)", f"{post_acc:.0%}", delta=f"{post_acc - pre_acc:.0%}")
with col2:
    pre_rating = pre_aug4['user_rating'].mean()
    post_rating = post_aug4['user_rating'].mean()
    st.metric("Avg User Rating (Pre-Aug 4)", f"{pre_rating:.1f}")
    st.metric("Avg User Rating (Post-Aug 4)", f"{post_rating:.1f}", delta=f"{post_rating - pre_rating:.1f}")

st.markdown("> **Conclusion**: The new prompt version appears to have slightly improved acceptance rates and user ratings across workflows.")

st.divider()

st.subheader("2. What's Suspicious: Data Anomalies & Policy Changes")
st.markdown("The data is quite noisy. Two specific anomalies stand out:")

st.markdown("### A. The Aug 7th Review Policy Change (Support Team)")
st.markdown("On **August 7th**, the Support team had a review policy change for `Reply draft`. Let's look at what happened to flags and ratings.")

reply_draft_df = df[df['workflow'] == 'Reply draft']
st.line_chart(reply_draft_df.set_index('date')[['flag_rate', 'user_rating', 'median_confidence']])
st.warning("⚠️ Notice how the `median_confidence` stayed high (0.91), but the `user_rating` tanked (2.1) and the `flag_rate` spiked. **Takeaway**: Do not trust `median_confidence` as a proxy for quality. The policy change created huge friction.")

st.markdown("### B. The Aug 5th Traffic Spike (Sales Team)")
sales_df = df[df['workflow'] == 'Lead summary']
st.bar_chart(sales_df.set_index('date')['sessions'])
st.warning("⚠️ There is a massive spike on August 5th caused by a demo account. This skews aggregate metrics heavily. **Takeaway**: Ensure demo/internal traffic is filtered out at the source before running broad analyses.")

st.divider()
st.subheader("Next Steps for the Team")
st.info("""
1. **Filter Test Data**: Implement a `is_demo_account` flag in the telemetry to filter out noise like the Aug 5th spike.
2. **Review the 'Reply draft' Policy**: The Aug 7 policy change is severely hurting user experience. Re-evaluate the strictness of the flags.
3. **Ignore Model Confidence**: Model confidence is proving to be a poor indicator of actual user satisfaction. Focus on `user_rating` and `acceptance_rate` instead.
""")

st.subheader("Raw Data Preview")
st.dataframe(filtered_df)

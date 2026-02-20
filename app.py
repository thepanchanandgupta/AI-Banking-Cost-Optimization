import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Banking Cost Simulator", layout="wide")

st.title("AI-Based Cost Optimization Model for Banks")

st.markdown("Interactive Financial Simulation for AI Customer Service Automation")

# Sidebar Inputs
st.sidebar.header("Model Assumptions")

monthly_queries = st.sidebar.number_input("Monthly Queries", value=500000)
human_cost = st.sidebar.number_input("Human Cost per Call ($)", value=4.0)
ai_cost = st.sidebar.number_input("AI Cost per Interaction ($)", value=0.8)
automation_rate = st.sidebar.slider("Automation Rate (%)", 0, 100, 60)
discount_rate = st.sidebar.slider("Discount Rate (%)", 0, 20, 10)

annual_queries = monthly_queries * 12
automation = automation_rate / 100
discount = discount_rate / 100

# Year 1 Calculations
current_annual_cost = annual_queries * human_cost
weighted_cost = (automation * ai_cost) + ((1 - automation) * human_cost)
ai_annual_cost = annual_queries * weighted_cost
annual_savings = current_annual_cost - ai_annual_cost

# 3-Year Forecast
growth_rate = 0.05
years = [1, 2, 3]
npv_values = []
query_projection = annual_queries

for year in years:
    yearly_cost = query_projection * human_cost
    yearly_ai_cost = query_projection * weighted_cost
    savings = yearly_cost - yearly_ai_cost
    npv = savings / ((1 + discount) ** year)
    npv_values.append(npv)
    query_projection *= (1 + growth_rate)

total_npv = sum(npv_values)

# Display Results
st.subheader("Financial Impact")

col1, col2, col3 = st.columns(3)

col1.metric("Current Annual Cost ($)", f"{current_annual_cost:,.0f}")
col2.metric("AI Annual Cost ($)", f"{ai_annual_cost:,.0f}")
col3.metric("Annual Savings ($)", f"{annual_savings:,.0f}")

st.subheader("3-Year NPV")
st.write(f"Total NPV: ${total_npv:,.0f}")

# Sensitivity Analysis
st.subheader("Sensitivity Analysis (Year 1)")

automation_range = np.arange(0.4, 0.9, 0.1)
savings_list = []

for a in automation_range:
    weighted = (a * ai_cost) + ((1 - a) * human_cost)
    savings_val = annual_queries * human_cost - annual_queries * weighted
    savings_list.append(savings_val)

df = pd.DataFrame({
    "Automation Rate": automation_range * 100,
    "Annual Savings ($)": savings_list
})

st.bar_chart(df.set_index("Automation Rate"))
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="💰 Finance Tracker", layout="wide")

# ---- Header ----
st.title("💰 Personal Finance Dashboard")
st.markdown("Track your income & expenses easily.")

# ---- Sidebar: User Input ----
st.sidebar.header("Add Transaction")
category = st.sidebar.selectbox("Category", ["Food", "Rent", "Salary", "Shopping", "Other"])
amount = st.sidebar.number_input("Amount", min_value=0.0, step=0.1)
type_ = st.sidebar.radio("Type", ["Income", "Expense"])
add_btn = st.sidebar.button("➕ Add")

# ---- Session Storage ----
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["Category", "Amount", "Type"])

# ---- Add Data ----
if add_btn and amount > 0:
    new_row = pd.DataFrame([[category, amount, type_]], columns=["Category", "Amount", "Type"])
    st.session_state["data"] = pd.concat([st.session_state["data"], new_row], ignore_index=True)
    st.success("Transaction added!")

data = st.session_state["data"]

# ---- Show Table ----
st.subheader("📋 Transaction History")
st.dataframe(data, use_container_width=True)

# ---- Summaries ----
if not data.empty:
    income = data[data["Type"] == "Income"]["Amount"].sum()
    expense = data[data["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense

    st.metric("💸 Total Income", f"₹{income}")
    st.metric("🧾 Total Expense", f"₹{expense}")
    st.metric("📊 Balance", f"₹{balance}")

    # ---- Charts ----
    col1, col2 = st.columns(2)

    with col1:
        pie = px.pie(data, values="Amount", names="Category", title="Category Breakdown")
        st.plotly_chart(pie, use_container_width=True)

    with col2:
        bar = px.bar(data, x="Category", y="Amount", color="Type", title="Spending by Category")
        st.plotly_chart(bar, use_container_width=True)
else:
    st.warning("No data yet. Add a transaction to get started.")

# Hide Streamlit menu and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


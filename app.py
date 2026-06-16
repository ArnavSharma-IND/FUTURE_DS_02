import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Customer Churn Dashboard",
    layout="wide"
)

st.title("Customer Retention & Churn Dashboard")

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df.dropna(inplace=True)

df["Churn_Flag"] = df["Churn"].map({
    "Yes": 1,
    "No": 0
})

st.sidebar.header("Filters")

contract = st.sidebar.multiselect(
    "Contract Type",
    df["Contract"].unique(),
    default=df["Contract"].unique()
)

internet = st.sidebar.multiselect(
    "Internet Service",
    df["InternetService"].unique(),
    default=df["InternetService"].unique()
)

filtered = df[
    (df["Contract"].isin(contract)) &
    (df["InternetService"].isin(internet))
]

total = len(filtered)
churned = filtered["Churn_Flag"].sum()
active = total - churned
churn_rate = churned / total * 100
avg_tenure = filtered["tenure"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Customers", f"{total:,}")
c2.metric("Churn Rate", f"{churn_rate:.2f}%")
c3.metric("Active Customers", f"{active:,}")
c4.metric("Avg Tenure", f"{avg_tenure:.1f} Months")

st.markdown("---")

fig1 = px.pie(
    filtered,
    names="Churn",
    title="Churn Distribution"
)

st.plotly_chart(fig1, use_container_width=True)

contract_churn = (
    filtered.groupby("Contract")
    ["Churn_Flag"]
    .mean()
    .reset_index()
)

contract_churn["Churn_Flag"] *= 100

fig2 = px.bar(
    contract_churn,
    x="Contract",
    y="Churn_Flag",
    title="Churn Rate by Contract",
    labels={"Churn_Flag": "Churn Rate (%)"}
)

st.plotly_chart(fig2, use_container_width=True)

internet_churn = (
    filtered.groupby("InternetService")
    ["Churn_Flag"]
    .mean()
    .reset_index()
)

internet_churn["Churn_Flag"] *= 100

fig3 = px.bar(
    internet_churn,
    x="InternetService",
    y="Churn_Flag",
    title="Churn by Internet Service",
    labels={"Churn_Flag": "Churn Rate (%)"}
)

st.plotly_chart(fig3, use_container_width=True)

fig4 = px.histogram(
    filtered,
    x="tenure",
    nbins=20,
    title="Customer Lifetime Distribution"
)

st.plotly_chart(fig4, use_container_width=True)

payment = (
    filtered.groupby("PaymentMethod")
    ["Churn_Flag"]
    .mean()
    .reset_index()
)

payment["Churn_Flag"] *= 100

fig5 = px.bar(
    payment,
    x="PaymentMethod",
    y="Churn_Flag",
    title="Churn by Payment Method"
)

st.plotly_chart(fig5, use_container_width=True)

st.subheader("Dataset Preview")
st.dataframe(filtered.head(20))
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df.dropna(inplace=True)

df["Churn_Flag"] = df["Churn"].map({"Yes": 1, "No": 0})

total_customers = len(df)
churned = df["Churn_Flag"].sum()
active = total_customers - churned
churn_rate = churned / total_customers * 100

print("="*50)
print(f"Total Customers: {total_customers}")
print(f"Churned Customers: {churned}")
print(f"Active Customers: {active}")
print(f"Churn Rate: {churn_rate:.2f}%")
print("="*50)

contract = df.groupby("Contract")["Churn_Flag"].mean() * 100

plt.figure(figsize=(8,5))
contract.plot(kind="bar")
plt.title("Churn Rate by Contract Type")
plt.ylabel("Churn Rate (%)")
plt.show()

internet = df.groupby("InternetService")["Churn_Flag"].mean() * 100

plt.figure(figsize=(8,5))
internet.plot(kind="bar")
plt.title("Churn Rate by Internet Service")
plt.ylabel("Churn Rate (%)")
plt.show()

plt.figure(figsize=(10,5))
plt.hist(df["tenure"], bins=20)
plt.title("Customer Tenure Distribution")
plt.xlabel("Months")
plt.ylabel("Customers")
plt.show()
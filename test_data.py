import pandas as pd

FILE = "NovaTech_Sales_Data.xlsx"

df = pd.read_excel(FILE)

print("\n========== NOVA DATA TEST ==========")

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nColumns:")
print(list(df.columns))

print("\n========== CORE KPIs ==========")

revenue = df["Revenue"].sum()
cost = df["Cost"].sum()
profit = df["Profit"].sum()
units = df["Units_Sold"].sum()
returns = df["Returns"].sum()

gross_margin = profit / revenue * 100
return_rate = returns / units * 100

print(f"Revenue: ${revenue:,.2f}")
print(f"Cost: ${cost:,.2f}")
print(f"Profit: ${profit:,.2f}")
print(f"Units: {units:,}")
print(f"Returns: {returns:,}")
print(f"Gross Margin: {gross_margin:.2f}%")
print(f"Return Rate: {return_rate:.2f}%")

print("\n========== TEST COMPLETE ==========")
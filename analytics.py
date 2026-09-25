"""
============================================================
NOVA ANALYTICS ENGINE
============================================================

Purpose:
    Transform the validated NovaTech Sales dataset into
    reusable analytical outputs for Nova's dashboard,
    visual intelligence engine, and future AI reasoning layer.

Source hierarchy:
    RAW EXCEL DATA
        ↓
    VALIDATED DATA
        ↓
    CALCULATED ANALYTICS
        ↓
    VISUALIZATION / INTELLIGENCE LAYER

Important:
    - This file does NOT modify the raw Excel file.
    - No causal claims are generated here.
    - No arbitrary business thresholds are applied.
    - June 2026 is explicitly treated as a partial period.
============================================================
"""

import pandas as pd

from trust_config import (
    DATASET_CONFIG,
    TRUSTED_KPIS,
)


# ============================================================
# 1. LOAD DATA
# ============================================================

FILE = DATASET_CONFIG["file_name"]

df = pd.read_excel(FILE)

# Convert date column to proper datetime
df["Date"] = pd.to_datetime(df["Date"])


# ============================================================
# 2. BASIC DATA SAFETY CHECK
# ============================================================

required_columns = DATASET_CONFIG["required_columns"]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

if len(df) != DATASET_CONFIG["expected_rows"]:
    raise ValueError(
        f"Unexpected row count. "
        f"Expected {DATASET_CONFIG['expected_rows']}, "
        f"found {len(df)}."
    )


# ============================================================
# 3. OVERALL KPI ANALYTICS
# ============================================================

def calculate_overall_kpis(data):

    revenue = data["Revenue"].sum()
    cost = data["Cost"].sum()
    profit = data["Profit"].sum()

    units = data["Units_Sold"].sum()
    returns = data["Returns"].sum()

    transactions = len(data)

    gross_margin = (
        profit / revenue * 100
        if revenue != 0
        else 0
    )

    return_rate = (
        returns / units * 100
        if units != 0
        else 0
    )

    avg_revenue_order = (
        revenue / transactions
        if transactions != 0
        else 0
    )

    avg_profit_order = (
        profit / transactions
        if transactions != 0
        else 0
    )

    avg_units_order = (
        units / transactions
        if transactions != 0
        else 0
    )

    avg_rating = data["Customer_Rating"].mean()

    return {
        "transactions": transactions,
        "units": int(units),
        "revenue": revenue,
        "cost": cost,
        "profit": profit,
        "gross_margin_pct": gross_margin,
        "returns": int(returns),
        "return_rate_pct": return_rate,
        "avg_revenue_order": avg_revenue_order,
        "avg_profit_order": avg_profit_order,
        "avg_units_order": avg_units_order,
        "avg_customer_rating": avg_rating,
    }


# ============================================================
# 4. PRODUCT ANALYTICS
# ============================================================

def calculate_product_analytics(data):

    result = (
        data.groupby("Product")
        .agg(
            Transactions=("Order_ID", "count"),
            Units=("Units_Sold", "sum"),
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            Profit=("Profit", "sum"),
            Returns=("Returns", "sum"),
            Avg_Rating=("Customer_Rating", "mean"),
        )
        .reset_index()
    )

    result["Gross_Margin_%"] = (
        result["Profit"]
        / result["Revenue"]
        * 100
    )

    result["Return_Rate_%"] = (
        result["Returns"]
        / result["Units"]
        * 100
    )

    result["Revenue_Share_%"] = (
        result["Revenue"]
        / result["Revenue"].sum()
        * 100
    )

    result["Profit_Share_%"] = (
        result["Profit"]
        / result["Profit"].sum()
        * 100
    )

    result = result.sort_values(
        "Revenue",
        ascending=False
    )

    return result


# ============================================================
# 5. REGION ANALYTICS
# ============================================================

def calculate_region_analytics(data):

    result = (
        data.groupby("Region")
        .agg(
            Transactions=("Order_ID", "count"),
            Units=("Units_Sold", "sum"),
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            Profit=("Profit", "sum"),
            Returns=("Returns", "sum"),
            Avg_Rating=("Customer_Rating", "mean"),
        )
        .reset_index()
    )

    result["Gross_Margin_%"] = (
        result["Profit"]
        / result["Revenue"]
        * 100
    )

    result["Return_Rate_%"] = (
        result["Returns"]
        / result["Units"]
        * 100
    )

    result["Revenue_Share_%"] = (
        result["Revenue"]
        / result["Revenue"].sum()
        * 100
    )

    result = result.sort_values(
        "Revenue",
        ascending=False
    )

    return result


# ============================================================
# 6. CHANNEL ANALYTICS
# ============================================================

def calculate_channel_analytics(data):

    result = (
        data.groupby("Channel")
        .agg(
            Transactions=("Order_ID", "count"),
            Units=("Units_Sold", "sum"),
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            Profit=("Profit", "sum"),
            Returns=("Returns", "sum"),
            Avg_Rating=("Customer_Rating", "mean"),
        )
        .reset_index()
    )

    result["Gross_Margin_%"] = (
        result["Profit"]
        / result["Revenue"]
        * 100
    )

    result["Return_Rate_%"] = (
        result["Returns"]
        / result["Units"]
        * 100
    )

    result["Revenue_Share_%"] = (
        result["Revenue"]
        / result["Revenue"].sum()
        * 100
    )

    result = result.sort_values(
        "Revenue",
        ascending=False
    )

    return result


# ============================================================
# 7. CUSTOMER SEGMENT ANALYTICS
# ============================================================

def calculate_segment_analytics(data):

    result = (
        data.groupby("Customer_Segment")
        .agg(
            Transactions=("Order_ID", "count"),
            Units=("Units_Sold", "sum"),
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            Profit=("Profit", "sum"),
            Returns=("Returns", "sum"),
            Avg_Rating=("Customer_Rating", "mean"),
        )
        .reset_index()
    )

    result["Gross_Margin_%"] = (
        result["Profit"]
        / result["Revenue"]
        * 100
    )

    result["Return_Rate_%"] = (
        result["Returns"]
        / result["Units"]
        * 100
    )

    result["Revenue_Share_%"] = (
        result["Revenue"]
        / result["Revenue"].sum()
        * 100
    )

    result = result.sort_values(
        "Revenue",
        ascending=False
    )

    return result


# ============================================================
# 8. MONTHLY TIME-SERIES ANALYTICS
# ============================================================

def calculate_monthly_analytics(data):

    monthly = (
        data.groupby(
            data["Date"].dt.to_period("M")
        )
        .agg(
            Transactions=("Order_ID", "count"),
            Units=("Units_Sold", "sum"),
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            Profit=("Profit", "sum"),
            Returns=("Returns", "sum"),
            Avg_Rating=("Customer_Rating", "mean"),
        )
        .reset_index()
    )

    monthly["Month"] = (
        monthly["Date"]
        .astype(str)
    )

    monthly["Gross_Margin_%"] = (
        monthly["Profit"]
        / monthly["Revenue"]
        * 100
    )

    monthly["Return_Rate_%"] = (
        monthly["Returns"]
        / monthly["Units"]
        * 100
    )

    monthly = monthly[
        [
            "Month",
            "Transactions",
            "Units",
            "Revenue",
            "Cost",
            "Profit",
            "Returns",
            "Gross_Margin_%",
            "Return_Rate_%",
            "Avg_Rating",
        ]
    ]

    return monthly


# ============================================================
# 9. PRODUCT × REGION RETURN RATE MATRIX
# ============================================================

def calculate_product_region_returns(data):

    matrix = pd.pivot_table(
        data,
        values="Returns",
        index="Product",
        columns="Region",
        aggfunc="sum",
        fill_value=0,
    )

    units_matrix = pd.pivot_table(
        data,
        values="Units_Sold",
        index="Product",
        columns="Region",
        aggfunc="sum",
        fill_value=0,
    )

    return_rate_matrix = (
        matrix
        / units_matrix
        * 100
    )

    return return_rate_matrix


# ============================================================
# 10. PRODUCT CONCENTRATION ANALYTICS
# ============================================================

def calculate_product_concentration(data):

    product = calculate_product_analytics(data)

    total_revenue = product["Revenue"].sum()
    total_profit = product["Profit"].sum()

    top_product = product.iloc[0]

    revenue_share = (
        top_product["Revenue"]
        / total_revenue
        * 100
    )

    profit_share = (
        top_product["Profit"]
        / total_profit
        * 100
    )

    return {
        "top_revenue_product": top_product["Product"],
        "top_product_revenue": top_product["Revenue"],
        "top_product_revenue_share_pct": revenue_share,
        "top_product_profit": top_product["Profit"],
        "top_product_profit_share_pct": profit_share,
    }


# ============================================================
# 11. PARTIAL PERIOD DETECTION
# ============================================================

def detect_partial_months(data):

    result = []

    max_date = data["Date"].max()

    latest_month = max_date.to_period("M")

    latest_month_data = data[
        data["Date"].dt.to_period("M")
        == latest_month
    ]

    latest_day = latest_month_data["Date"].max()

    month_end = latest_day.days_in_month

    if latest_day.day < month_end:

        result.append({
            "period": str(latest_month),
            "status": "PARTIAL_PERIOD",
            "latest_date": str(
                latest_day.date()
            ),
            "message": (
                f"{latest_month} is partial. "
                f"Data currently runs through "
                f"{latest_day.date()}."
            ),
        })

    return result


# ============================================================
# 12. ANALYTICS ENGINE
# ============================================================

def run_analytics(data):

    analytics = {

        "overall": calculate_overall_kpis(data),

        "product": calculate_product_analytics(data),

        "region": calculate_region_analytics(data),

        "channel": calculate_channel_analytics(data),

        "segment": calculate_segment_analytics(data),

        "monthly": calculate_monthly_analytics(data),

        "product_region_returns":
            calculate_product_region_returns(data),

        "concentration":
            calculate_product_concentration(data),

        "partial_periods":
            detect_partial_months(data),
    }

    return analytics


# ============================================================
# 13. RUN ENGINE
# ============================================================

analytics = run_analytics(df)


# ============================================================
# 14. CONSOLE REPORT
# ============================================================

print("\n")
print("=" * 80)
print("                    NOVA ANALYTICS ENGINE")
print("=" * 80)


# ------------------------------------------------------------
# OVERALL
# ------------------------------------------------------------

overall = analytics["overall"]

print("\n========== OVERALL KPIs ==========")

print(
    f"Transactions       : "
    f"{overall['transactions']:,}"
)

print(
    f"Units              : "
    f"{overall['units']:,}"
)

print(
    f"Revenue            : "
    f"${overall['revenue']:,.2f}"
)

print(
    f"Cost               : "
    f"${overall['cost']:,.2f}"
)

print(
    f"Profit             : "
    f"${overall['profit']:,.2f}"
)

print(
    f"Gross Margin       : "
    f"{overall['gross_margin_pct']:.2f}%"
)

print(
    f"Returns            : "
    f"{overall['returns']:,}"
)

print(
    f"Return Rate        : "
    f"{overall['return_rate_pct']:.2f}%"
)

print(
    f"Avg Revenue/Order  : "
    f"${overall['avg_revenue_order']:,.2f}"
)

print(
    f"Avg Profit/Order   : "
    f"${overall['avg_profit_order']:,.2f}"
)

print(
    f"Avg Units/Order    : "
    f"{overall['avg_units_order']:.2f}"
)

print(
    f"Avg Customer Rating: "
    f"{overall['avg_customer_rating']:.2f}"
)


# ------------------------------------------------------------
# PRODUCT
# ------------------------------------------------------------

print("\n========== PRODUCT PERFORMANCE ==========")

print(
    analytics["product"][
        [
            "Product",
            "Transactions",
            "Revenue",
            "Profit",
            "Gross_Margin_%",
            "Returns",
            "Return_Rate_%",
            "Avg_Rating",
        ]
    ].to_string(
        index=False,
        formatters={
            "Revenue": "${:,.2f}".format,
            "Profit": "${:,.2f}".format,
            "Gross_Margin_%": "{:.2f}%".format,
            "Return_Rate_%": "{:.2f}%".format,
            "Avg_Rating": "{:.2f}".format,
        },
    )
)


# ------------------------------------------------------------
# REGION
# ------------------------------------------------------------

print("\n========== REGIONAL PERFORMANCE ==========")

print(
    analytics["region"][
        [
            "Region",
            "Transactions",
            "Revenue",
            "Profit",
            "Gross_Margin_%",
            "Returns",
            "Return_Rate_%",
            "Avg_Rating",
        ]
    ].to_string(
        index=False,
        formatters={
            "Revenue": "${:,.2f}".format,
            "Profit": "${:,.2f}".format,
            "Gross_Margin_%": "{:.2f}%".format,
            "Return_Rate_%": "{:.2f}%".format,
            "Avg_Rating": "{:.2f}".format,
        },
    )
)


# ------------------------------------------------------------
# CHANNEL
# ------------------------------------------------------------

print("\n========== CHANNEL PERFORMANCE ==========")

print(
    analytics["channel"][
        [
            "Channel",
            "Transactions",
            "Revenue",
            "Profit",
            "Gross_Margin_%",
            "Returns",
            "Return_Rate_%",
            "Avg_Rating",
        ]
    ].to_string(
        index=False,
        formatters={
            "Revenue": "${:,.2f}".format,
            "Profit": "${:,.2f}".format,
            "Gross_Margin_%": "{:.2f}%".format,
            "Return_Rate_%": "{:.2f}%".format,
            "Avg_Rating": "{:.2f}".format,
        },
    )
)


# ------------------------------------------------------------
# CUSTOMER SEGMENT
# ------------------------------------------------------------

print("\n========== CUSTOMER SEGMENT PERFORMANCE ==========")

print(
    analytics["segment"][
        [
            "Customer_Segment",
            "Transactions",
            "Revenue",
            "Profit",
            "Gross_Margin_%",
            "Returns",
            "Return_Rate_%",
            "Avg_Rating",
        ]
    ].to_string(
        index=False,
        formatters={
            "Revenue": "${:,.2f}".format,
            "Profit": "${:,.2f}".format,
            "Gross_Margin_%": "{:.2f}%".format,
            "Return_Rate_%": "{:.2f}%".format,
            "Avg_Rating": "{:.2f}".format,
        },
    )
)


# ------------------------------------------------------------
# MONTHLY
# ------------------------------------------------------------

print("\n========== MONTHLY PERFORMANCE ==========")

print(
    analytics["monthly"][
        [
            "Month",
            "Transactions",
            "Revenue",
            "Profit",
            "Gross_Margin_%",
            "Returns",
            "Return_Rate_%",
        ]
    ].to_string(
        index=False,
        formatters={
            "Revenue": "${:,.2f}".format,
            "Profit": "${:,.2f}".format,
            "Gross_Margin_%": "{:.2f}%".format,
            "Return_Rate_%": "{:.2f}%".format,
        },
    )
)


# ------------------------------------------------------------
# PRODUCT × REGION RETURNS
# ------------------------------------------------------------

print(
    "\n========== PRODUCT × REGION RETURN RATE =========="
)

print(
    analytics["product_region_returns"]
    .round(2)
    .to_string()
)


# ------------------------------------------------------------
# CONCENTRATION
# ------------------------------------------------------------

concentration = analytics["concentration"]

print(
    "\n========== PRODUCT CONCENTRATION =========="
)

print(
    f"Top revenue product       : "
    f"{concentration['top_revenue_product']}"
)

print(
    f"Revenue                   : "
    f"${concentration['top_product_revenue']:,.2f}"
)

print(
    f"Revenue share             : "
    f"{concentration['top_product_revenue_share_pct']:.2f}%"
)

print(
    f"Profit                    : "
    f"${concentration['top_product_profit']:,.2f}"
)

print(
    f"Profit share              : "
    f"{concentration['top_product_profit_share_pct']:.2f}%"
)


# ------------------------------------------------------------
# PARTIAL PERIOD
# ------------------------------------------------------------

print(
    "\n========== DATA FRESHNESS / PARTIAL PERIOD =========="
)

if analytics["partial_periods"]:

    for period in analytics["partial_periods"]:

        print(
            f"⚠️ {period['status']}: "
            f"{period['message']}"
        )

else:

    print(
        "No partial latest month detected."
    )


# ============================================================
# FINAL STATUS
# ============================================================

print("\n" + "=" * 80)

print(
    "🟢 NOVA ANALYTICS ENGINE: "
    "READY"
)

print(
    "Analytics generated directly from "
    "the NovaTech raw dataset."
)

print(
    "No causal assumptions or arbitrary "
    "business thresholds were applied."
)

print("=" * 80)
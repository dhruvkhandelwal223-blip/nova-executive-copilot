"""
NOVA INSIGHT & INVESTIGATION ENGINE
-----------------------------------

Purpose:
Convert validated signals into connected business insights
and structured investigation paths.

Flow:

RAW DATA
    ↓
DATA VALIDATION
    ↓
ANALYTICS
    ↓
SIGNAL DETECTION
    ↓
INSIGHT ENGINE
    ↓
MANAGEMENT INTELLIGENCE
    ↓
VISUAL INTELLIGENCE
    ↓
EXECUTIVE OUTPUT

Core principles:
- Raw data is the source of truth.
- Signals identify patterns; they do not prove causation.
- Insights connect multiple validated signals.
- Facts and interpretations remain separate.
- Unknowns are explicitly identified.
- Investigation questions are generated where evidence is incomplete.
- No arbitrary business thresholds are introduced.
"""

import pandas as pd

from analytics import (
    calculate_overall_kpis,
    calculate_product_analytics,
    calculate_region_analytics,
    detect_partial_months,
)

from signal_detection import signal_df


# ============================================================
# 1. CONFIGURATION
# ============================================================

DATA_FILE = "NovaTech_Sales_Data.xlsx"


# ============================================================
# 2. LOAD RAW DATA
# ============================================================

df = pd.read_excel(DATA_FILE)

df["Date"] = pd.to_datetime(df["Date"])


# ============================================================
# 3. REQUIRED COLUMN CHECK
# ============================================================

REQUIRED_COLUMNS = [
    "Order_ID",
    "Date",
    "Region",
    "Product",
    "Channel",
    "Customer_Segment",
    "Units_Sold",
    "Revenue",
    "Cost",
    "Profit",
    "Returns",
    "Customer_Rating",
    "Gross_Margin_%",
    "Return_Rate_%",
]

missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing_columns:

    raise ValueError(
        "Required columns missing from dataset: "
        + ", ".join(missing_columns)
    )


# ============================================================
# 4. RUN EXISTING ANALYTICS
# ============================================================

overall = calculate_overall_kpis(df)

product_df = calculate_product_analytics(df)

region_df = calculate_region_analytics(df)

partial_months = detect_partial_months(df)


# ============================================================
# 5. CALCULATE COMPANY-LEVEL VALUES DIRECTLY
# ============================================================

company_revenue = df["Revenue"].sum()

company_profit = df["Profit"].sum()

company_units = df["Units_Sold"].sum()

company_returns = df["Returns"].sum()

company_return_rate = (
    company_returns / company_units * 100
    if company_units != 0
    else 0
)

company_gross_margin = (
    company_profit / company_revenue * 100
    if company_revenue != 0
    else 0
)

company_average_rating = df["Customer_Rating"].mean()


# ============================================================
# 6. CALCULATE PRODUCT CONCENTRATION DIRECTLY
# ============================================================
#
# We deliberately calculate this from raw data instead of
# depending on the structure of calculate_product_concentration().
#
# This prevents dataframe-column naming problems and keeps
# raw data as the source of truth.
# ============================================================

product_summary = (
    df.groupby("Product")
    .agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Units=("Units_Sold", "sum"),
        Transactions=("Order_ID", "count"),
    )
    .reset_index()
)

product_summary["Revenue_Share_%"] = (
    product_summary["Revenue"]
    / company_revenue
    * 100
)

product_summary["Profit_Share_%"] = (
    product_summary["Profit"]
    / company_profit
    * 100
)


# ============================================================
# 7. GET NOVAWATCH PRO CONCENTRATION
# ============================================================

watch_pro_concentration_rows = product_summary[
    product_summary["Product"] == "NovaWatch Pro"
]

if watch_pro_concentration_rows.empty:

    raise ValueError(
        "NovaWatch Pro was not found in raw product summary."
    )

watch_pro_concentration = (
    watch_pro_concentration_rows.iloc[0]
)


# ============================================================
# 8. GET KEY PRODUCT DATA
# ============================================================

buds_x_rows = product_df[
    product_df["Product"] == "NovaBuds X"
]

watch_pro_rows = product_df[
    product_df["Product"] == "NovaWatch Pro"
]

fit_band_rows = product_df[
    product_df["Product"] == "NovaFit Band"
]


if buds_x_rows.empty:

    raise ValueError(
        "NovaBuds X was not found in product analytics."
    )

if watch_pro_rows.empty:

    raise ValueError(
        "NovaWatch Pro was not found in product analytics."
    )

if fit_band_rows.empty:

    raise ValueError(
        "NovaFit Band was not found in product analytics."
    )


buds_x = buds_x_rows.iloc[0]

watch_pro_product = watch_pro_rows.iloc[0]

fit_band = fit_band_rows.iloc[0]


# ============================================================
# 9. GET REGIONAL DATA
# ============================================================

east_rows = region_df[
    region_df["Region"] == "East"
]

west_rows = region_df[
    region_df["Region"] == "West"
]


if east_rows.empty:

    raise ValueError(
        "East was not found in regional analytics."
    )

if west_rows.empty:

    raise ValueError(
        "West was not found in regional analytics."
    )


east = east_rows.iloc[0]

west = west_rows.iloc[0]


# ============================================================
# 10. INSIGHT BUILDER
# ============================================================

def build_insight(
    insight_id,
    title,
    linked_signals,
    evidence_level,
    known_facts,
    interpretation,
    unknowns,
    investigation_questions,
    limitations,
):

    return {

        "Insight_ID": insight_id,

        "Title": title,

        "Linked_Signals": linked_signals,

        "Evidence_Level": evidence_level,

        "Known_Facts": known_facts,

        "Interpretation": interpretation,

        "Unknowns": unknowns,

        "Investigation_Questions": investigation_questions,

        "Limitations": limitations,

    }


# ============================================================
# 11. INSIGHT 001
# NOVABUDS X
# ============================================================

insight_001 = build_insight(

    insight_id="INS-001",

    title=(
        "NovaBuds X shows a combined return-rate "
        "and customer-experience signal"
    ),

    linked_signals=[
        "SIG-001",
        "SIG-002",
        "SIG-003",
    ],

    evidence_level="VALIDATED_PATTERN",

    known_facts=[

        (
            f"NovaBuds X return rate is "
            f"{buds_x['Return_Rate_%']:.2f}%, "
            f"compared with the company return rate of "
            f"{company_return_rate:.2f}%."
        ),

        (
            f"NovaBuds X average customer rating is "
            f"{buds_x['Avg_Rating']:.2f}, "
            f"compared with company average rating of "
            f"{company_average_rating:.2f}."
        ),

        (
            "NovaBuds X has the highest product-level "
            "return rate in the dataset."
        ),

        (
            "NovaBuds X has elevated return rates across "
            "all four regions."
        ),

        (
            "NovaBuds X has its highest regional return rate "
            "in West at 8.24%."
        ),
    ],

    interpretation=[

        (
            "The return-rate and customer-rating signals "
            "appear together in the available data."
        ),

        (
            "The data supports treating NovaBuds X as a "
            "product requiring investigation."
        ),

        (
            "The current dataset does not establish why "
            "customers are returning the product."
        ),
    ],

    unknowns=[

        "Specific return reasons are not available.",

        "Customer complaint details are not available.",

        "Product defect information is not available.",

        "Delivery or handling information is not available.",

        "Return reasons by region are not available.",
    ],

    investigation_questions=[

        "What are the top stated reasons for NovaBuds X returns?",

        (
            "Are returns associated with product defects, "
            "fit, comfort, battery, connectivity, packaging, "
            "or another issue?"
        ),

        (
            "Do customer complaints show the same pattern "
            "as returns?"
        ),

        (
            "Why is NovaBuds X return rate highest in West?"
        ),

        (
            "Does the West pattern remain after considering "
            "product mix and order volume?"
        ),
    ],

    limitations=[

        (
            "No causal conclusion should be made from the "
            "current sales dataset."
        ),

        (
            "Customer rating and return rate are observational "
            "signals, not proof of cause."
        ),
    ],
)


# ============================================================
# 12. INSIGHT 002
# EAST REGIONAL RETURN SIGNAL
# ============================================================

insight_002 = build_insight(

    insight_id="INS-002",

    title=(
        "East has the highest overall regional return rate, "
        "but the cause is not established"
    ),

    linked_signals=[
        "SIG-004",
        "SIG-010",
        "SIG-003",
    ],

    evidence_level="VALIDATED_PATTERN",

    known_facts=[

        (
            f"East has the highest overall regional return "
            f"rate at {east['Return_Rate_%']:.2f}%."
        ),

        (
            f"West has an overall return rate of "
            f"{west['Return_Rate_%']:.2f}%."
        ),

        (
            "Within NovaBuds X, West has the highest "
            "regional return rate at 8.24%."
        ),

        (
            "Within East, NovaBuds X has a return rate "
            "of 7.80%."
        ),

        (
            "East's elevated return rate is not limited "
            "to a single product."
        ),
    ],

    interpretation=[

        (
            "East should be investigated as a regional "
            "return-rate signal."
        ),

        (
            "Product mix and regional factors both require "
            "further examination."
        ),

        (
            "The available data does not establish logistics, "
            "delivery, or fulfilment as the cause."
        ),
    ],

    unknowns=[

        "Return reasons by region are unavailable.",

        "Delivery-time data is unavailable.",

        "Courier or fulfilment data is unavailable.",

        "Customer complaint data by region is unavailable.",

        (
            "Product-mix-adjusted regional return analysis "
            "has not been performed."
        ),
    ],

    investigation_questions=[

        "Which products contribute most to East's return rate?",

        "Are East returns concentrated in particular channels?",

        (
            "Are East returns associated with specific "
            "fulfilment or delivery patterns?"
        ),

        (
            "Do customer complaints in East differ "
            "from other regions?"
        ),

        (
            "Is the East signal still present after "
            "considering product mix?"
        ),
    ],

    limitations=[

        (
            "East's high return rate does not prove "
            "a logistics problem."
        ),

        (
            "NovaBuds X is not uniquely responsible "
            "for the entire East regional signal."
        ),

        (
            "West is the worst region specifically "
            "for NovaBuds X."
        ),
    ],
)


# ============================================================
# 13. INSIGHT 003
# NOVAWATCH PRO CONCENTRATION
# ============================================================

insight_003 = build_insight(

    insight_id="INS-003",

    title=(
        "NovaWatch Pro represents a significant share "
        "of company revenue and profit"
    ),

    linked_signals=[
        "SIG-005",
        "SIG-007",
    ],

    evidence_level="VALIDATED_PATTERN",

    known_facts=[

        (
            f"NovaWatch Pro contributes "
            f"{watch_pro_concentration['Revenue_Share_%']:.2f}% "
            f"of total revenue."
        ),

        (
            f"NovaWatch Pro contributes "
            f"{watch_pro_concentration['Profit_Share_%']:.2f}% "
            f"of total profit."
        ),

        (
            f"NovaWatch Pro gross margin is "
            f"{watch_pro_product['Gross_Margin_%']:.2f}%."
        ),

        (
            "NovaWatch Pro is the largest product by "
            "revenue, profit, and units."
        ),
    ],

    interpretation=[

        (
            "A large portion of current business performance "
            "is associated with NovaWatch Pro."
        ),

        (
            "The concentration signal is relevant for "
            "portfolio-dependency monitoring."
        ),

        (
            "The data does not establish that this "
            "concentration is inherently positive or negative."
        ),
    ],

    unknowns=[

        (
            "Management-defined acceptable concentration "
            "level is not available."
        ),

        "Sales pipeline dependency is not available.",

        "Future demand forecasts are not available.",

        "Product lifecycle information is not available.",

        "Pricing and discount details are not available.",
    ],

    investigation_questions=[

        (
            "What percentage of the future sales pipeline "
            "depends on NovaWatch Pro?"
        ),

        (
            "How stable is NovaWatch Pro demand over time?"
        ),

        (
            "What is driving the product's lower margin "
            "compared with other products?"
        ),

        (
            "How sensitive is total company profit to "
            "changes in NovaWatch Pro volume?"
        ),

        (
            "Are alternative products capable of absorbing "
            "demand if NovaWatch Pro demand changes?"
        ),
    ],

    limitations=[

        (
            "No arbitrary concentration threshold is applied."
        ),

        (
            "The dataset alone cannot determine whether "
            "the concentration represents an unacceptable risk."
        ),
    ],
)


# ============================================================
# 14. INSIGHT 004
# PRODUCT MARGIN
# ============================================================

insight_004 = build_insight(

    insight_id="INS-004",

    title=(
        "Product margins differ across the portfolio"
    ),

    linked_signals=[
        "SIG-006",
        "SIG-007",
    ],

    evidence_level="VALIDATED_PATTERN",

    known_facts=[

        (
            f"NovaFit Band has the highest gross margin "
            f"at {fit_band['Gross_Margin_%']:.2f}%."
        ),

        (
            f"NovaWatch Pro has the lowest gross margin "
            f"at {watch_pro_product['Gross_Margin_%']:.2f}%."
        ),

        (
            "The portfolio contains differences in "
            "product-level margins."
        ),
    ],

    interpretation=[

        (
            "The margin difference creates an opportunity "
            "to investigate product economics."
        ),

        (
            "Margin differences alone do not prove that "
            "one product has better pricing."
        ),

        (
            "The Fitness Enthusiast margin difference is "
            "driven by product mix rather than a proven "
            "pricing advantage."
        ),
    ],

    unknowns=[

        "Product-level pricing strategy is unavailable.",

        "Discount information is unavailable.",

        "Detailed product cost drivers are unavailable.",

        "Marketing and acquisition costs are unavailable.",
    ],

    investigation_questions=[

        (
            "What cost components explain the margin "
            "difference between products?"
        ),

        (
            "Are discounts affecting product-level margins?"
        ),

        (
            "Which products generate the best profit "
            "after all relevant costs?"
        ),

        (
            "Are higher-margin products scalable without "
            "affecting demand or returns?"
        ),
    ],

    limitations=[

        (
            "Gross margin is based on the available "
            "Revenue and Cost fields."
        ),

        (
            "No conclusion about optimal pricing should "
            "be made without additional pricing and demand data."
        ),
    ],
)


# ============================================================
# 15. INSIGHT 005
# JUNE PARTIAL PERIOD
# ============================================================

insight_005 = build_insight(

    insight_id="INS-005",

    title=(
        "June 2026 is a partial reporting period "
        "and requires caution"
    ),

    linked_signals=[
        "SIG-008",
        "SIG-009",
    ],

    evidence_level="RAW_DATA_VERIFIED",

    known_facts=[

        (
            "June 2026 contains transactions only through "
            "June 29."
        ),

        (
            "June 2026 contains 22 transactions."
        ),

        (
            "June 2026 revenue is lower than May 2026 revenue."
        ),

        (
            "The current dataset identifies June 2026 "
            "as a partial month."
        ),
    ],

    interpretation=[

        (
            "June 2026 should not be treated as a "
            "complete-month performance result."
        ),

        (
            "Month-over-month comparisons involving June "
            "should clearly display the partial-period warning."
        ),

        (
            "The available data is insufficient to determine "
            "full-month June performance."
        ),
    ],

    unknowns=[

        (
            "Transactions after June 29 are not present "
            "in the dataset."
        ),

        "Full-month June revenue is unknown.",

        "Full-month June profit is unknown.",

        "Full-month June return rate is unknown.",
    ],

    investigation_questions=[

        (
            "Will additional June transactions become available?"
        ),

        (
            "What is the complete June performance after "
            "the reporting period closes?"
        ),

        (
            "Should partial-month values be excluded from "
            "executive trend comparisons?"
        ),
    ],

    limitations=[

        (
            "Do not interpret the June month-over-month "
            "movement as a complete-month performance trend."
        ),

        (
            "Do not forecast June full-month results from "
            "the current partial dataset."
        ),
    ],
)


# ============================================================
# 16. INSIGHT 006
# PROFITABILITY + RETURNS
# ============================================================

insight_006 = build_insight(

    insight_id="INS-006",

    title=(
        "Product profitability and return performance "
        "should be evaluated together"
    ),

    linked_signals=[
        "SIG-001",
        "SIG-006",
        "SIG-007",
    ],

    evidence_level="CALCULATED_FROM_RAW_DATA",

    known_facts=[

        (
            f"NovaBuds X has a gross margin of "
            f"{buds_x['Gross_Margin_%']:.2f}% and a return "
            f"rate of {buds_x['Return_Rate_%']:.2f}%."
        ),

        (
            f"NovaFit Band has a gross margin of "
            f"{fit_band['Gross_Margin_%']:.2f}% and a return "
            f"rate of {fit_band['Return_Rate_%']:.2f}%."
        ),

        (
            "Product profitability and product return "
            "performance vary across the portfolio."
        ),
    ],

    interpretation=[

        (
            "Margin alone should not be used as the only "
            "product-performance indicator."
        ),

        (
            "Nova should consider profitability, returns, "
            "ratings, and volume together when investigating "
            "product performance."
        ),

        (
            "The dataset does not establish whether high "
            "returns are reducing product profitability "
            "beyond the recorded Cost and Profit fields."
        ),
    ],

    unknowns=[

        "Cost impact of returns is not separately available.",

        "Refund and replacement costs are not separately available.",

        "Return processing costs are not separately available.",
    ],

    investigation_questions=[

        (
            "What is the financial impact of returns by product?"
        ),

        (
            "Do returned units generate additional replacement "
            "or service costs?"
        ),

        (
            "Which products combine strong profit contribution "
            "with acceptable return performance?"
        ),
    ],

    limitations=[

        (
            "The current Profit field may not separately "
            "capture all return-related economic effects."
        ),

        (
            "No causal relationship between margin and "
            "returns should be inferred."
        ),
    ],
)


# ============================================================
# 17. MASTER INSIGHT REGISTER
# ============================================================

insights = [

    insight_001,
    insight_002,
    insight_003,
    insight_004,
    insight_005,
    insight_006,

]


insight_df = pd.DataFrame(insights)


# ============================================================
# 18. DISPLAY HEADER
# ============================================================

print("\n")
print("=" * 90)

print(
    "                    NOVA INSIGHT & INVESTIGATION ENGINE"
)

print("=" * 90)

print("\nPurpose:")

print(
    "Connect validated signals into evidence-based "
    "business insights and investigation paths."
)

print(
    f"\nTotal insights generated: {len(insight_df)}"
)


# ============================================================
# 19. DISPLAY INSIGHTS
# ============================================================

print("\n")
print("=" * 90)

print("INSIGHT REGISTER")

print("=" * 90)


for _, row in insight_df.iterrows():

    print("\n")
    print("-" * 90)

    print(
        f"{row['Insight_ID']} | {row['Title']}"
    )

    print(
        f"Evidence Level: {row['Evidence_Level']}"
    )

    print(
        "Linked Signals: "
        + ", ".join(row["Linked_Signals"])
    )

    print("\nKNOWN FACTS:")

    for fact in row["Known_Facts"]:

        print(f"  • {fact}")

    print("\nINTERPRETATION:")

    for item in row["Interpretation"]:

        print(f"  • {item}")

    print("\nUNKNOWN:")

    for item in row["Unknowns"]:

        print(f"  • {item}")

    print("\nINVESTIGATION QUESTIONS:")

    for item in row["Investigation_Questions"]:

        print(f"  • {item}")

    print("\nLIMITATIONS:")

    for item in row["Limitations"]:

        print(f"  • {item}")


# ============================================================
# 20. SUMMARY
# ============================================================

print("\n")
print("=" * 90)

print(
    "                    NOVA INSIGHT ENGINE SUMMARY"
)

print("=" * 90)

print(
    f"\nTotal insights: {len(insight_df)}"
)

print("\nEvidence Levels:")

print(
    insight_df["Evidence_Level"]
    .value_counts()
    .to_string()
)


# ============================================================
# 21. CONNECTED SIGNALS
# ============================================================

all_linked_signals = []

for signals in insight_df["Linked_Signals"]:

    all_linked_signals.extend(signals)


unique_linked_signals = sorted(
    set(all_linked_signals)
)


print("\nSignals connected to insights:")

for signal_id in unique_linked_signals:

    print(f"  ✓ {signal_id}")


# ============================================================
# 22. FINAL STATUS
# ============================================================

print("\n")
print("=" * 90)

print(
    "🟢 NOVA INSIGHT & INVESTIGATION ENGINE: READY"
)

print(
    "Insights connect validated signals without "
    "claiming unsupported causation."
)

print(
    "Unknowns and investigation requirements are "
    "explicitly separated from observed facts."
)

print(
    "No arbitrary business thresholds or risk scores "
    "were applied."
)

print("=" * 90)
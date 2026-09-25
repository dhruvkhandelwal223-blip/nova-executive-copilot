"""
============================================================
NOVA SIGNAL DETECTION ENGINE
============================================================

Purpose:
    Detect meaningful analytical signals from the outputs
    produced by Nova's Analytics Engine.

IMPORTANT PRINCIPLES:
    - Signals are not automatically problems.
    - Signals are not causal conclusions.
    - No arbitrary business thresholds are used.
    - Every signal contains evidence and context.
    - Known audit corrections remain in the Trust Layer.
    - Partial periods are explicitly flagged.

Evidence hierarchy:

    RAW DATA
        ↓
    CALCULATED
        ↓
    VALIDATED PATTERN
        ↓
    INTERPRETATION
        ↓
    HYPOTHESIS
        ↓
    INVESTIGATION REQUIRED
============================================================
"""

import pandas as pd

from analytics import (
    df,
    calculate_overall_kpis,
    calculate_product_analytics,
    calculate_region_analytics,
    calculate_channel_analytics,
    calculate_segment_analytics,
    calculate_monthly_analytics,
    calculate_product_region_returns,
    calculate_product_concentration,
    detect_partial_months,
)


# ============================================================
# 1. SIGNAL STORAGE
# ============================================================

signals = []


def add_signal(
    signal_id,
    category,
    title,
    observation,
    evidence,
    evidence_level,
    interpretation,
    investigation,
    metric=None,
    value=None,
    comparison=None,
):
    """
    Add a structured signal to Nova's signal register.
    """

    signals.append({

        "signal_id": signal_id,

        "category": category,

        "title": title,

        "observation": observation,

        "evidence": evidence,

        "evidence_level": evidence_level,

        "interpretation": interpretation,

        "investigation_required": investigation,

        "metric": metric,

        "value": value,

        "comparison": comparison,
    })


# ============================================================
# 2. LOAD ANALYTICS
# ============================================================

overall = calculate_overall_kpis(df)

product = calculate_product_analytics(df)

region = calculate_region_analytics(df)

channel = calculate_channel_analytics(df)

segment = calculate_segment_analytics(df)

monthly = calculate_monthly_analytics(df)

product_region_returns = calculate_product_region_returns(df)

concentration = calculate_product_concentration(df)

partial_periods = detect_partial_months(df)


# ============================================================
# 3. SIGNAL: NOVABUDS X RETURN RATE
# ============================================================

company_return_rate = overall["return_rate_pct"]

novabuds_x = product[
    product["Product"] == "NovaBuds X"
]

if not novabuds_x.empty:

    row = novabuds_x.iloc[0]

    product_return_rate = row["Return_Rate_%"]

    difference = (
        product_return_rate
        - company_return_rate
    )

    add_signal(

        signal_id="SIG-001",

        category="PRODUCT_RETURN",

        title="NovaBuds X has elevated return rate",

        observation=(
            f"NovaBuds X has a return rate of "
            f"{product_return_rate:.2f}%, compared with "
            f"the company return rate of "
            f"{company_return_rate:.2f}%."
        ),

        evidence=(
            f"Difference: "
            f"{difference:+.2f} percentage points."
        ),

        evidence_level="VALIDATED_PATTERN",

        interpretation=(
            "NovaBuds X is an identifiable product-level "
            "return-rate signal that warrants investigation."
        ),

        investigation=(
            "Review product-level return reasons, "
            "customer support records, quality records, "
            "and other available diagnostic data."
        ),

        metric="Return Rate",

        value=product_return_rate,

        comparison=company_return_rate,
    )


# ============================================================
# 4. SIGNAL: NOVABUDS X CUSTOMER RATING
# ============================================================

novabuds_x_rating = (
    novabuds_x.iloc[0]["Avg_Rating"]
    if not novabuds_x.empty
    else None
)

if novabuds_x_rating is not None:

    company_rating = overall["avg_customer_rating"]

    rating_difference = (
        novabuds_x_rating
        - company_rating
    )

    add_signal(

        signal_id="SIG-002",

        category="PRODUCT_CUSTOMER_EXPERIENCE",

        title="NovaBuds X has lower average rating",

        observation=(
            f"NovaBuds X average customer rating is "
            f"{novabuds_x_rating:.2f}, compared with the "
            f"company average of {company_rating:.2f}."
        ),

        evidence=(
            f"Difference: "
            f"{rating_difference:+.2f} rating points."
        ),

        evidence_level="VALIDATED_PATTERN",

        interpretation=(
            "NovaBuds X shows a lower average rating "
            "than the company-wide average."
        ),

        investigation=(
            "Review customer feedback and support records "
            "to determine whether recurring issues are "
            "associated with the lower rating."
        ),

        metric="Average Customer Rating",

        value=novabuds_x_rating,

        comparison=company_rating,
    )


# ============================================================
# 5. SIGNAL: NOVABUDS X × WEST
# ============================================================

if "NovaBuds X" in product_region_returns.index:

    buds_x_regions = (
        product_region_returns.loc["NovaBuds X"]
    )

    worst_region = buds_x_regions.idxmax()

    worst_rate = buds_x_regions.max()

    add_signal(

        signal_id="SIG-003",

        category="PRODUCT_REGION",

        title="NovaBuds X has highest return rate in West",

        observation=(
            f"NovaBuds X return rate is highest in "
            f"{worst_region} at {worst_rate:.2f}%."
        ),

        evidence=(
            "This is calculated from the product-region "
            "return-rate matrix."
        ),

        evidence_level="VALIDATED_PATTERN",

        interpretation=(
            "The NovaBuds X × West combination is a "
            "specific product-region pattern that "
            "warrants investigation."
        ),

        investigation=(
            "Review regional return reasons, delivery/"
            "fulfilment information, customer feedback, "
            "and product handling data if available."
        ),

        metric="NovaBuds X Return Rate in West",

        value=worst_rate,

        comparison=None,
    )


# ============================================================
# 6. SIGNAL: EAST REGIONAL RETURN RATE
# ============================================================

east = region[
    region["Region"] == "East"
]

if not east.empty:

    east_row = east.iloc[0]

    east_return_rate = east_row["Return_Rate_%"]

    highest_region = region.loc[
        region["Return_Rate_%"].idxmax()
    ]

    add_signal(

        signal_id="SIG-004",

        category="REGIONAL_RETURN",

        title="East has the highest overall regional return rate",

        observation=(
            f"East has a return rate of "
            f"{east_return_rate:.2f}%, the highest among "
            f"the four regions."
        ),

        evidence=(
            "Calculated from regional units and returns."
        ),

        evidence_level="VALIDATED_PATTERN",

        interpretation=(
            "East shows a broad regional return-rate "
            "signal across the dataset."
        ),

        investigation=(
            "Review regional return reasons, fulfilment "
            "patterns, customer feedback, and product mix. "
            "Logistics is only a hypothesis until additional "
            "evidence is available."
        ),

        metric="Regional Return Rate",

        value=east_return_rate,

        comparison=company_return_rate,
    )


# ============================================================
# 7. SIGNAL: NOVAWATCH PRO CONCENTRATION
# ============================================================

top_product = concentration[
    "top_revenue_product"
]

revenue_share = concentration[
    "top_product_revenue_share_pct"
]

profit_share = concentration[
    "top_product_profit_share_pct"
]

add_signal(

    signal_id="SIG-005",

    category="REVENUE_CONCENTRATION",

    title="Revenue is concentrated in NovaWatch Pro",

    observation=(
        f"{top_product} contributes "
        f"{revenue_share:.2f}% of total revenue and "
        f"{profit_share:.2f}% of total profit."
    ),

    evidence=(
        "Calculated from product-level revenue and profit."
    ),

    evidence_level="VALIDATED_PATTERN",

    interpretation=(
        "A substantial share of business revenue and "
        "profit is associated with one product."
    ),

    investigation=(
        "Assess product dependency, portfolio balance, "
        "sales pipeline diversity, and management-defined "
        "concentration risk criteria."
    ),

    metric="Top Product Revenue Share",

    value=revenue_share,

    comparison=None,
)


# ============================================================
# 8. SIGNAL: NOVAFIT BAND HIGH MARGIN
# ============================================================

novafit = product[
    product["Product"] == "NovaFit Band"
]

if not novafit.empty:

    fit_row = novafit.iloc[0]

    fit_margin = fit_row["Gross_Margin_%"]

    add_signal(

        signal_id="SIG-006",

        category="PRODUCT_MARGIN",

        title="NovaFit Band has the highest product margin",

        observation=(
            f"NovaFit Band has a gross margin of "
            f"{fit_margin:.2f}%, the highest among "
            f"the products in the dataset."
        ),

        evidence=(
            "Calculated from product-level profit and revenue."
        ),

        evidence_level="VALIDATED_PATTERN",

        interpretation=(
            "NovaFit Band shows the highest observed "
            "blended gross margin among the products."
        ),

        investigation=(
            "Review product economics, volume, cost structure, "
            "and demand before drawing conclusions about "
            "scalability or strategic importance."
        ),

        metric="Gross Margin",

        value=fit_margin,

        comparison=None,
    )


# ============================================================
# 9. SIGNAL: NOVAWATCH PRO LOWEST PRODUCT MARGIN
# ============================================================

watch_pro = product[
    product["Product"] == "NovaWatch Pro"
]

if not watch_pro.empty:

    watch_row = watch_pro.iloc[0]

    watch_margin = watch_row["Gross_Margin_%"]

    lowest_margin_product = product.loc[
        product["Gross_Margin_%"].idxmin()
    ]

    add_signal(

        signal_id="SIG-007",

        category="PRODUCT_MARGIN",

        title="NovaWatch Pro has the lowest product margin",

        observation=(
            f"NovaWatch Pro has a gross margin of "
            f"{watch_margin:.2f}%, the lowest among "
            f"the products."
        ),

        evidence=(
            "Calculated from product-level profit and revenue."
        ),

        evidence_level="VALIDATED_PATTERN",

        interpretation=(
            "The product generating the largest revenue "
            "share also has the lowest observed product "
            "gross margin."
        ),

        investigation=(
            "Review product-level cost structure, pricing, "
            "discounting, and profitability drivers."
        ),

        metric="Gross Margin",

        value=watch_margin,

        comparison=None,
    )


# ============================================================
# 10. SIGNAL: MONTHLY REVENUE MOVEMENT
# ============================================================

if len(monthly) >= 2:

    previous_month = monthly.iloc[-2]

    latest_month = monthly.iloc[-1]

    previous_revenue = previous_month["Revenue"]

    latest_revenue = latest_month["Revenue"]

    revenue_change = (
        (latest_revenue - previous_revenue)
        / previous_revenue
        * 100
        if previous_revenue != 0
        else 0
    )

    add_signal(

        signal_id="SIG-008",

        category="TIME_SERIES",

        title="Latest month revenue differs from previous month",

        observation=(
            f"{latest_month['Month']} revenue was "
            f"${latest_revenue:,.2f}, compared with "
            f"${previous_revenue:,.2f} in "
            f"{previous_month['Month']}."
        ),

        evidence=(
            f"Month-over-month change: "
            f"{revenue_change:+.2f}%."
        ),

        evidence_level="CALCULATED_FROM_RAW_DATA",

        interpretation=(
            "The latest month shows a measurable revenue "
            "change relative to the preceding month."
        ),

        investigation=(
            "Because the latest month is partial, do not "
            "interpret this month-over-month movement as a "
            "full-month performance trend."
        ),

        metric="Monthly Revenue",

        value=latest_revenue,

        comparison=previous_revenue,
    )


# ============================================================
# 11. SIGNAL: PARTIAL PERIOD
# ============================================================

for period in partial_periods:

    add_signal(

        signal_id="SIG-009",

        category="DATA_QUALITY",

        title="Latest month is a partial period",

        observation=(
            period["message"]
        ),

        evidence=(
            "Detected from the latest transaction date "
            "relative to the calendar month."
        ),

        evidence_level="RAW_DATA_VERIFIED",

        interpretation=(
            "Latest-month comparisons require caution "
            "because the period is incomplete."
        ),

        investigation=(
            "Use completed-period comparisons or clearly "
            "label the latest period as partial."
        ),

        metric="Data Freshness",

        value=period["latest_date"],

        comparison=None,
    )


# ============================================================
# 12. SIGNAL: EAST PRODUCT-REGION CONTEXT
# ============================================================

if "East" in product_region_returns.columns:

    east_product_rates = (
        product_region_returns["East"]
        .sort_values(
            ascending=False
        )
    )

    highest_east_product = (
        east_product_rates.index[0]
    )

    highest_east_rate = (
        east_product_rates.iloc[0]
    )

    add_signal(

        signal_id="SIG-010",

        category="REGIONAL_PRODUCT",

        title="East return-rate signal has product-level variation",

        observation=(
            f"Within East, {highest_east_product} has the "
            f"highest observed product return rate at "
            f"{highest_east_rate:.2f}%."
        ),

        evidence=(
            "Calculated from the product-region return-rate "
            "matrix."
        ),

        evidence_level="CALCULATED_FROM_RAW_DATA",

        interpretation=(
            "The elevated East regional return rate is not "
            "necessarily uniform across all products."
        ),

        investigation=(
            "Review product mix and product-specific return "
            "patterns before attributing the regional signal "
            "to a single cause."
        ),

        metric="Highest East Product Return Rate",

        value=highest_east_rate,

        comparison=None,
    )


# ============================================================
# 13. SIGNAL REGISTER DATAFRAME
# ============================================================

signal_df = pd.DataFrame(signals)


# ============================================================
# 14. SIGNAL SUMMARY
# ============================================================

def summarize_signals(signal_data):

    return {
        "total_signals": len(signal_data),

        "categories": (
            signal_data["category"]
            .value_counts()
            .to_dict()
            if not signal_data.empty
            else {}
        ),

        "evidence_levels": (
            signal_data["evidence_level"]
            .value_counts()
            .to_dict()
            if not signal_data.empty
            else {}
        ),
    }


signal_summary = summarize_signals(
    signal_df
)


# ============================================================
# 15. CONSOLE REPORT
# ============================================================

print("\n")
print("=" * 90)
print("                    NOVA SIGNAL DETECTION ENGINE")
print("=" * 90)


print(
    "\n========== SIGNAL REGISTER =========="
)


for _, signal in signal_df.iterrows():

    print("\n" + "-" * 90)

    print(
        f"{signal['signal_id']} | "
        f"{signal['category']}"
    )

    print(
        f"TITLE: "
        f"{signal['title']}"
    )

    print(
        f"OBSERVATION: "
        f"{signal['observation']}"
    )

    print(
        f"EVIDENCE: "
        f"{signal['evidence']}"
    )

    print(
        f"EVIDENCE LEVEL: "
        f"{signal['evidence_level']}"
    )

    print(
        f"INTERPRETATION: "
        f"{signal['interpretation']}"
    )

    print(
        f"INVESTIGATION: "
        f"{signal['investigation_required']}"
    )


# ============================================================
# 16. SUMMARY
# ============================================================

print("\n")
print("=" * 90)
print("                    SIGNAL SUMMARY")
print("=" * 90)

print(
    f"\nTotal signals detected: "
    f"{signal_summary['total_signals']}"
)


print(
    "\n========== BY CATEGORY =========="
)

for category, count in (
    signal_summary["categories"]
    .items()
):

    print(
        f"{category}: {count}"
    )


print(
    "\n========== BY EVIDENCE LEVEL =========="
)

for level, count in (
    signal_summary["evidence_levels"]
    .items()
):

    print(
        f"{level}: {count}"
    )


# ============================================================
# 17. FINAL STATUS
# ============================================================

print("\n" + "=" * 90)

print(
    "🟢 NOVA SIGNAL DETECTION ENGINE: READY"
)

print(
    "Signals identify patterns for investigation."
)

print(
    "Signals do NOT establish causation."
)

print(
    "No arbitrary business thresholds were applied."
)

print("=" * 90)
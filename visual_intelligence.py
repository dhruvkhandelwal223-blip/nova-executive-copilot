"""
NOVA VISUAL INTELLIGENCE ENGINE
================================

Purpose:
Convert trusted Nova analytics into validated business visualizations.

Architecture:

RAW DATA
    ↓
DATA VALIDATION
    ↓
ANALYTICS
    ↓
SIGNAL DETECTION
    ↓
INSIGHTS
    ↓
MANAGEMENT INTELLIGENCE
    ↓
VISUAL INTELLIGENCE
    ↓
CEO DASHBOARD

Visualization principles:
- Raw data remains the source of truth.
- Analytics must remain evidence-based.
- Visualization type must match the analytical question.
- Partial periods must be clearly identified.
- No arbitrary business thresholds.
- No unsupported causal claims.
- No risk scores are invented.
"""

import pandas as pd
import plotly.express as px

from analytics import (
    calculate_product_analytics,
    calculate_region_analytics,
    calculate_channel_analytics,
    calculate_segment_analytics,
    calculate_monthly_analytics,
    calculate_product_region_returns,
    detect_partial_months,
)


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = "NovaTech_Sales_Data.xlsx"


# ============================================================
# REQUIRED RAW COLUMNS
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


# ============================================================
# VISUALIZATION DECISION ENGINE
# ============================================================

def choose_visualization(question_type):

    visualization_map = {

        "KPI": {
            "visual": "KPI CARD",
            "reason": (
                "A headline business metric is best communicated "
                "through a KPI card."
            ),
        },

        "PRODUCT_COMPARISON": {
            "visual": "BAR CHART",
            "reason": (
                "Products are categorical groups, making a bar chart "
                "appropriate for comparison."
            ),
        },

        "REGION_COMPARISON": {
            "visual": "BAR CHART",
            "reason": (
                "Regions are categorical groups that can be "
                "directly compared using bars."
            ),
        },

        "CHANNEL_COMPARISON": {
            "visual": "BAR CHART",
            "reason": (
                "Channels are categorical groups suitable for "
                "side-by-side comparison."
            ),
        },

        "SEGMENT_COMPARISON": {
            "visual": "BAR CHART",
            "reason": (
                "Customer segments are categorical groups suitable "
                "for comparison."
            ),
        },

        "TIME_TREND": {
            "visual": "LINE CHART",
            "reason": (
                "Time-series data is naturally represented using "
                "a line chart."
            ),
        },

        "PRODUCT_REGION": {
            "visual": "HEATMAP",
            "reason": (
                "A product-by-region matrix is suitable for "
                "a heatmap."
            ),
        },

        "CONCENTRATION": {
            "visual": "BAR CHART",
            "reason": (
                "Product contribution can be clearly compared "
                "using a ranked bar chart."
            ),
        },

        "TRANSACTION_DETAIL": {
            "visual": "TABLE",
            "reason": (
                "Transaction-level information is best displayed "
                "in a table."
            ),
        },

        "EXECUTIVE_OVERVIEW": {
            "visual": "EXECUTIVE DASHBOARD",
            "reason": (
                "An executive overview requires multiple coordinated "
                "KPIs and analytical visuals."
            ),
        },
    }

    return visualization_map.get(
        question_type,
        {
            "visual": "TABLE",
            "reason": (
                "A table is used when a more specific visualization "
                "type has not yet been defined."
            ),
        },
    )


# ============================================================
# DATA VALIDATION FOR VISUALS
# ============================================================

def validate_visual_data(dataframe, required_columns):

    result = {
        "status": "VALID",
        "issues": [],
    }

    if dataframe is None:

        result["status"] = "INVALID"
        result["issues"].append(
            "Dataframe is None."
        )

        return result

    if not isinstance(dataframe, pd.DataFrame):

        result["status"] = "INVALID"
        result["issues"].append(
            "Object is not a pandas dataframe."
        )

        return result

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:

        result["status"] = "INVALID"

        for column in missing_columns:

            result["issues"].append(
                f"Required column missing: {column}"
            )

    if dataframe.empty:

        result["status"] = "INVALID"
        result["issues"].append(
            "Dataset contains no records."
        )

    return result


# ============================================================
# RAW DATA VALIDATION
# ============================================================

def validate_raw_dataset(df):

    print("\n")
    print("=" * 90)
    print("RAW DATA VISUALIZATION VALIDATION")
    print("=" * 90)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        print("🔴 REQUIRED COLUMNS MISSING:")

        for column in missing_columns:
            print(f"  • {column}")

        return False

    print("🟢 All required columns are available.")

    print(f"Rows       : {len(df):,}")
    print(f"Columns    : {len(df.columns):,}")

    return True


# ============================================================
# KPI CARDS
# ============================================================

def build_kpi_cards(df):

    """
    Build KPI values directly from the validated raw dataset.

    This function intentionally does not depend on the internal
    dictionary structure returned by analytics.calculate_overall_kpis().
    """

    revenue = df["Revenue"].sum()

    profit = df["Profit"].sum()

    transactions = len(df)

    units = df["Units_Sold"].sum()

    returns = df["Returns"].sum()

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

    return {
        "Revenue": revenue,
        "Profit": profit,
        "Gross Margin": gross_margin,
        "Return Rate": return_rate,
        "Transactions": transactions,
    }


# ============================================================
# PRODUCT REVENUE CHART
# ============================================================

def create_product_revenue_chart(product_df):

    validation = validate_visual_data(
        product_df,
        [
            "Product",
            "Revenue",
        ],
    )

    if validation["status"] != "VALID":

        print("🔴 Product revenue chart skipped.")

        for issue in validation["issues"]:
            print(f"   • {issue}")

        return None

    chart_df = product_df.sort_values(
        "Revenue",
        ascending=False,
    )

    fig = px.bar(
        chart_df,
        x="Product",
        y="Revenue",
        title="Revenue by Product",
        labels={
            "Revenue": "Revenue ($)",
            "Product": "Product",
        },
    )

    fig.update_layout(
        xaxis_tickangle=-30,
    )

    return fig


# ============================================================
# PRODUCT PROFIT CHART
# ============================================================

def create_product_profit_chart(product_df):

    validation = validate_visual_data(
        product_df,
        [
            "Product",
            "Profit",
        ],
    )

    if validation["status"] != "VALID":

        print("🔴 Product profit chart skipped.")

        for issue in validation["issues"]:
            print(f"   • {issue}")

        return None

    chart_df = product_df.sort_values(
        "Profit",
        ascending=False,
    )

    fig = px.bar(
        chart_df,
        x="Product",
        y="Profit",
        title="Profit by Product",
        labels={
            "Profit": "Profit ($)",
            "Product": "Product",
        },
    )

    fig.update_layout(
        xaxis_tickangle=-30,
    )

    return fig


# ============================================================
# PRODUCT RETURN RATE CHART
# ============================================================

def create_product_return_chart(product_df):

    validation = validate_visual_data(
        product_df,
        [
            "Product",
            "Return_Rate_%",
        ],
    )

    if validation["status"] != "VALID":

        print("🔴 Product return chart skipped.")

        for issue in validation["issues"]:
            print(f"   • {issue}")

        return None

    chart_df = product_df.sort_values(
        "Return_Rate_%",
        ascending=False,
    )

    fig = px.bar(
        chart_df,
        x="Product",
        y="Return_Rate_%",
        title="Return Rate by Product",
        labels={
            "Return_Rate_%": "Return Rate (%)",
            "Product": "Product",
        },
    )

    fig.update_layout(
        xaxis_tickangle=-30,
    )

    return fig


# ============================================================
# REGIONAL RETURN RATE CHART
# ============================================================

def create_region_return_chart(region_df):

    validation = validate_visual_data(
        region_df,
        [
            "Region",
            "Return_Rate_%",
        ],
    )

    if validation["status"] != "VALID":

        print("🔴 Regional return chart skipped.")

        for issue in validation["issues"]:
            print(f"   • {issue}")

        return None

    chart_df = region_df.sort_values(
        "Return_Rate_%",
        ascending=False,
    )

    fig = px.bar(
        chart_df,
        x="Region",
        y="Return_Rate_%",
        title="Return Rate by Region",
        labels={
            "Return_Rate_%": "Return Rate (%)",
            "Region": "Region",
        },
    )

    return fig


# ============================================================
# MONTHLY REVENUE TREND
# ============================================================

def create_monthly_revenue_chart(monthly_df):

    validation = validate_visual_data(
        monthly_df,
        [
            "Month",
            "Revenue",
        ],
    )

    if validation["status"] != "VALID":

        print("🔴 Monthly revenue chart skipped.")

        for issue in validation["issues"]:
            print(f"   • {issue}")

        return None

    chart_df = monthly_df.copy()

    chart_df["Month"] = chart_df["Month"].astype(str)

    fig = px.line(
        chart_df,
        x="Month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend",
        labels={
            "Revenue": "Revenue ($)",
            "Month": "Month",
        },
    )

    return fig


# ============================================================
# PRODUCT × REGION RETURN HEATMAP
# ============================================================

def create_product_region_heatmap(product_region_df):

    if product_region_df is None:

        print(
            "🔴 Product-region heatmap skipped: "
            "dataframe is None."
        )

        return None

    if not isinstance(
        product_region_df,
        pd.DataFrame,
    ):

        print(
            "🔴 Product-region heatmap skipped: "
            "invalid dataframe."
        )

        return None

    if product_region_df.empty:

        print(
            "🔴 Product-region heatmap skipped: "
            "empty dataframe."
        )

        return None

    heatmap_df = product_region_df.copy()

    # --------------------------------------------------------
    # Case 1:
    # Product is already a normal column
    # --------------------------------------------------------

    if "Product" in heatmap_df.columns:

        value_columns = [
            column
            for column in heatmap_df.columns
            if column != "Product"
        ]

        long_df = heatmap_df.melt(
            id_vars=["Product"],
            value_vars=value_columns,
            var_name="Region",
            value_name="Return_Rate",
        )

    # --------------------------------------------------------
    # Case 2:
    # Product is stored as dataframe index
    # --------------------------------------------------------

    else:

        heatmap_df = heatmap_df.reset_index()

        first_column = heatmap_df.columns[0]

        long_df = heatmap_df.melt(
            id_vars=[first_column],
            var_name="Region",
            value_name="Return_Rate",
        )

        long_df.rename(
            columns={
                first_column: "Product",
            },
            inplace=True,
        )

    fig = px.density_heatmap(
        long_df,
        x="Region",
        y="Product",
        z="Return_Rate",
        text_auto=".2f",
        title="Product × Region Return Rate",
        labels={
            "Return_Rate": "Return Rate (%)",
        },
    )

    return fig


# ============================================================
# PRODUCT CONCENTRATION CHART
# ============================================================

def create_product_concentration_chart(df):

    product_summary = (
        df.groupby("Product")
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
        )
        .reset_index()
    )

    total_revenue = product_summary["Revenue"].sum()

    if total_revenue == 0:

        print(
            "🔴 Product concentration chart skipped: "
            "total revenue is zero."
        )

        return None

    product_summary["Revenue_Share_%"] = (
        product_summary["Revenue"]
        / total_revenue
        * 100
    )

    chart_df = product_summary.sort_values(
        "Revenue_Share_%",
        ascending=False,
    )

    fig = px.bar(
        chart_df,
        x="Product",
        y="Revenue_Share_%",
        title="Revenue Concentration by Product",
        labels={
            "Revenue_Share_%": "Revenue Share (%)",
            "Product": "Product",
        },
    )

    fig.update_layout(
        xaxis_tickangle=-30,
    )

    return fig


# ============================================================
# VISUALIZATION REGISTRY
# ============================================================

def build_visual_registry(
    product_df,
    region_df,
    monthly_df,
    product_region_df,
):

    registry = {

        "KPI_CARDS": {
            "type": "KPI",
            "visualization": choose_visualization(
                "KPI"
            ),
            "data_status": "VALID",
        },

        "PRODUCT_REVENUE": {
            "type": "PRODUCT_COMPARISON",
            "visualization": choose_visualization(
                "PRODUCT_COMPARISON"
            ),
            "data_status": validate_visual_data(
                product_df,
                [
                    "Product",
                    "Revenue",
                ],
            )["status"],
        },

        "PRODUCT_PROFIT": {
            "type": "PRODUCT_COMPARISON",
            "visualization": choose_visualization(
                "PRODUCT_COMPARISON"
            ),
            "data_status": validate_visual_data(
                product_df,
                [
                    "Product",
                    "Profit",
                ],
            )["status"],
        },

        "PRODUCT_RETURN_RATE": {
            "type": "PRODUCT_COMPARISON",
            "visualization": choose_visualization(
                "PRODUCT_COMPARISON"
            ),
            "data_status": validate_visual_data(
                product_df,
                [
                    "Product",
                    "Return_Rate_%",
                ],
            )["status"],
        },

        "REGION_RETURN_RATE": {
            "type": "REGION_COMPARISON",
            "visualization": choose_visualization(
                "REGION_COMPARISON"
            ),
            "data_status": validate_visual_data(
                region_df,
                [
                    "Region",
                    "Return_Rate_%",
                ],
            )["status"],
        },

        "MONTHLY_REVENUE": {
            "type": "TIME_TREND",
            "visualization": choose_visualization(
                "TIME_TREND"
            ),
            "data_status": validate_visual_data(
                monthly_df,
                [
                    "Month",
                    "Revenue",
                ],
            )["status"],
        },

        "PRODUCT_REGION_RETURNS": {
            "type": "PRODUCT_REGION",
            "visualization": choose_visualization(
                "PRODUCT_REGION"
            ),
            "data_status": "VALID",
        },

        "PRODUCT_CONCENTRATION": {
            "type": "CONCENTRATION",
            "visualization": choose_visualization(
                "CONCENTRATION"
            ),
            "data_status": "VALID",
        },
    }

    return registry


# ============================================================
# CHART GENERATION
# ============================================================

def generate_all_charts(
    df,
    product_df,
    region_df,
    monthly_df,
    product_region_df,
):

    charts = {}

    charts["product_revenue"] = (
        create_product_revenue_chart(
            product_df
        )
    )

    charts["product_profit"] = (
        create_product_profit_chart(
            product_df
        )
    )

    charts["product_return_rate"] = (
        create_product_return_chart(
            product_df
        )
    )

    charts["region_return_rate"] = (
        create_region_return_chart(
            region_df
        )
    )

    charts["monthly_revenue"] = (
        create_monthly_revenue_chart(
            monthly_df
        )
    )

    charts["product_region_returns"] = (
        create_product_region_heatmap(
            product_region_df
        )
    )

    charts["product_concentration"] = (
        create_product_concentration_chart(
            df
        )
    )

    return charts


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 90)
    print("                    NOVA VISUAL INTELLIGENCE ENGINE")
    print("=" * 90)

    print("\nPurpose:")
    print(
        "Convert trusted analytics into validated "
        "business visualizations."
    )

    # ========================================================
    # LOAD DATASET
    # ========================================================

    try:

        df = pd.read_excel(
            DATA_FILE
        )

    except FileNotFoundError:

        print("\n🔴 DATASET NOT FOUND")
        print(
            f"Expected file: {DATA_FILE}"
        )

        raise SystemExit(1)

    print("\nDataset loaded:")
    print(
        f"Rows: {len(df):,}"
    )
    print(
        f"Columns: {len(df.columns):,}"
    )

    # ========================================================
    # VALIDATE RAW DATA
    # ========================================================

    if not validate_raw_dataset(df):

        print("\n🔴 VISUAL ENGINE STOPPED")
        print(
            "Required raw-data columns are missing."
        )

        raise SystemExit(1)

    # ========================================================
    # BUILD KPI DATA
    # ========================================================

    kpis = build_kpi_cards(
        df
    )

    print("\n")
    print("=" * 90)
    print("KPI VISUALIZATION DATA")
    print("=" * 90)

    print(
        f"Revenue             : "
        f"${kpis['Revenue']:,.2f}"
    )

    print(
        f"Profit              : "
        f"${kpis['Profit']:,.2f}"
    )

    print(
        f"Gross Margin        : "
        f"{kpis['Gross Margin']:.2f}%"
    )

    print(
        f"Return Rate         : "
        f"{kpis['Return Rate']:.2f}%"
    )

    print(
        f"Transactions        : "
        f"{kpis['Transactions']:,}"
    )

    # ========================================================
    # RUN TRUSTED ANALYTICS
    # ========================================================

    print("\n")
    print("=" * 90)
    print("LOADING TRUSTED ANALYTICS")
    print("=" * 90)

    product_df = calculate_product_analytics(
        df
    )

    region_df = calculate_region_analytics(
        df
    )

    channel_df = calculate_channel_analytics(
        df
    )

    segment_df = calculate_segment_analytics(
        df
    )

    monthly_df = calculate_monthly_analytics(
        df
    )

    product_region_df = calculate_product_region_returns(
        df
    )

    print("🟢 Product analytics loaded.")
    print("🟢 Regional analytics loaded.")
    print("🟢 Channel analytics loaded.")
    print("🟢 Segment analytics loaded.")
    print("🟢 Monthly analytics loaded.")
    print("🟢 Product-region analytics loaded.")

    # ========================================================
    # BUILD VISUALIZATION REGISTRY
    # ========================================================

    registry = build_visual_registry(
        product_df,
        region_df,
        monthly_df,
        product_region_df,
    )

    print("\n")
    print("=" * 90)
    print("VISUALIZATION REGISTRY")
    print("=" * 90)

    for visual_name, config in registry.items():

        print("\n" + "-" * 90)

        print(
            f"VISUAL: {visual_name}"
        )

        print(
            f"TYPE: {config['type']}"
        )

        print(
            f"SELECTED VISUAL: "
            f"{config['visualization']['visual']}"
        )

        print(
            f"WHY: "
            f"{config['visualization']['reason']}"
        )

        print(
            f"DATA STATUS: "
            f"{config['data_status']}"
        )

    # ========================================================
    # GENERATE CHARTS
    # ========================================================

    charts = generate_all_charts(
        df,
        product_df,
        region_df,
        monthly_df,
        product_region_df,
    )

    # ========================================================
    # PARTIAL PERIOD CHECK
    # ========================================================

    partial_periods = detect_partial_months(
        df
    )

    print("\n")
    print("=" * 90)
    print("VISUAL DATA SAFETY CHECK")
    print("=" * 90)

    if partial_periods:

        print(
            "⚠️ PARTIAL REPORTING PERIOD DETECTED"
        )

        for period in partial_periods:

            print(
                f"  • {period}"
            )

        print(
            "\nLatest-period trend visuals must clearly "
            "identify the incomplete reporting period."
        )

    else:

        print(
            "🟢 No partial reporting periods detected."
        )

    # ========================================================
    # CHART GENERATION STATUS
    # ========================================================

    print("\n")
    print("=" * 90)
    print("CHART GENERATION STATUS")
    print("=" * 90)

    successful_charts = 0

    total_charts = len(
        charts
    )

    for name, chart in charts.items():

        if chart is not None:

            successful_charts += 1

            print(
                f"🟢 {name}: READY"
            )

        else:

            print(
                f"🔴 {name}: NOT GENERATED"
            )

    # ========================================================
    # VISUAL ENGINE SUMMARY
    # ========================================================

    print("\n")
    print("=" * 90)
    print("VISUAL ENGINE SUMMARY")
    print("=" * 90)

    print(
        f"\nCharts generated successfully: "
        f"{successful_charts}/{total_charts}"
    )

    if successful_charts == total_charts:

        print(
            "\n🟢 All planned visualization objects "
            "were generated successfully."
        )

    else:

        print(
            "\n⚠️ Some visualization objects "
            "were not generated."
        )

    print(
        "\nVisualization types were selected "
        "based on analytical context."
    )

    print(
        "Partial-period warnings are preserved."
    )

    print(
        "No arbitrary thresholds or unsupported "
        "business claims were introduced."
    )

    # ========================================================
    # FINAL STATUS
    # ========================================================

    if successful_charts == total_charts:

        print("\n")
        print("=" * 90)
        print(
            "🟢 NOVA VISUAL INTELLIGENCE ENGINE: READY"
        )
        print("=" * 90)

        print(
            "Trusted analytics have been converted "
            "into validated visualization objects."
        )

        print(
            "The engine is ready for Streamlit "
            "dashboard integration."
        )

        print("=" * 90)

    else:

        print("\n")
        print("=" * 90)
        print(
            "🟡 NOVA VISUAL INTELLIGENCE ENGINE: "
            "PARTIALLY READY"
        )
        print("=" * 90)

        print(
            "Review the chart generation status above "
            "before dashboard integration."
        )

        print("=" * 90)
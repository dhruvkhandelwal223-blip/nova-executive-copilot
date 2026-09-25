# ============================================================
# NOVA — EXECUTIVE COPILOT
# Frontend V2 — Stitch-Inspired Executive Intelligence UI
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from question_engine import ask_nova
from ceo_brief import generate_ceo_brief

from nova_ui import (
    apply_nova_theme,
    render_brand,
    command_bar,
    section_header,
    epistemic_badge,
    kpi_card,
    signal_card,
    trust_panel,
    scope_bar,
    knowledge_panel,
    nova_footer,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NOVA — Executive Copilot",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_nova_theme()


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    data = pd.read_excel("NovaTech_Sales_Data.xlsx")

    required = [
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

    missing = [column for column in required if column not in data.columns]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    numeric_columns = [
        "Units_Sold",
        "Revenue",
        "Cost",
        "Profit",
        "Returns",
        "Customer_Rating",
        "Gross_Margin_%",
        "Return_Rate_%",
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    return data


try:
    df = load_data()
except Exception as exc:
    st.error("NOVA could not load the validated sales dataset.")
    st.code(str(exc))
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "active_view" not in st.session_state:
    st.session_state.active_view = "Command Center"

if "ask_result" not in st.session_state:
    st.session_state.ask_result = None


# ============================================================
# HELPERS
# ============================================================

def safe_percentage(numerator, denominator):
    try:
        denominator_value = float(denominator)
        if denominator_value == 0:
            return 0.0
        return (float(numerator) / denominator_value) * 100
    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0


def calculate_scope_metrics(data):
    revenue = float(data["Revenue"].sum())
    profit = float(data["Profit"].sum())
    units = float(data["Units_Sold"].sum())
    returns = float(data["Returns"].sum())
    transactions = int(len(data))

    return {
        "revenue": revenue,
        "profit": profit,
        "units": units,
        "returns": returns,
        "transactions": transactions,
        "margin": safe_percentage(profit, revenue),
        "return_rate": safe_percentage(returns, units),
    }


def result_value(result, *keys, default=""):
    if isinstance(result, dict):
        for key in keys:
            value = result.get(key)
            if value not in (None, ""):
                return value
    return default


def display_value(value):
    if isinstance(value, (list, tuple)):
        return "\n".join(f"• {item}" for item in value)
    return value


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    render_brand()

    st.caption("NAVIGATION")

    navigation_items = [
        "Command Center",
        "CEO Brief",
        "Ask Nova",
        "Performance",
        "Signals",
        "Investigations",
        "Data Trust",
    ]

    for item in navigation_items:
        button_type = "primary" if st.session_state.active_view == item else "secondary"

        if st.button(
            item,
            key=f"nav_{item}",
            use_container_width=True,
            type=button_type,
        ):
            st.session_state.active_view = item
            st.rerun()

    st.markdown("---")
    st.caption("DATA SCOPE")

    product_options = ["All"] + sorted(
        df["Product"].dropna().unique().tolist()
    )
    region_options = ["All"] + sorted(
        df["Region"].dropna().unique().tolist()
    )
    channel_options = ["All"] + sorted(
        df["Channel"].dropna().unique().tolist()
    )
    segment_options = ["All"] + sorted(
        df["Customer_Segment"].dropna().unique().tolist()
    )

    selected_product = st.selectbox(
        "Product",
        product_options,
        key="scope_product",
    )

    selected_region = st.selectbox(
        "Region",
        region_options,
        key="scope_region",
    )

    selected_channel = st.selectbox(
        "Channel",
        channel_options,
        key="scope_channel",
    )

    selected_segment = st.selectbox(
        "Customer Segment",
        segment_options,
        key="scope_segment",
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_product != "All":
    filtered_df = filtered_df[
        filtered_df["Product"] == selected_product
    ]

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_channel != "All":
    filtered_df = filtered_df[
        filtered_df["Channel"] == selected_channel
    ]

if selected_segment != "All":
    filtered_df = filtered_df[
        filtered_df["Customer_Segment"] == selected_segment
    ]


# ============================================================
# CURRENT SCOPE
# ============================================================

metrics = calculate_scope_metrics(filtered_df)

revenue = metrics["revenue"]
profit = metrics["profit"]
units = metrics["units"]
returns = metrics["returns"]
transactions = metrics["transactions"]
margin = metrics["margin"]
return_rate = metrics["return_rate"]

if not df.empty and df["Date"].notna().any():
    min_date = df["Date"].min().strftime("%d %b %Y")
    max_date = df["Date"].max().strftime("%d %b %Y")
    date_range = f"{min_date} → {max_date}"
else:
    date_range = "Date range unavailable"

filter_parts = []
for label, value in [
    ("Product", selected_product),
    ("Region", selected_region),
    ("Channel", selected_channel),
    ("Segment", selected_segment),
]:
    if value != "All":
        filter_parts.append(f"{label}: {value}")

filter_summary = "All available records" if not filter_parts else " • ".join(filter_parts)


# ============================================================
# MANAGEMENT SIGNALS
# ============================================================

buds_df = filtered_df[filtered_df["Product"] == "NovaBuds X"]
watch_df = filtered_df[filtered_df["Product"] == "NovaWatch Pro"]
east_df = filtered_df[filtered_df["Region"] == "East"]

buds_return_rate = safe_percentage(
    buds_df["Returns"].sum(),
    buds_df["Units_Sold"].sum(),
)

watch_revenue_share = safe_percentage(
    watch_df["Revenue"].sum(),
    revenue,
)

east_return_rate = safe_percentage(
    east_df["Returns"].sum(),
    east_df["Units_Sold"].sum(),
)


# ============================================================
# TOP COMMAND BAR + SCOPE BAR
# ============================================================

command_bar(
    active_view=st.session_state.active_view,
    record_count=transactions,
)

scope_bar(
    product=selected_product,
    region=selected_region,
    channel=selected_channel,
    segment=selected_segment,
    records=transactions,
    date_range=date_range,
    filters=filter_summary,
)


# ============================================================
# COMMAND CENTER
# ============================================================

def render_command_center():
    section_header(
        "Command Center",
        "Executive overview of the validated NovaTech sales dataset.",
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        kpi_card(
            "Revenue",
            f"${revenue:,.0f}",
            "Validated financial metric",
            "FACT",
        )

    with col2:
        kpi_card(
            "Profit",
            f"${profit:,.0f}",
            "Calculated from transaction data",
            "CALCULATION",
        )

    with col3:
        kpi_card(
            "Gross Margin",
            f"{margin:.2f}%",
            "Profit ÷ Revenue",
            "CALCULATION",
        )

    with col4:
        kpi_card(
            "Return Rate",
            f"{return_rate:.2f}%",
            "Returns ÷ Units Sold",
            "CALCULATION",
        )

    with col5:
        kpi_card(
            "Transactions",
            f"{transactions:,}",
            "Records in current scope",
            "FACT",
        )

    st.markdown("")

    section_header(
        "Management Signals",
        "Validated patterns requiring attention or investigation.",
    )

    signal_col1, signal_col2, signal_col3 = st.columns(3)

    with signal_col1:
        signal_card(
            title="NovaBuds X Return Rate",
            metric=f"{buds_return_rate:.2f}%",
            description=(
                "NovaBuds X return rate within the current "
                "validated dataset scope."
            ),
            status="VALIDATED PATTERN",
        )

    with signal_col2:
        signal_card(
            title="NovaWatch Pro Revenue Share",
            metric=f"{watch_revenue_share:.2f}%",
            description=(
                "Share of current-scope revenue generated "
                "by NovaWatch Pro."
            ),
            status="VALIDATED PATTERN",
        )

    with signal_col3:
        signal_card(
            title="East Region Return Rate",
            metric=f"{east_return_rate:.2f}%",
            description=(
                "Observed East-region return rate. "
                "The dataset does not establish the cause."
            ),
            status="INVESTIGATION REQUIRED",
        )

    st.markdown("")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        section_header(
            "Revenue by Product",
            "Current filtered scope.",
        )

        if filtered_df.empty:
            st.info("No product data available for the current scope.")
        else:
            product_chart = (
                filtered_df.groupby("Product", as_index=False)
                .agg(Revenue=("Revenue", "sum"))
                .sort_values("Revenue", ascending=False)
            )

            fig = px.bar(
                product_chart,
                x="Product",
                y="Revenue",
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=20, b=20),
                height=350,
                xaxis_title=None,
                yaxis_title="Revenue",
            )
            st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        section_header(
            "Return Rate by Region",
            "Descriptive regional return behavior.",
        )

        if filtered_df.empty:
            st.info("No regional data available.")
        else:
            regional_chart = (
                filtered_df.groupby("Region", as_index=False)
                .agg(
                    Units=("Units_Sold", "sum"),
                    Returns=("Returns", "sum"),
                )
            )

            regional_chart["Return Rate"] = (
                regional_chart["Returns"]
                / regional_chart["Units"].replace(0, pd.NA)
                * 100
            ).fillna(0)

            fig = px.bar(
                regional_chart,
                x="Region",
                y="Return Rate",
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=20, b=20),
                height=350,
                xaxis_title=None,
                yaxis_title="Return Rate (%)",
            )
            st.plotly_chart(fig, use_container_width=True)


# ============================================================
# CEO BRIEF
# ============================================================

def render_ceo_brief():
    section_header(
        "CEO Brief",
        "Evidence-backed executive summary from the current dataset scope.",
    )

    epistemic_badge(
        "FACT",
        "Evidence hierarchy active",
    )

    if filtered_df.empty:
        st.warning("No records are available in the current scope.")
        return

    with st.spinner("Generating executive brief..."):
        brief = generate_ceo_brief(filtered_df)

    if isinstance(brief, dict):
        snapshot = result_value(
            brief,
            "executive_snapshot",
            "snapshot",
            "executive_summary",
        )
        validated_signals = result_value(
            brief,
            "validated_signals",
            "signals",
        )
        what_we_know = result_value(
            brief,
            "what_we_know",
            "known",
        )
        what_we_do_not_know = result_value(
            brief,
            "what_we_do_not_know",
            "unknowns",
        )
        investigate_next = result_value(
            brief,
            "investigate_next",
            "investigation",
        )

        if snapshot:
            st.markdown("### Executive Snapshot")
            st.write(display_value(snapshot))

        if validated_signals:
            st.markdown("### Validated Signals")
            st.write(display_value(validated_signals))

        if what_we_know:
            knowledge_panel(
                "What NOVA Knows",
                display_value(what_we_know),
                "FACT / CALCULATION / VALIDATED PATTERN",
            )

        if what_we_do_not_know:
            knowledge_panel(
                "What NOVA Does Not Know",
                display_value(what_we_do_not_know),
                "INVESTIGATION REQUIRED",
            )

        if investigate_next:
            knowledge_panel(
                "Investigate Next",
                display_value(investigate_next),
                "NEXT INVESTIGATION",
            )

    else:
        st.write(brief)

    trust_panel(
        title="Evidence Boundary",
        message=(
            "NOVA interprets information supported by the validated "
            "NovaTech sales dataset. Operational causes outside the "
            "current transaction schema are not asserted as facts."
        ),
    )


# ============================================================
# ASK NOVA
# ============================================================

def render_ask_nova():
    section_header(
        "Ask Nova",
        "Conversational business intelligence against the current scope.",
    )

    epistemic_badge(
        "FACT",
        "Evidence-first answering",
    )

    st.markdown("### Conversational BI")
    st.caption(
        "Ask a business question. NOVA separates evidence, "
        "calculation, interpretation and investigation."
    )

    question = st.text_input(
        "Ask NOVA",
        placeholder="Example: Which product has the highest return rate?",
        key="nova_question",
    )

    ask_button = st.button(
        "Analyze with NOVA",
        type="primary",
        use_container_width=False,
    )

    if ask_button:
        if not question.strip():
            st.warning("Please enter a business question.")
        elif filtered_df.empty:
            st.warning("No records are available in the current scope.")
        else:
            with st.spinner("NOVA is analyzing the validated dataset..."):
                st.session_state.ask_result = ask_nova(
                    question,
                    filtered_df,
                )

    result = st.session_state.ask_result

    if result is None:
        st.markdown("#### Suggested Questions")
        suggestion_col1, suggestion_col2 = st.columns(2)

        with suggestion_col1:
            st.info("Which product has the highest return rate?")
            st.info("Which product generates the most revenue?")

        with suggestion_col2:
            st.info("Which region has the highest return rate?")
            st.info("What should management investigate?")
        return

    st.markdown("---")

    if isinstance(result, dict):
        answer = result_value(result, "answer", default="")
        evidence = result_value(result, "evidence", default="")
        interpretation = result_value(
            result,
            "interpretation",
            default="",
        )
        confidence = result_value(
            result,
            "confidence",
            default="",
        )
        unknowns = result_value(
            result,
            "unknowns",
            "what_we_do_not_know",
            default="",
        )
        investigation = result_value(
            result,
            "investigation",
            "suggested_next_investigation",
            default="",
        )
        status = result_value(
            result,
            "status",
            default="FACT",
        )

        st.markdown("### NOVA Answer")
        epistemic_badge(status, "Answer classification")
        st.write(display_value(answer))

        if evidence:
            knowledge_panel(
                "Empirical Evidence",
                display_value(evidence),
                "SOURCE DATA",
            )

        if interpretation:
            knowledge_panel(
                "Interpretation",
                display_value(interpretation),
                "INTERPRETATION",
            )

        if confidence:
            knowledge_panel(
                "Confidence",
                display_value(confidence),
                "MODEL OUTPUT",
            )

        if unknowns:
            knowledge_panel(
                "What NOVA Does Not Know",
                display_value(unknowns),
                "UNKNOWN",
            )

        if investigation:
            knowledge_panel(
                "Suggested Next Investigation",
                display_value(investigation),
                "INVESTIGATION REQUIRED",
            )

    else:
        st.write(result)

    trust_panel(
        title="NOVA Trust Boundary",
        message=(
            "NOVA does not invent external operational systems, "
            "unavailable metrics or causal explanations."
        ),
    )


# ============================================================
# PERFORMANCE
# ============================================================

def render_performance():
    section_header(
        "Performance",
        "Detailed financial, product and regional performance.",
    )

    product_tab, region_tab, trend_tab = st.tabs(
        ["Products", "Regions", "Trend"]
    )

    with product_tab:
        if filtered_df.empty:
            st.info("No product data available.")
        else:
            product_perf = (
                filtered_df.groupby("Product", as_index=False)
                .agg(
                    Revenue=("Revenue", "sum"),
                    Profit=("Profit", "sum"),
                    Units=("Units_Sold", "sum"),
                    Returns=("Returns", "sum"),
                )
            )

            product_perf["Margin %"] = (
                product_perf["Profit"]
                / product_perf["Revenue"].replace(0, pd.NA)
                * 100
            ).fillna(0)

            product_perf["Return Rate %"] = (
                product_perf["Returns"]
                / product_perf["Units"].replace(0, pd.NA)
                * 100
            ).fillna(0)

            st.dataframe(
                product_perf,
                use_container_width=True,
                hide_index=True,
            )

    with region_tab:
        if filtered_df.empty:
            st.info("No regional data available.")
        else:
            region_perf = (
                filtered_df.groupby("Region", as_index=False)
                .agg(
                    Revenue=("Revenue", "sum"),
                    Profit=("Profit", "sum"),
                    Units=("Units_Sold", "sum"),
                    Returns=("Returns", "sum"),
                )
            )

            region_perf["Margin %"] = (
                region_perf["Profit"]
                / region_perf["Revenue"].replace(0, pd.NA)
                * 100
            ).fillna(0)

            region_perf["Return Rate %"] = (
                region_perf["Returns"]
                / region_perf["Units"].replace(0, pd.NA)
                * 100
            ).fillna(0)

            st.dataframe(
                region_perf,
                use_container_width=True,
                hide_index=True,
            )

    with trend_tab:
        if filtered_df.empty:
            st.info("No trend data available.")
        else:
            trend_df = filtered_df.copy()
            trend_df["Month"] = (
                trend_df["Date"]
                .dt.to_period("M")
                .astype(str)
            )

            monthly_summary = (
                trend_df.groupby("Month", as_index=False)
                .agg(
                    Revenue=("Revenue", "sum"),
                    Profit=("Profit", "sum"),
                )
            )

            fig = px.line(
                monthly_summary,
                x="Month",
                y="Revenue",
                markers=True,
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=20, b=20),
                height=400,
                yaxis_title="Revenue",
                xaxis_title=None,
            )

            st.plotly_chart(fig, use_container_width=True)

            st.caption(
                "Note: June 2026 is a partial period in the source dataset "
                "and should not be treated as a full-month comparison."
            )


# ============================================================
# SIGNALS
# ============================================================

def render_signals():
    section_header(
        "Signals",
        "Validated patterns and areas requiring further investigation.",
    )

    signal_card(
        title="NovaBuds X",
        metric=f"{buds_return_rate:.2f}%",
        description=(
            "Product-level return rate within the current scope."
        ),
        status="VALIDATED PATTERN",
    )

    signal_card(
        title="NovaWatch Pro",
        metric=f"{watch_revenue_share:.2f}%",
        description=(
            "Share of current-scope revenue."
        ),
        status="VALIDATED PATTERN",
    )

    signal_card(
        title="East Region",
        metric=f"{east_return_rate:.2f}%",
        description=(
            "Regional return rate requiring further investigation. "
            "The transaction data does not establish the cause."
        ),
        status="INVESTIGATION REQUIRED",
    )


# ============================================================
# INVESTIGATIONS
# ============================================================

def render_investigations():
    section_header(
        "Investigations",
        "Questions requiring evidence beyond the current sales ledger.",
    )

    knowledge_panel(
        "Return Drivers",
        (
            "The current transaction data identifies return patterns "
            "but does not establish the operational cause behind those returns."
        ),
        "INVESTIGATION REQUIRED",
    )

    knowledge_panel(
        "Customer Experience",
        (
            "Customer survey and CSAT information is not available "
            "in the current sales transaction schema."
        ),
        "NOT AVAILABLE",
    )

    knowledge_panel(
        "Hardware / Fit / Firmware",
        (
            "Hardware, fit and firmware defect information is not "
            "available in the current sales transaction schema."
        ),
        "NOT AVAILABLE",
    )

    knowledge_panel(
        "Regional Operations",
        (
            "The dataset can identify regional return-rate differences, "
            "but additional operational evidence would be required "
            "to determine why they occur."
        ),
        "INVESTIGATION REQUIRED",
    )


# ============================================================
# DATA TRUST
# ============================================================

def render_data_trust():
    section_header(
        "Data Trust",
        "Validation status and evidence boundaries.",
    )

    trust_panel(
        title="Data Integrity Verified",
        message=(
            "NOVA is operating on the validated NovaTech Sales Dataset."
        ),
    )

    trust_col1, trust_col2, trust_col3, trust_col4 = st.columns(4)

    with trust_col1:
        kpi_card(
            "Records",
            f"{len(df):,}",
            "Source transactions",
            "FACT",
        )

    with trust_col2:
        missing_values = int(df.isna().sum().sum())
        kpi_card(
            "Missing Values",
            f"{missing_values:,}",
            "Dataset validation",
            "FACT",
        )

    with trust_col3:
        duplicate_ids = int(df["Order_ID"].duplicated().sum())
        kpi_card(
            "Duplicate IDs",
            f"{duplicate_ids:,}",
            "Order ID validation",
            "FACT",
        )

    with trust_col4:
        negative_revenue = int((df["Revenue"] < 0).sum())
        kpi_card(
            "Negative Revenue",
            f"{negative_revenue:,}",
            "Revenue validation",
            "FACT",
        )

    calculated_profit = df["Revenue"] - df["Cost"]
    profit_variance = float(
        (calculated_profit - df["Profit"]).abs().max()
    )

    if profit_variance <= 0.01:
        profit_status = (
            "Profit arithmetic reconciles with Revenue minus Cost "
            "within a one-cent tolerance."
        )
    else:
        profit_status = (
            f"A maximum profit arithmetic variance of "
            f"${profit_variance:.4f} exists and requires review."
        )

    knowledge_panel(
        "Profit Arithmetic",
        profit_status,
        "VALIDATION",
    )

    invalid_returns = int(
        (df["Returns"] > df["Units_Sold"]).sum()
    )

    if invalid_returns == 0:
        return_status = (
            "No records contain returns exceeding units sold."
        )
    else:
        return_status = (
            f"{invalid_returns} records contain returns "
            "exceeding units sold."
        )

    knowledge_panel(
        "Return Integrity",
        return_status,
        "VALIDATION",
    )

    knowledge_panel(
        "Evidence Boundary",
        (
            "Raw transaction data is the authoritative source for "
            "NOVA's current analysis. External operational systems, "
            "unsupported causal explanations and unavailable business "
            "metrics are not treated as facts."
        ),
        "GOVERNANCE",
    )


# ============================================================
# ROUTER
# ============================================================

active_view = st.session_state.active_view

if active_view == "Command Center":
    render_command_center()
elif active_view == "CEO Brief":
    render_ceo_brief()
elif active_view == "Ask Nova":
    render_ask_nova()
elif active_view == "Performance":
    render_performance()
elif active_view == "Signals":
    render_signals()
elif active_view == "Investigations":
    render_investigations()
elif active_view == "Data Trust":
    render_data_trust()
else:
    st.session_state.active_view = "Command Center"
    st.rerun()


# ============================================================
# FOOTER
# ============================================================

nova_footer()

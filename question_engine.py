import pandas as pd


# ============================================================
# NOVA QUESTION ENGINE
# Scope-Aware + Management Intelligence V1
# ============================================================


# ============================================================
# CORE KPI ENGINE
# ============================================================

def calculate_kpis(df):

    if df.empty:
        return {
            "transactions": 0,
            "units": 0,
            "revenue": 0,
            "cost": 0,
            "profit": 0,
            "gross_margin": 0,
            "returns": 0,
            "return_rate": 0,
            "avg_rating": 0,
        }

    revenue = df["Revenue"].sum()
    cost = df["Cost"].sum()
    profit = df["Profit"].sum()
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

    avg_rating = (
        df["Customer_Rating"].mean()
        if "Customer_Rating" in df.columns
        else 0
    )

    return {
        "transactions": len(df),
        "units": units,
        "revenue": revenue,
        "cost": cost,
        "profit": profit,
        "gross_margin": gross_margin,
        "returns": returns,
        "return_rate": return_rate,
        "avg_rating": avg_rating,
    }


# ============================================================
# SCOPE DESCRIPTION
# ============================================================

def describe_scope(df):

    if df.empty:
        return "The current analysis scope contains no records."

    parts = []

    if "Product" in df.columns:
        products = df["Product"].dropna().unique()
        if len(products) == 1:
            parts.append(f"Product: {products[0]}")
        elif len(products) < df["Product"].nunique():
            parts.append(f"{len(products)} products")

    if "Region" in df.columns:
        regions = df["Region"].dropna().unique()
        if len(regions) == 1:
            parts.append(f"Region: {regions[0]}")

    if "Channel" in df.columns:
        channels = df["Channel"].dropna().unique()
        if len(channels) == 1:
            parts.append(f"Channel: {channels[0]}")

    if "Customer_Segment" in df.columns:
        segments = df["Customer_Segment"].dropna().unique()
        if len(segments) == 1:
            parts.append(f"Segment: {segments[0]}")

    if parts:
        return "Current scope: " + " | ".join(parts)

    return "Current scope: all available validated records."


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

def product_analysis(df):

    if df.empty:
        return pd.DataFrame()

    result = (
        df.groupby("Product")
        .agg(
            Transactions=("Order_ID", "count"),
            Units=("Units_Sold", "sum"),
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Returns=("Returns", "sum"),
            Rating=("Customer_Rating", "mean"),
        )
        .reset_index()
    )

    result["Margin_%"] = (
        result["Profit"] / result["Revenue"] * 100
    )

    result["Return_Rate_%"] = (
        result["Returns"] / result["Units"] * 100
    )

    return result


# ============================================================
# REGION ANALYSIS
# ============================================================

def region_analysis(df):

    if df.empty:
        return pd.DataFrame()

    result = (
        df.groupby("Region")
        .agg(
            Transactions=("Order_ID", "count"),
            Units=("Units_Sold", "sum"),
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Returns=("Returns", "sum"),
        )
        .reset_index()
    )

    result["Margin_%"] = (
        result["Profit"] / result["Revenue"] * 100
    )

    result["Return_Rate_%"] = (
        result["Returns"] / result["Units"] * 100
    )

    return result


# ============================================================
# MONTHLY ANALYSIS
# ============================================================

def monthly_analysis(df):

    if df.empty:
        return pd.DataFrame()

    temp = df.copy()
    temp["Date"] = pd.to_datetime(temp["Date"])

    result = (
        temp.groupby(temp["Date"].dt.to_period("M"))
        .agg(
            Transactions=("Order_ID", "count"),
            Units=("Units_Sold", "sum"),
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Returns=("Returns", "sum"),
        )
        .reset_index()
    )

    result["Month"] = result["Date"].astype(str)

    result["Margin_%"] = (
        result["Profit"] / result["Revenue"] * 100
    )

    result["Return_Rate_%"] = (
        result["Returns"] / result["Units"] * 100
    )

    return result


# ============================================================
# COMPARISON HELPERS
# ============================================================

def comparison_possible(series):

    return series.dropna().nunique() > 1


def highest_product(df, column):

    analysis = product_analysis(df)

    if analysis.empty:
        return None

    if len(analysis) == 1:
        return None

    row = analysis.loc[analysis[column].idxmax()]

    return row


def lowest_product(df, column):

    analysis = product_analysis(df)

    if analysis.empty:
        return None

    if len(analysis) == 1:
        return None

    row = analysis.loc[analysis[column].idxmin()]

    return row


# ============================================================
# PRODUCT RETURN QUESTION
# ============================================================

def answer_product_return_rate(df):

    analysis = product_analysis(df)

    if analysis.empty:
        return {
            "answer": "There is no data in the current analysis scope.",
            "evidence": "No records are available.",
            "interpretation": "No product-level conclusion can be made.",
            "confidence": "High",
            "unknowns": "No data is available in the current scope.",
        }

    if len(analysis) == 1:

        row = analysis.iloc[0]

        return {
            "answer": (
                f"Within the current analysis scope, "
                f"{row['Product']} has a return rate of "
                f"{row['Return_Rate_%']:.2f}%."
            ),
            "evidence": (
                f"{row['Product']} has "
                f"{int(row['Returns']):,} returns against "
                f"{int(row['Units']):,} units across "
                f"{int(row['Transactions']):,} transactions "
                f"in the current scope."
            ),
            "interpretation": (
                "The return rate is a validated pattern "
                "within the selected analysis scope. "
                "It can be used to identify an area for "
                "further investigation."
            ),
            "confidence": "High",
            "unknowns": (
                "The available sales data does not establish "
                "the cause of the returns."
            ),
        }

    row = analysis.loc[analysis["Return_Rate_%"].idxmax()]
    company_kpis = calculate_kpis(df)

    difference = (
        row["Return_Rate_%"] -
        company_kpis["return_rate"]
    )

    return {
        "answer": (
            f"Return rate for the current analysis scope is "
            f"{company_kpis['return_rate']:.2f}%. "
            f"The product with the highest return rate in "
            f"this scope is {row['Product']} at "
            f"{row['Return_Rate_%']:.2f}%."
        ),
        "evidence": (
            f"{row['Product']} has "
            f"{int(row['Returns']):,} returns against "
            f"{int(row['Units']):,} units. "
            f"This is {difference:+.2f} percentage points "
            f"versus the scope return rate."
        ),
        "interpretation": (
            "The product shows the strongest validated "
            "return-rate signal within the current scope. "
            "The available data does not establish the cause."
        ),
        "confidence": "High",
        "unknowns": (
            "The available sales data does not establish "
            "the cause of the returns."
        ),
    }


# ============================================================
# PRODUCT PERFORMANCE QUESTION
# ============================================================

def answer_product_performance(df):

    analysis = product_analysis(df)

    if analysis.empty:
        return {
            "answer": "There is no product data in the current scope.",
            "evidence": "No product records are available.",
            "interpretation": "No product performance conclusion can be made.",
            "confidence": "High",
            "unknowns": "No product data is available.",
        }

    if len(analysis) == 1:

        row = analysis.iloc[0]

        return {
            "answer": (
                f"{row['Product']} generated "
                f"${row['Revenue']:,.2f} revenue and "
                f"${row['Profit']:,.2f} profit in the current scope."
            ),
            "evidence": (
                f"Revenue: ${row['Revenue']:,.2f}; "
                f"Profit: ${row['Profit']:,.2f}; "
                f"Margin: {row['Margin_%']:.2f}%."
            ),
            "interpretation": (
                "The current scope contains only one product, "
                "so no product-level ranking is possible."
            ),
            "confidence": "High",
            "unknowns": (
                "A product comparison requires multiple products "
                "in the analysis scope."
            ),
        }

    revenue_row = analysis.loc[analysis["Revenue"].idxmax()]
    profit_row = analysis.loc[analysis["Profit"].idxmax()]

    return {
        "answer": (
            f"{revenue_row['Product']} has the highest revenue "
            f"at ${revenue_row['Revenue']:,.2f}, while "
            f"{profit_row['Product']} has the highest profit "
            f"at ${profit_row['Profit']:,.2f}."
        ),
        "evidence": (
            f"Highest revenue: {revenue_row['Product']} — "
            f"${revenue_row['Revenue']:,.2f}. "
            f"Highest profit: {profit_row['Product']} — "
            f"${profit_row['Profit']:,.2f}."
        ),
        "interpretation": (
            "Revenue and profit leadership should be evaluated "
            "separately because a product can lead on revenue "
            "without leading on profitability."
        ),
        "confidence": "High",
        "unknowns": (
            "The sales dataset does not establish the causal "
            "drivers behind product performance."
        ),
    }


# ============================================================
# MANAGEMENT INVESTIGATION
# ============================================================

def answer_management_investigation(df):

    if df.empty:
        return {
            "answer": "There is no data in the current analysis scope.",
            "evidence": "No records are available.",
            "interpretation": "Management investigation cannot be generated.",
            "confidence": "High",
            "unknowns": "The current scope contains no data.",
        }

    kpis = calculate_kpis(df)
    product_df = product_analysis(df)
    region_df = region_analysis(df)

    evidence_items = []
    investigation_items = []

    # --------------------------------------------------------
    # PRODUCT RETURN SIGNAL
    # --------------------------------------------------------

    if not product_df.empty:

        if len(product_df) > 1:

            row = product_df.loc[
                product_df["Return_Rate_%"].idxmax()
            ]

            evidence_items.append(
                "RETURN PERFORMANCE: "
                f"{row['Product']} has a "
                f"{row['Return_Rate_%']:.2f}% return rate. "
                f"Evidence: {int(row['Returns']):,} returns "
                f"against {int(row['Units']):,} units."
            )

            investigation_items.append(
                "Review return reasons, quality records, "
                "customer feedback, and operational logs "
                f"for {row['Product']}."
            )

        else:

            row = product_df.iloc[0]

            evidence_items.append(
                "RETURN PERFORMANCE: "
                f"{row['Product']} has a "
                f"{row['Return_Rate_%']:.2f}% return rate "
                "within the current scope."
            )

            investigation_items.append(
                "Review return reasons and customer feedback "
                f"for {row['Product']}."
            )

    # --------------------------------------------------------
    # CUSTOMER EXPERIENCE
    # --------------------------------------------------------

    if not product_df.empty:

        if len(product_df) > 1:

            row = product_df.loc[
                product_df["Rating"].idxmin()
            ]

            evidence_items.append(
                "CUSTOMER EXPERIENCE: "
                f"{row['Product']} has the lowest average "
                f"customer rating in the current scope at "
                f"{row['Rating']:.2f}."
            )

            investigation_items.append(
                "Review customer feedback and complaint "
                f"patterns for {row['Product']}."
            )

        else:

            row = product_df.iloc[0]

            evidence_items.append(
                "CUSTOMER EXPERIENCE: "
                f"{row['Product']} has an average customer "
                f"rating of {row['Rating']:.2f} in the current scope."
            )

            investigation_items.append(
                "Review customer feedback if a deeper "
                "customer-experience assessment is required."
            )

    # --------------------------------------------------------
    # PRODUCT MARGIN
    # --------------------------------------------------------

    if not product_df.empty:

        if len(product_df) > 1:

            row = product_df.loc[
                product_df["Margin_%"].idxmin()
            ]

            evidence_items.append(
                "PRODUCT PROFITABILITY: "
                f"{row['Product']} has the lowest margin "
                f"in the current scope at {row['Margin_%']:.2f}%."
            )

            investigation_items.append(
                "Review product-level cost structure, pricing, "
                "and product mix for the lower-margin product."
            )

        else:

            row = product_df.iloc[0]

            evidence_items.append(
                "PRODUCT PROFITABILITY: "
                f"{row['Product']} has a margin of "
                f"{row['Margin_%']:.2f}% in the current scope. "
                "No product-level comparison is possible."
            )

    # --------------------------------------------------------
    # REGIONAL RETURN SIGNAL
    # --------------------------------------------------------

    if not region_df.empty and len(region_df) > 1:

        row = region_df.loc[
            region_df["Return_Rate_%"].idxmax()
        ]

        evidence_items.append(
            "REGIONAL RETURNS: "
            f"{row['Region']} has the highest regional "
            f"return rate at {row['Return_Rate_%']:.2f}%."
        )

        investigation_items.append(
            f"Review return patterns, logistics records, "
            f"customer feedback, and operational data for "
            f"{row['Region']}."
        )

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    if not evidence_items:

        evidence_items.append(
            f"Overall return rate is {kpis['return_rate']:.2f}% "
            f"across {kpis['transactions']:,} transactions."
        )

    evidence_text = " | ".join(evidence_items)

    investigation_text = " ".join(investigation_items)

    return {
        "answer": (
            "Based on the current analysis scope, management "
            "attention should focus on the strongest validated "
            "signals identified in the available data."
        ),
        "evidence": evidence_text,
        "interpretation": (
            "These are analytical signals rather than proven "
            "causes. Management should investigate the underlying "
            "operational or customer-level evidence before taking "
            "corrective action."
        ),
        "confidence": "High",
        "unknowns": (
            "The current sales dataset does not contain sufficient "
            "information to establish root causes. Additional "
            "evidence such as quality records, return reasons, "
            "customer feedback, or operational logs may be required."
        ),
        "investigation": investigation_text,
    }


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

def executive_summary(df):

    if df.empty:
        return {
            "answer": "There is no data in the current analysis scope.",
            "evidence": "No records are available.",
            "interpretation": "No executive summary can be generated.",
            "confidence": "High",
            "unknowns": "The current scope contains no data.",
        }

    kpis = calculate_kpis(df)
    products = product_analysis(df)
    regions = region_analysis(df)

    evidence = [
        f"Revenue: ${kpis['revenue']:,.2f}",
        f"Profit: ${kpis['profit']:,.2f}",
        f"Gross margin: {kpis['gross_margin']:.2f}%",
        f"Return rate: {kpis['return_rate']:.2f}%",
        f"Transactions: {kpis['transactions']:,}",
    ]

    interpretations = []

    if len(products) > 1:

        revenue_leader = products.loc[
            products["Revenue"].idxmax()
        ]

        profit_leader = products.loc[
            products["Profit"].idxmax()
        ]

        return_leader = products.loc[
            products["Return_Rate_%"].idxmax()
        ]

        interpretations.append(
            f"{revenue_leader['Product']} leads product revenue "
            f"at ${revenue_leader['Revenue']:,.2f}."
        )

        interpretations.append(
            f"{profit_leader['Product']} leads product profit "
            f"at ${profit_leader['Profit']:,.2f}."
        )

        interpretations.append(
            f"{return_leader['Product']} has the highest "
            f"product return rate at "
            f"{return_leader['Return_Rate_%']:.2f}%."
        )

    else:

        product = products.iloc[0]

        interpretations.append(
            f"{product['Product']} generated "
            f"${product['Revenue']:,.2f} revenue and "
            f"${product['Profit']:,.2f} profit in the current scope."
        )

        interpretations.append(
            "Only one product is present in the current scope, "
            "so product-level rankings are not available."
        )

    if len(regions) > 1:

        region = regions.loc[
            regions["Return_Rate_%"].idxmax()
        ]

        interpretations.append(
            f"{region['Region']} has the highest regional "
            f"return rate at {region['Return_Rate_%']:.2f}%."
        )

    return {
        "answer": (
            "Executive summary generated from the current "
            "validated analysis scope."
        ),
        "evidence": " | ".join(evidence),
        "interpretation": " ".join(interpretations),
        "confidence": "High",
        "unknowns": (
            "The dataset does not establish causal drivers "
            "behind observed performance patterns."
        ),
    }


# ============================================================
# MAIN QUESTION ROUTER
# ============================================================

def ask_nova(question, df):

    if df is None:
        return {
            "answer": "No dataframe was provided.",
            "evidence": "Nova cannot calculate from missing data.",
            "interpretation": "Load the validated sales dataset first.",
            "confidence": "High",
            "unknowns": "The data source is unavailable.",
        }

    question = str(question).lower().strip()

    # --------------------------------------------------------
    # RETURN RATE
    # --------------------------------------------------------

    return_keywords = [
        "return rate",
        "returns",
        "returned",
        "returning",
    ]

    if any(keyword in question for keyword in return_keywords):

        if "highest" in question or "which product" in question:
            return answer_product_return_rate(df)

    # --------------------------------------------------------
    # MANAGEMENT
    # --------------------------------------------------------

    management_keywords = [
        "management",
        "investigate",
        "investigation",
        "attention",
        "what should we focus",
        "what should management",
    ]

    if any(keyword in question for keyword in management_keywords):
        return answer_management_investigation(df)

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    performance_keywords = [
        "performance",
        "best product",
        "top product",
        "product performance",
    ]

    if any(keyword in question for keyword in performance_keywords):
        return answer_product_performance(df)

    # --------------------------------------------------------
    # EXECUTIVE SUMMARY
    # --------------------------------------------------------

    summary_keywords = [
        "executive",
        "overview",
        "summary",
        "how are we doing",
        "what is happening",
    ]

    if any(keyword in question for keyword in summary_keywords):
        return executive_summary(df)

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    return {
        "answer": (
            "I can currently analyze revenue, profit, margin, "
            "returns, customer ratings, management attention, "
            "and executive performance."
        ),
        "evidence": (
            "Nova uses the validated NovaTech sales data "
            "within the current dashboard scope."
        ),
        "interpretation": (
            "Try asking a specific business question such as "
            "'Which product has the highest return rate?', "
            "'What should management investigate?', or "
            "'Give me an executive summary.'"
        ),
        "confidence": "High",
        "unknowns": (
            "Questions outside the currently implemented "
            "analysis functions may require additional logic."
        ),
    }
"""
NOVA MANAGEMENT INTELLIGENCE ENGINE
===================================

Purpose:
Convert validated insights into management-ready intelligence.

Flow:
Validated Insights
        ↓
Management Interpretation
        ↓
Business Implication
        ↓
Investigation Priority
        ↓
Management Intelligence Output

Rules:
- Raw data remains the source of truth.
- No unsupported causal claims.
- No arbitrary risk scores.
- No invented thresholds.
- Facts, interpretations, and unknowns remain separate.
- Recommendations must be supported by evidence.
"""

import pandas as pd

from insight_engine import insights


# ============================================================
# MANAGEMENT INTELLIGENCE BUILDER
# ============================================================

def build_management_intelligence(insight_list):

    management_records = []

    for insight in insight_list:

        insight_id = insight["Insight_ID"]
        title = insight["Title"]
        evidence_level = insight["Evidence_Level"]

        known_facts = insight["Known_Facts"]
        interpretation = insight["Interpretation"]
        unknowns = insight["Unknowns"]
        investigation_questions = insight["Investigation_Questions"]
        limitations = insight["Limitations"]

        # ----------------------------------------------------
        # Default management classification
        # ----------------------------------------------------

        management_area = "GENERAL BUSINESS PERFORMANCE"
        management_attention = "MONITOR"

        # ----------------------------------------------------
        # INS-001
        # ----------------------------------------------------

        if insight_id == "INS-001":

            management_area = "PRODUCT QUALITY / CUSTOMER EXPERIENCE"
            management_attention = "INVESTIGATE"

            management_message = (
                "NovaBuds X shows a combined return-rate and "
                "customer-experience signal that requires investigation "
                "before management decisions are made."
            )

            business_implication = (
                "If the observed return and rating pattern is confirmed "
                "through customer and product-level evidence, it could "
                "have implications for product performance and customer "
                "experience."
            )

            management_action = (
                "Review return reasons, customer complaints, quality "
                "records, and product-specific service data."
            )

        # ----------------------------------------------------
        # INS-002
        # ----------------------------------------------------

        elif insight_id == "INS-002":

            management_area = "REGIONAL PERFORMANCE"
            management_attention = "INVESTIGATE"

            management_message = (
                "East has the highest overall regional return rate, "
                "but the available data does not establish the reason."
            )

            business_implication = (
                "The regional return pattern may require management "
                "attention, particularly after considering product mix "
                "and regional operating factors."
            )

            management_action = (
                "Break East returns down by product, channel, fulfilment, "
                "delivery information, and customer feedback."
            )

        # ----------------------------------------------------
        # INS-003
        # ----------------------------------------------------

        elif insight_id == "INS-003":

            management_area = "PORTFOLIO CONCENTRATION"
            management_attention = "MONITOR"

            management_message = (
                "NovaWatch Pro represents a substantial share of company "
                "revenue and profit."
            )

            business_implication = (
                "A significant portion of current business performance "
                "is associated with one product, making portfolio "
                "dependency relevant for management monitoring."
            )

            management_action = (
                "Monitor NovaWatch Pro demand, pipeline dependency, "
                "margin drivers, and the contribution of alternative products."
            )

        # ----------------------------------------------------
        # INS-004
        # ----------------------------------------------------

        elif insight_id == "INS-004":

            management_area = "PRODUCT PROFITABILITY"
            management_attention = "INVESTIGATE"

            management_message = (
                "Product-level gross margins vary across the portfolio."
            )

            business_implication = (
                "Differences in product economics may affect overall "
                "profitability and should be understood before making "
                "pricing, cost, or portfolio decisions."
            )

            management_action = (
                "Review product-level cost structure, pricing, discounts, "
                "volume, and profitability drivers."
            )

        # ----------------------------------------------------
        # INS-005
        # ----------------------------------------------------

        elif insight_id == "INS-005":

            management_area = "DATA QUALITY / REPORTING"
            management_attention = "CAUTION"

            management_message = (
                "June 2026 is a partial reporting period and should not "
                "be treated as a complete month."
            )

            business_implication = (
                "Executive trend comparisons involving June may be "
                "misleading if the incomplete reporting period is not "
                "clearly identified."
            )

            management_action = (
                "Use completed periods for formal comparisons or clearly "
                "label June as a partial reporting period."
            )

        # ----------------------------------------------------
        # INS-006
        # ----------------------------------------------------

        elif insight_id == "INS-006":

            management_area = "PROFITABILITY + RETURNS"
            management_attention = "INVESTIGATE"

            management_message = (
                "Product profitability and return performance should "
                "be evaluated together rather than using margin alone."
            )

            business_implication = (
                "A product can show attractive gross margin while also "
                "having elevated returns, so product evaluation should "
                "consider multiple performance dimensions."
            )

            management_action = (
                "Evaluate product margin, return rate, rating, volume, "
                "and profit contribution together."
            )

        # ----------------------------------------------------
        # Fallback
        # ----------------------------------------------------

        else:

            management_message = (
                "This insight identifies a measurable business pattern "
                "that requires contextual management review."
            )

            business_implication = (
                "Additional evidence may be required before determining "
                "its business significance."
            )

            management_action = (
                "Review the associated evidence and investigation questions."
            )

        # ----------------------------------------------------
        # Create management intelligence record
        # ----------------------------------------------------

        management_records.append(
            {
                "Management_ID": f"MI-{insight_id.split('-')[1]}",
                "Insight_ID": insight_id,
                "Management_Area": management_area,
                "Attention": management_attention,
                "Evidence_Level": evidence_level,
                "Title": title,
                "Management_Message": management_message,
                "Business_Implication": business_implication,
                "Management_Action": management_action,
                "Known_Facts": known_facts,
                "Interpretation": interpretation,
                "Unknowns": unknowns,
                "Investigation_Questions": investigation_questions,
                "Limitations": limitations,
            }
        )

    return pd.DataFrame(management_records)


# ============================================================
# DISPLAY FUNCTION
# ============================================================

def display_management_intelligence(management_df):

    print("\n")
    print("=" * 90)
    print("                    NOVA MANAGEMENT INTELLIGENCE ENGINE")
    print("=" * 90)

    print("\nPurpose:")
    print(
        "Convert validated insights into management-ready intelligence "
        "without unsupported conclusions."
    )

    print("\nTotal management intelligence records:",
          len(management_df))

    print("\n")
    print("=" * 90)
    print("MANAGEMENT INTELLIGENCE REGISTER")
    print("=" * 90)

    for _, row in management_df.iterrows():

        print("\n")
        print("-" * 90)

        print(
            f"{row['Management_ID']} | "
            f"{row['Insight_ID']} | "
            f"{row['Management_Area']}"
        )

        print(f"ATTENTION: {row['Attention']}")
        print(f"EVIDENCE LEVEL: {row['Evidence_Level']}")

        print("\nTITLE:")
        print(f"  {row['Title']}")

        print("\nMANAGEMENT MESSAGE:")
        print(f"  {row['Management_Message']}")

        print("\nBUSINESS IMPLICATION:")
        print(f"  {row['Business_Implication']}")

        print("\nMANAGEMENT ACTION:")
        print(f"  {row['Management_Action']}")

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

        for question in row["Investigation_Questions"]:
            print(f"  • {question}")

        print("\nLIMITATIONS:")

        for limitation in row["Limitations"]:
            print(f"  • {limitation}")


# ============================================================
# MANAGEMENT SUMMARY
# ============================================================

def generate_management_summary(management_df):

    print("\n")
    print("=" * 90)
    print("                    MANAGEMENT INTELLIGENCE SUMMARY")
    print("=" * 90)

    print(
        f"\nTotal management intelligence records: "
        f"{len(management_df)}"
    )

    print("\n========== BY MANAGEMENT AREA ==========")

    area_counts = management_df["Management_Area"].value_counts()

    for area, count in area_counts.items():
        print(f"{area}: {count}")

    print("\n========== BY ATTENTION LEVEL ==========")

    attention_counts = management_df["Attention"].value_counts()

    for attention, count in attention_counts.items():
        print(f"{attention}: {count}")

    print("\n========== BY EVIDENCE LEVEL ==========")

    evidence_counts = management_df["Evidence_Level"].value_counts()

    for evidence, count in evidence_counts.items():
        print(f"{evidence}: {count}")

    print("\n========== MANAGEMENT ATTENTION ITEMS ==========")

    attention_order = ["INVESTIGATE", "MONITOR", "CAUTION"]

    for attention in attention_order:

        rows = management_df[
            management_df["Attention"] == attention
        ]

        for _, row in rows.iterrows():

            print(
                f"  • {row['Management_ID']} | "
                f"{row['Management_Area']} | "
                f"{row['Title']}"
            )


# ============================================================
# MAIN EXECUTION
# ============================================================

management_df = build_management_intelligence(insights)

display_management_intelligence(management_df)

generate_management_summary(management_df)


print("\n")
print("=" * 90)
print("🟢 NOVA MANAGEMENT INTELLIGENCE ENGINE: READY")
print("=" * 90)

print(
    "Validated insights have been converted into management-ready "
    "messages, implications, actions, and investigation paths."
)

print(
    "No unsupported causal claims, arbitrary thresholds, "
    "or risk scores were introduced."
)

print("=" * 90)
import pandas as pd

from question_engine import (
    calculate_kpis,
    product_analysis,
    region_analysis,
)


# ============================================================
# NOVA CEO BRIEF ENGINE
# Executive Intelligence V1
# ============================================================


def generate_ceo_brief(df):

    if df is None or df.empty:
        return {
            "status": "NO_DATA",
            "title": "Nova CEO Brief",
            "snapshot": "No data is available in the current analysis scope.",
            "kpis": {},
            "signals": [],
            "what_we_know": [],
            "what_we_do_not_know": [],
            "investigate_next": [],
        }

    kpis = calculate_kpis(df)
    products = product_analysis(df)
    regions = region_analysis(df)

    # --------------------------------------------------------
    # KPI SNAPSHOT
    # --------------------------------------------------------

    kpi_snapshot = {
        "Revenue": kpis["revenue"],
        "Profit": kpis["profit"],
        "Gross Margin": kpis["gross_margin"],
        "Return Rate": kpis["return_rate"],
        "Transactions": kpis["transactions"],
    }

    # --------------------------------------------------------
    # VALIDATED SIGNALS
    # --------------------------------------------------------

    signals = []

    # Product return signal
    if not products.empty and len(products) > 1:

        highest_return = products.loc[
            products["Return_Rate_%"].idxmax()
        ]

        signals.append(
            {
                "area": "Product Returns",
                "message": (
                    f"{highest_return['Product']} has the highest "
                    f"product return rate at "
                    f"{highest_return['Return_Rate_%']:.2f}%."
                ),
                "evidence": (
                    f"{int(highest_return['Returns']):,} returns "
                    f"against {int(highest_return['Units']):,} units."
                ),
            }
        )

    # Customer rating signal
    if not products.empty and len(products) > 1:

        lowest_rating = products.loc[
            products["Rating"].idxmin()
        ]

        signals.append(
            {
                "area": "Customer Experience",
                "message": (
                    f"{lowest_rating['Product']} has the lowest "
                    f"average customer rating at "
                    f"{lowest_rating['Rating']:.2f}."
                ),
                "evidence": (
                    "Customer_Rating is the source field used "
                    "for this calculation."
                ),
            }
        )

    # Revenue concentration
    if not products.empty and len(products) > 1:

        total_revenue = products["Revenue"].sum()

        concentration_product = products.loc[
            products["Revenue"].idxmax()
        ]

        revenue_share = (
            concentration_product["Revenue"]
            / total_revenue
            * 100
        )

        signals.append(
            {
                "area": "Portfolio Concentration",
                "message": (
                    f"{concentration_product['Product']} contributes "
                    f"{revenue_share:.2f}% of revenue within the "
                    f"current scope."
                ),
                "evidence": (
                    f"Revenue: "
                    f"${concentration_product['Revenue']:,.2f}."
                ),
            }
        )

    # Regional return signal
    if not regions.empty and len(regions) > 1:

        highest_region_return = regions.loc[
            regions["Return_Rate_%"].idxmax()
        ]

        signals.append(
            {
                "area": "Regional Performance",
                "message": (
                    f"{highest_region_return['Region']} has the "
                    f"highest regional return rate at "
                    f"{highest_region_return['Return_Rate_%']:.2f}%."
                ),
                "evidence": (
                    f"{int(highest_region_return['Returns']):,} returns "
                    f"against {int(highest_region_return['Units']):,} units."
                ),
            }
        )

    # --------------------------------------------------------
    # WHAT WE KNOW
    # --------------------------------------------------------

    what_we_know = [
        (
            f"The current scope contains "
            f"{kpis['transactions']:,} transactions."
        ),
        (
            f"Revenue is ${kpis['revenue']:,.2f} and "
            f"profit is ${kpis['profit']:,.2f}."
        ),
        (
            f"Gross margin is "
            f"{kpis['gross_margin']:.2f}%."
        ),
        (
            f"Return rate is "
            f"{kpis['return_rate']:.2f}%."
        ),
    ]

    # --------------------------------------------------------
    # WHAT WE DO NOT KNOW
    # --------------------------------------------------------

    what_we_do_not_know = [
        "The dataset does not establish root causes of returns.",
        "The dataset does not contain detailed customer-level feedback.",
        "The dataset does not establish whether operational or logistics factors caused observed regional differences.",
        "The dataset does not prove that an observed correlation is causal.",
    ]

    # --------------------------------------------------------
    # INVESTIGATION PATH
    # --------------------------------------------------------

    investigate_next = [
        "Review product-level return reasons.",
        "Review customer complaints and feedback.",
        "Review quality-control records for products with elevated returns.",
        "Review regional logistics and operational records where return rates are elevated.",
    ]

    # --------------------------------------------------------
    # EXECUTIVE SNAPSHOT
    # --------------------------------------------------------

    snapshot = (
        f"The current analysis scope contains "
        f"{kpis['transactions']:,} transactions generating "
        f"${kpis['revenue']:,.2f} revenue and "
        f"${kpis['profit']:,.2f} profit, with a "
        f"{kpis['gross_margin']:.2f}% gross margin and "
        f"{kpis['return_rate']:.2f}% return rate."
    )

    return {
        "status": "READY",
        "title": "Nova CEO Brief",
        "snapshot": snapshot,
        "kpis": kpi_snapshot,
        "signals": signals,
        "what_we_know": what_we_know,
        "what_we_do_not_know": what_we_do_not_know,
        "investigate_next": investigate_next,
    }


# ============================================================
# TEST MODE
# ============================================================

if __name__ == "__main__":

    df = pd.read_excel("NovaTech_Sales_Data.xlsx")

    brief = generate_ceo_brief(df)

    print()
    print("=" * 60)
    print("NOVA CEO BRIEF")
    print("=" * 60)

    print()
    print("EXECUTIVE SNAPSHOT")
    print(brief["snapshot"])

    print()
    print("KPI SNAPSHOT")

    for key, value in brief["kpis"].items():

        if isinstance(value, float):
            if "Margin" in key or "Rate" in key:
                print(f"{key}: {value:.2f}%")
            else:
                print(f"{key}: {value:,.2f}")
        else:
            print(f"{key}: {value:,}")

    print()
    print("VALIDATED SIGNALS")

    for signal in brief["signals"]:

        print(f"- {signal['area']}: {signal['message']}")
        print(f"  Evidence: {signal['evidence']}")

    print()
    print("WHAT WE KNOW")

    for item in brief["what_we_know"]:
        print(f"- {item}")

    print()
    print("WHAT WE DO NOT KNOW")

    for item in brief["what_we_do_not_know"]:
        print(f"- {item}")

    print()
    print("INVESTIGATE NEXT")

    for item in brief["investigate_next"]:
        print(f"- {item}")

    print()
    print("=" * 60)
    print("NOVA CEO BRIEF ENGINE: READY")
    print("=" * 60)
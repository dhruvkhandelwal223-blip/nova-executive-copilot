"""
NOVA DATA VALIDATION ENGINE

Purpose:
Validate the raw NovaTech Sales dataset against
Nova's trusted data contract.

Validation outcomes:
    VERIFIED
    ROUNDING DIFFERENCE
    MISMATCH
"""

import pandas as pd

from trust_config import (
    DATASET_CONFIG,
    TRUSTED_KPIS,
)


# ============================================================
# TOLERANCES
# ============================================================

# Floating-point safety tolerance
FLOAT_TOLERANCE = 0.000001

# Financial rounding tolerance
MONEY_TOLERANCE = 0.011

# Percentage rounding tolerance
PERCENT_TOLERANCE = 0.011


# ============================================================
# LOAD DATA
# ============================================================

FILE = DATASET_CONFIG["file_name"]

df = pd.read_excel(FILE)


# ============================================================
# VALIDATION RESULTS
# ============================================================

results = []


def add_result(name, status, details):
    results.append({
        "check": name,
        "status": status,
        "details": details,
    })


# ============================================================
# 1. DATASET SIZE
# ============================================================

add_result(
    "Row count",
    "VERIFIED"
    if len(df) == DATASET_CONFIG["expected_rows"]
    else "MISMATCH",
    f"Expected {DATASET_CONFIG['expected_rows']}, found {len(df)}",
)


add_result(
    "Column count",
    "VERIFIED"
    if len(df.columns) == DATASET_CONFIG["expected_columns"]
    else "MISMATCH",
    f"Expected {DATASET_CONFIG['expected_columns']}, found {len(df.columns)}",
)


# ============================================================
# 2. REQUIRED COLUMNS
# ============================================================

missing_columns = [
    column
    for column in DATASET_CONFIG["required_columns"]
    if column not in df.columns
]

add_result(
    "Required columns",
    "VERIFIED" if not missing_columns else "MISMATCH",
    "All required columns present"
    if not missing_columns
    else f"Missing columns: {missing_columns}",
)


# ============================================================
# 3. MISSING VALUES
# ============================================================

missing_values = int(df.isnull().sum().sum())

add_result(
    "Missing values",
    "VERIFIED" if missing_values == 0 else "MISMATCH",
    f"Total missing values: {missing_values}",
)


# ============================================================
# 4. DUPLICATE ORDER IDS
# ============================================================

duplicate_ids = int(df["Order_ID"].duplicated().sum())

add_result(
    "Duplicate Order IDs",
    "VERIFIED" if duplicate_ids == 0 else "MISMATCH",
    f"Duplicate Order IDs found: {duplicate_ids}",
)


# ============================================================
# 5. DUPLICATE FULL ROWS
# ============================================================

duplicate_rows = int(df.duplicated().sum())

add_result(
    "Duplicate full rows",
    "VERIFIED" if duplicate_rows == 0 else "MISMATCH",
    f"Duplicate full rows found: {duplicate_rows}",
)


# ============================================================
# 6. NEGATIVE REVENUE
# ============================================================

negative_revenue = int(
    (df["Revenue"] < 0).sum()
)

add_result(
    "Negative revenue",
    "VERIFIED" if negative_revenue == 0 else "MISMATCH",
    f"Rows with negative revenue: {negative_revenue}",
)


# ============================================================
# 7. NEGATIVE UNITS
# ============================================================

negative_units = int(
    (df["Units_Sold"] < 0).sum()
)

add_result(
    "Negative units",
    "VERIFIED" if negative_units == 0 else "MISMATCH",
    f"Rows with negative units: {negative_units}",
)


# ============================================================
# 8. RETURNS CANNOT EXCEED UNITS
# ============================================================

invalid_returns = int(
    (df["Returns"] > df["Units_Sold"]).sum()
)

add_result(
    "Returns <= Units Sold",
    "VERIFIED"
    if invalid_returns == 0
    else "MISMATCH",
    f"Rows where returns exceed units: {invalid_returns}",
)


# ============================================================
# 9. PROFIT FORMULA
# ============================================================

profit_difference = (
    df["Profit"] - (df["Revenue"] - df["Cost"])
).abs()

max_profit_difference = float(
    profit_difference.max()
)

rows_with_profit_difference = int(
    (profit_difference > FLOAT_TOLERANCE).sum()
)


if max_profit_difference <= FLOAT_TOLERANCE:

    profit_status = "VERIFIED"

    profit_details = (
        "Profit exactly matches Revenue - Cost"
    )

elif max_profit_difference <= MONEY_TOLERANCE:

    profit_status = "ROUNDING DIFFERENCE"

    profit_details = (
        f"Maximum difference: "
        f"${max_profit_difference:.2f}; "
        f"{rows_with_profit_difference} row(s) affected. "
        f"Within accepted $0.01 rounding tolerance."
    )

else:

    profit_status = "MISMATCH"

    profit_details = (
        f"Maximum difference: "
        f"${max_profit_difference:.2f}; "
        f"{rows_with_profit_difference} row(s) affected."
    )


add_result(
    "Profit formula",
    profit_status,
    profit_details,
)


# ============================================================
# 10. CORE KPI CALCULATIONS
# ============================================================

revenue = float(df["Revenue"].sum())
cost = float(df["Cost"].sum())
profit = float(df["Profit"].sum())

units = int(df["Units_Sold"].sum())
returns = int(df["Returns"].sum())

gross_margin = profit / revenue * 100
return_rate = returns / units * 100


# ============================================================
# KPI VALIDATION FUNCTION
# ============================================================

def validate_kpi(
    name,
    calculated,
    trusted,
    tolerance,
    display_format,
):
    difference = abs(calculated - trusted)

    if difference <= FLOAT_TOLERANCE:

        status = "VERIFIED"

    elif difference <= tolerance:

        status = "ROUNDING DIFFERENCE"

    else:

        status = "MISMATCH"

    details = (
        f"Calculated {display_format.format(calculated)} | "
        f"Trusted {display_format.format(trusted)} | "
        f"Difference {display_format.format(difference)}"
    )

    add_result(
        name,
        status,
        details,
    )


# ============================================================
# 11. REVENUE KPI
# ============================================================

validate_kpi(
    "Revenue KPI",
    revenue,
    TRUSTED_KPIS["revenue"],
    MONEY_TOLERANCE,
    "${:,.2f}",
)


# ============================================================
# 12. COST KPI
# ============================================================

validate_kpi(
    "Cost KPI",
    cost,
    TRUSTED_KPIS["cost"],
    MONEY_TOLERANCE,
    "${:,.2f}",
)


# ============================================================
# 13. PROFIT KPI
# ============================================================

validate_kpi(
    "Profit KPI",
    profit,
    TRUSTED_KPIS["profit"],
    MONEY_TOLERANCE,
    "${:,.2f}",
)


# ============================================================
# 14. UNITS KPI
# ============================================================

validate_kpi(
    "Units KPI",
    units,
    TRUSTED_KPIS["units"],
    0,
    "{:,.0f}",
)


# ============================================================
# 15. RETURNS KPI
# ============================================================

validate_kpi(
    "Returns KPI",
    returns,
    TRUSTED_KPIS["returns"],
    0,
    "{:,.0f}",
)


# ============================================================
# 16. GROSS MARGIN KPI
# ============================================================

validate_kpi(
    "Gross Margin KPI",
    gross_margin,
    TRUSTED_KPIS["gross_margin_pct"],
    PERCENT_TOLERANCE,
    "{:.2f}%",
)


# ============================================================
# 17. RETURN RATE KPI
# ============================================================

validate_kpi(
    "Return Rate KPI",
    return_rate,
    TRUSTED_KPIS["return_rate_pct"],
    PERCENT_TOLERANCE,
    "{:.2f}%",
)


# ============================================================
# PRINT VALIDATION REPORT
# ============================================================

print("\n")

print("=" * 70)
print("                  NOVA DATA VALIDATION")
print("=" * 70)


for result in results:

    status = result["status"]

    if status == "VERIFIED":
        symbol = "🟢"

    elif status == "ROUNDING DIFFERENCE":
        symbol = "🟡"

    else:
        symbol = "🔴"

    print(
        f"{symbol} {result['check']}: "
        f"{status} — {result['details']}"
    )


# ============================================================
# FINAL TRUST DECISION
# ============================================================

mismatches = [
    result
    for result in results
    if result["status"] == "MISMATCH"
]

rounding_differences = [
    result
    for result in results
    if result["status"] == "ROUNDING DIFFERENCE"
]


print("\n" + "=" * 70)


if mismatches:

    print("🔴 NOVA TRUST STATUS: FAILED")

    print(
        f"{len(mismatches)} critical validation "
        f"check(s) failed."
    )


elif rounding_differences:

    print(
        "🟡 NOVA TRUST STATUS: "
        "VERIFIED WITH ROUNDING"
    )

    print(
        f"{len(rounding_differences)} "
        f"rounding difference(s) detected."
    )

    print(
        "No critical validation mismatch detected."
    )


else:

    print("🟢 NOVA TRUST STATUS: VERIFIED")

    print(
        "All validation checks passed exactly."
    )


print("=" * 70)
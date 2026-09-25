"""
NOVA TRUST CONFIGURATION

Purpose:
Define the validated baseline and known audit corrections
for the NovaTech Sales dataset.

IMPORTANT:
This file does NOT modify the raw Excel data.
It only defines what Nova expects and what has already
been independently validated.
"""


# ============================================================
# DATASET CONTRACT
# ============================================================

DATASET_CONFIG = {
    "file_name": "NovaTech_Sales_Data.xlsx",
    "expected_rows": 420,
    "expected_columns": 14,

    "required_columns": [
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
    ],
}


# ============================================================
# TRUSTED CORE KPIs
# ============================================================

TRUSTED_KPIS = {
    "revenue": 2560392.43,
    "cost": 1434382.37,
    "profit": 1126010.04,
    "units": 18216,
    "returns": 660,
    "gross_margin_pct": 43.98,
    "return_rate_pct": 3.62,
}


# ============================================================
# VALIDATED DATA QUALITY CONDITIONS
# ============================================================

DATA_QUALITY_RULES = {
    "duplicate_order_ids_allowed": False,
    "duplicate_full_rows_allowed": False,
    "missing_values_allowed": False,
    "negative_revenue_allowed": False,
    "negative_units_allowed": False,
    "returns_greater_than_units_allowed": False,
}


# ============================================================
# FORMULA VALIDATION RULES
# ============================================================

FORMULA_RULES = {
    "profit_formula": "Profit = Revenue - Cost",

    "gross_margin_formula": (
        "Gross Margin % = Profit / Revenue * 100"
    ),

    "return_rate_formula": (
        "Return Rate % = Returns / Units_Sold * 100"
    ),
}


# ============================================================
# KNOWN AUDIT CORRECTIONS
# ============================================================

KNOWN_CORRECTIONS = {

    "novabuds_x_region": {
        "status": "CORRECTED",
        "finding": (
            "West is the highest NovaBuds X return-rate region "
            "at 8.24%. East is 7.80% for NovaBuds X."
        ),
        "additional_context": (
            "East is the highest overall regional return-rate "
            "region at 4.89%."
        ),
    },

    "fitness_margin_interpretation": {
        "status": "CORRECTED",
        "finding": (
            "Fitness Enthusiast's higher blended margin is "
            "mix-driven and does not prove a pricing advantage."
        ),
    },

    "east_logistics": {
        "status": "INVESTIGATION_REQUIRED",
        "finding": (
            "East has the highest overall regional return rate "
            "at 4.89%, but logistics is only a hypothesis."
        ),
    },

    "novabuds_x_quality": {
        "status": "NOT_PROVEN",
        "finding": (
            "The available dataset does not prove the cause "
            "of NovaBuds X returns or lower ratings."
        ),
    },

    "june_2026": {
        "status": "PARTIAL_PERIOD",
        "finding": (
            "June 2026 contains only part of the month and "
            "must be clearly flagged in time-based analysis."
        ),
    },
}


# ============================================================
# EVIDENCE LEVELS
# ============================================================

EVIDENCE_LEVELS = {
    1: "RAW_DATA_VERIFIED",
    2: "CALCULATED_FROM_RAW_DATA",
    3: "VALIDATED_PATTERN",
    4: "INTERPRETATION",
    5: "HYPOTHESIS",
    6: "EXTERNAL_INVESTIGATION_REQUIRED",
}


# ============================================================
# TRUST STATUS
# ============================================================

TRUST_STATUS = {
    "VERIFIED": "Verified against trusted baseline",
    "VERIFIED_WITH_ROUNDING": "Verified with acceptable rounding difference",
    "CORRECTED": "Original analytical statement required correction",
    "UNSUPPORTED": "Not supported by available data",
    "NOT_TESTABLE": "Cannot be tested with available data",
    "INVESTIGATION_REQUIRED": "Requires additional evidence",
}


# ============================================================
# DATA LIMITATIONS
# ============================================================

DATA_LIMITATIONS = [
    "Dataset does not contain causal variables.",
    "Costs are available at transaction level but causal cost drivers are not provided.",
    "No customer-level identifier is available.",
    "June 2026 is a partial period.",
    "The dataset alone cannot prove the cause of returns.",
    "The dataset alone cannot prove pricing advantages.",
]


# ============================================================
# TRUST CONFIGURATION COMPLETE
# ============================================================

TRUST_CONFIG_READY = True
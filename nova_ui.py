"""
============================================================
NOVA — EXECUTIVE COPILOT
UI DESIGN SYSTEM — V2.4
============================================================

Stitch-inspired executive presentation layer for NOVA.

ARCHITECTURE BOUNDARY
---------------------
This module is PRESENTATION ONLY.

It does NOT:
    - calculate business metrics
    - manipulate source data
    - perform AI reasoning
    - validate business claims
    - detect management signals
    - modify the Trust Layer

Core principle:
    EVIDENCE BEFORE INTERPRETATION

Compatibility goal:
    Preserve the public component interfaces used by app.py while
    making the presentation layer tolerant of strings, lists, tuples,
    dictionaries and optional keyword arguments.
============================================================
"""

import html

import streamlit as st


# ============================================================
# DESIGN TOKENS
# ============================================================

COLORS = {
    "bg": "#080C14",
    "surface": "#0D121B",
    "surface_2": "#111824",
    "surface_3": "#172130",
    "border": "#263244",
    "border_soft": "#1A2534",
    "text": "#F8FAFC",
    "text_muted": "#A7B3C5",
    "text_dim": "#708096",
    "emerald": "#10B981",
    "cyan": "#22D3EE",
    "indigo": "#818CF8",
    "purple": "#C084FC",
    "amber": "#FBBF24",
    "rose": "#FB7185",
    "red": "#F87171",
}

EPISTEMIC_COLORS = {
    "FACT": COLORS["cyan"],
    "CALCULATION": COLORS["emerald"],
    "VALIDATED PATTERN": COLORS["indigo"],
    "INTERPRETATION": COLORS["purple"],
    "INVESTIGATION REQUIRED": COLORS["amber"],
    "SOURCE DATA": COLORS["cyan"],
    "VALIDATION": COLORS["emerald"],
    "GOVERNANCE": COLORS["cyan"],
    "NEXT INVESTIGATION": COLORS["amber"],
    "NOT AVAILABLE": COLORS["amber"],
    "UNKNOWN": COLORS["amber"],
    "MODEL OUTPUT": COLORS["purple"],
    "DATA INTEGRITY VERIFIED": COLORS["emerald"],
}


# ============================================================
# SAFE / NORMALIZATION HELPERS
# ============================================================

def _safe(value):
    """Safely escape dynamic text before placing it inside HTML."""
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def _normalize_items(value):
    """
    Normalize evidence values into a list without iterating over strings
    character-by-character.

    This fixes the historical:
        ✓ S
        ✓ O
        ✓ U
        ...
    rendering bug when NOVA returned a plain string.
    """
    if value is None:
        return []

    if isinstance(value, str):
        cleaned = value.strip()
        return [cleaned] if cleaned else []

    if isinstance(value, dict):
        return [value]

    if isinstance(value, (list, tuple, set)):
        return list(value)

    return [value]


def _display_text(value):
    """Convert common NOVA result structures into readable text."""
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            if item in (None, ""):
                continue
            parts.append(f"{key}: {item}")
        return "\n".join(parts)

    if isinstance(value, (list, tuple, set)):
        return "\n".join(f"• {item}" for item in value)

    return str(value)


def _status_color(status, fallback=None):
    normalized = str(status or "").strip().upper()
    return EPISTEMIC_COLORS.get(
        normalized,
        fallback or COLORS["text_dim"],
    )


def _render(content):
    """Render controlled NOVA HTML using Streamlit's native HTML renderer."""
    if content is None:
        return

    content = str(content).strip()
    if not content:
        return

    st.html(content)


# Backward-compatible name used by earlier NOVA UI versions.
_render_html = _render


# ============================================================
# GLOBAL THEME
# ============================================================

def apply_nova_theme():
    """
    Apply the NOVA visual system.

    The native Streamlit theme should be defined in:
        .streamlit/config.toml

    This function adds only presentation-level CSS for the executive UI.
    """

    css = f"""
    <style>
        /* -------------------------------------------------- */
        /* GLOBAL CANVAS                                      */
        /* -------------------------------------------------- */

        .stApp {{
            background:
                radial-gradient(
                    circle at 88% 0%,
                    rgba(34, 211, 238, 0.045),
                    transparent 27%
                ),
                radial-gradient(
                    circle at 10% 20%,
                    rgba(16, 185, 129, 0.035),
                    transparent 24%
                ),
                {COLORS["bg"]};
            color: {COLORS["text"]};
        }}

        .main {{
            background: {COLORS["bg"]};
        }}

        .block-container {{
            max-width: 1500px;
            padding-top: 1.25rem;
            padding-bottom: 4rem;
        }}

        html, body,
        [class*="css"] {{
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: {COLORS["text"]} !important;
            letter-spacing: -0.02em;
        }}

        p, label {{
            color: {COLORS["text_muted"]};
        }}

        /* -------------------------------------------------- */
        /* SIDEBAR                                             */
        /* -------------------------------------------------- */

        section[data-testid="stSidebar"] {{
            background: {COLORS["surface"]};
            border-right: 1px solid {COLORS["border_soft"]};
        }}

        section[data-testid="stSidebar"] > div {{
            background: {COLORS["surface"]};
        }}

        /* -------------------------------------------------- */
        /* NATIVE STREAMLIT INPUTS                             */
        /* -------------------------------------------------- */

        div[data-testid="stTextInput"] {{
            width: 100% !important;
            margin-bottom: 8px !important;
        }}

        div[data-testid="stTextInput"] label {{
            color: {COLORS["text_muted"]} !important;
            font-size: 11px !important;
            font-weight: 650 !important;
            letter-spacing: 0.04em !important;
        }}

        div[data-testid="stTextInput"] > div {{
            width: 100% !important;
        }}

        div[data-testid="stTextInput"] div[data-baseweb="base-input"],
        div[data-testid="stTextInput"] div[data-baseweb="input"] {{
            width: 100% !important;
            min-height: 48px !important;
            background: {COLORS["surface"]} !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 12px !important;
            box-shadow: 0 8px 26px rgba(0,0,0,0.18) !important;
        }}

        div[data-testid="stTextInput"] div[data-baseweb="input"] > div {{
            background: transparent !important;
            border: none !important;
            border-radius: 12px !important;
        }}

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextInput"] input[type="text"] {{
            width: 100% !important;
            min-height: 46px !important;
            background: transparent !important;
            color: {COLORS["text"]} !important;
            -webkit-text-fill-color: {COLORS["text"]} !important;
            caret-color: {COLORS["cyan"]} !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }}

        div[data-testid="stTextInput"] input::placeholder {{
            color: {COLORS["text_dim"]} !important;
            -webkit-text-fill-color: {COLORS["text_dim"]} !important;
            opacity: 1 !important;
        }}

        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
        div[data-testid="stTextInput"] div[data-baseweb="base-input"]:focus-within {{
            background: {COLORS["surface"]} !important;
            border: 1px solid {COLORS["cyan"]} !important;
            box-shadow:
                0 0 0 1px rgba(34,211,238,0.13),
                0 8px 28px rgba(0,0,0,0.20) !important;
        }}

        /* Broad fallback for Streamlit/BaseWeb input variants. */
        div[data-baseweb="input"] input,
        input[type="text"] {{
            background: transparent !important;
            color: {COLORS["text"]} !important;
            -webkit-text-fill-color: {COLORS["text"]} !important;
            caret-color: {COLORS["cyan"]} !important;
        }}

        input[type="text"]::placeholder {{
            color: {COLORS["text_dim"]} !important;
            -webkit-text-fill-color: {COLORS["text_dim"]} !important;
            opacity: 1 !important;
        }}

        /* Select widgets */
        div[data-baseweb="select"] > div {{
            background: {COLORS["surface"]} !important;
            border-color: {COLORS["border"]} !important;
            color: {COLORS["text"]} !important;
            border-radius: 8px !important;
        }}

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] input {{
            color: {COLORS["text"]} !important;
        }}

        /* -------------------------------------------------- */
        /* BUTTONS                                             */
        /* -------------------------------------------------- */

        .stButton > button {{
            background: {COLORS["surface_2"]} !important;
            color: {COLORS["text"]} !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 9px !important;
            font-weight: 650 !important;
            min-height: 42px !important;
            padding: 0 16px !important;
            transition: all 0.16s ease !important;
        }}

        .stButton > button:hover {{
            border-color: {COLORS["cyan"]} !important;
            color: {COLORS["cyan"]} !important;
            background: {COLORS["surface_3"]} !important;
        }}

        .stButton > button:focus,
        .stButton > button:focus-visible {{
            outline: none !important;
            box-shadow: 0 0 0 1px rgba(34,211,238,0.25) !important;
        }}

        .stButton > button[kind="primary"] {{
            background: rgba(34,211,238,0.08) !important;
            border-color: rgba(34,211,238,0.34) !important;
            color: {COLORS["cyan"]} !important;
        }}

        .stButton > button[kind="primary"]:hover {{
            background: rgba(34,211,238,0.13) !important;
            border-color: rgba(34,211,238,0.60) !important;
        }}

        /* -------------------------------------------------- */
        /* TABS / DATAFRAME / DIVIDERS                         */
        /* -------------------------------------------------- */

        button[data-baseweb="tab"] {{
            color: {COLORS["text_muted"]} !important;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {COLORS["cyan"]} !important;
        }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid {COLORS["border"]};
            border-radius: 9px;
            overflow: hidden;
        }}

        hr {{
            border-color: {COLORS["border_soft"]} !important;
        }}

        /* -------------------------------------------------- */
        /* STREAMLIT CHROME                                    */
        /* -------------------------------------------------- */

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        [data-testid="stToolbar"] {{
            background: transparent !important;
        }}

        /* -------------------------------------------------- */
        /* SCROLLBAR                                           */
        /* -------------------------------------------------- */

        ::-webkit-scrollbar {{
            width: 7px;
            height: 7px;
        }}

        ::-webkit-scrollbar-track {{
            background: {COLORS["bg"]};
        }}

        ::-webkit-scrollbar-thumb {{
            background: {COLORS["border"]};
            border-radius: 10px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS["text_dim"]};
        }}

        /* -------------------------------------------------- */
        /* RESPONSIVE HTML COMPONENTS                          */
        /* -------------------------------------------------- */

        @media (max-width: 850px) {{
            .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}
        }}
    </style>
    """

    _render(css)


# ============================================================
# BRAND
# ============================================================

def render_brand():
    _render(
        f"""
        <div style="
            padding:4px 0 18px 0;
            border-bottom:1px solid {COLORS["border_soft"]};
            margin-bottom:18px;
        ">
            <div style="
                font-size:23px;
                font-weight:800;
                letter-spacing:0.10em;
                color:{COLORS["text"]};
            ">NOVA</div>

            <div style="
                font-size:9px;
                font-weight:750;
                letter-spacing:0.16em;
                color:{COLORS["cyan"]};
                margin-top:4px;
            ">EXECUTIVE COPILOT</div>

            <div style="
                font-size:10px;
                color:{COLORS["text_dim"]};
                margin-top:8px;
                letter-spacing:0.03em;
            ">Evidence Before Interpretation</div>
        </div>
        """
    )


# ============================================================
# COMMAND BAR
# ============================================================

def command_bar(
    active_view="Command Center",
    record_count=0,
    title=None,
    subtitle=None,
    **kwargs,
):
    """Render the executive workspace header."""
    if title is None:
        title = active_view

    if subtitle is None:
        try:
            subtitle = (
                "Executive intelligence workspace • "
                f"{int(record_count):,} records in scope"
            )
        except (TypeError, ValueError):
            subtitle = "Executive intelligence workspace"

    _render(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:flex-end;
            gap:20px;
            padding:6px 0 20px 0;
            border-bottom:1px solid {COLORS["border_soft"]};
            margin-bottom:20px;
        ">
            <div>
                <div style="
                    font-size:10px;
                    font-weight:750;
                    color:{COLORS["cyan"]};
                    letter-spacing:0.14em;
                    text-transform:uppercase;
                    margin-bottom:7px;
                ">NOVA / EXECUTIVE INTELLIGENCE</div>

                <div style="
                    font-size:28px;
                    line-height:1.1;
                    font-weight:780;
                    color:{COLORS["text"]};
                    letter-spacing:-0.035em;
                ">{_safe(title)}</div>

                <div style="
                    margin-top:7px;
                    font-size:12px;
                    color:{COLORS["text_dim"]};
                ">{_safe(subtitle)}</div>
            </div>

            <div style="
                padding:7px 11px;
                border:1px solid rgba(16,185,129,0.25);
                border-radius:7px;
                background:rgba(16,185,129,0.055);
                color:{COLORS["emerald"]};
                font-size:8px;
                font-weight:750;
                letter-spacing:0.09em;
                white-space:nowrap;
            ">DATA INTEGRITY VERIFIED</div>
        </div>
        """
    )


# ============================================================
# SECTION HEADER
# ============================================================

def section_header(title, subtitle=None, status=None, **kwargs):
    status_html = ""

    if status:
        status_color = _status_color(status, COLORS["emerald"])
        status_html = f"""
        <span style="
            margin-left:10px;
            padding:3px 8px;
            border-radius:999px;
            background:{status_color}12;
            border:1px solid {status_color}55;
            color:{status_color};
            font-size:8px;
            font-weight:750;
            letter-spacing:0.07em;
        ">{_safe(status)}</span>
        """

    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <div style="
            color:{COLORS["text_dim"]};
            font-size:11px;
            margin-top:5px;
            line-height:1.5;
        ">{_safe(subtitle)}</div>
        """

    _render(
        f"""
        <div style="margin:10px 0 18px 0;">
            <div style="
                display:flex;
                align-items:center;
                gap:4px;
                flex-wrap:wrap;
                font-size:19px;
                font-weight:750;
                color:{COLORS["text"]};
                letter-spacing:-0.02em;
            ">
                {_safe(title)}
                {status_html}
            </div>
            {subtitle_html}
        </div>
        """
    )


# ============================================================
# EPISTEMIC BADGE
# ============================================================

def epistemic_badge(level, label=None, **kwargs):
    normalized = str(level or "UNKNOWN").strip().upper()
    color = _status_color(normalized)

    label_html = ""
    if label:
        label_html = f"""
        <span style="
            margin-left:8px;
            color:{COLORS["text_dim"]};
            font-size:9px;
            font-weight:500;
            letter-spacing:0;
        ">{_safe(label)}</span>
        """

    _render(
        f"""
        <div style="margin:2px 0 8px 0;">
            <span style="
                display:inline-flex;
                align-items:center;
                padding:5px 9px;
                border-radius:999px;
                border:1px solid {color}55;
                background:{color}12;
                color:{color};
                font-size:8px;
                font-weight:750;
                letter-spacing:0.075em;
                white-space:nowrap;
            ">
                <span style="
                    display:inline-block;
                    width:5px;
                    height:5px;
                    border-radius:50%;
                    background:{color};
                    margin-right:6px;
                "></span>
                {_safe(normalized)}
                {label_html}
            </span>
        </div>
        """
    )


# ============================================================
# KPI CARD
# ============================================================

def kpi_card(
    label,
    value,
    caption=None,
    status="FACT",
    delta=None,
    **kwargs,
):
    status_color = _status_color(status, COLORS["emerald"])

    caption_html = ""
    if caption:
        caption_html = f"""
        <div style="
            margin-top:7px;
            color:{COLORS["text_dim"]};
            font-size:10px;
            line-height:1.4;
        ">{_safe(caption)}</div>
        """

    delta_html = ""
    if delta not in (None, ""):
        delta_html = f"""
        <div style="
            margin-top:7px;
            color:{COLORS["text_muted"]};
            font-size:10px;
        ">{_safe(delta)}</div>
        """

    _render(
        f"""
        <div style="
            background:linear-gradient(
                145deg,
                {COLORS["surface_2"]},
                {COLORS["surface"]}
            );
            border:1px solid {COLORS["border"]};
            border-radius:10px;
            padding:17px 18px;
            min-height:122px;
            box-sizing:border-box;
        ">
            <div style="
                color:{COLORS["text_dim"]};
                font-size:9px;
                font-weight:750;
                letter-spacing:0.10em;
                text-transform:uppercase;
            ">{_safe(label)}</div>

            <div style="
                margin-top:10px;
                color:{COLORS["text"]};
                font-family:
                    'JetBrains Mono',
                    'SFMono-Regular',
                    Consolas,
                    monospace;
                font-size:24px;
                font-weight:700;
                letter-spacing:-0.035em;
            ">{_safe(value)}</div>

            {caption_html}
            {delta_html}

            <div style="
                margin-top:10px;
                color:{status_color};
                font-size:8px;
                font-weight:750;
                letter-spacing:0.10em;
            ">{_safe(str(status).upper())}</div>
        </div>
        """
    )


# ============================================================
# SIGNAL CARD
# ============================================================

def signal_card(
    title,
    metric=None,
    description="",
    status="VALIDATED PATTERN",
    implication=None,
    level=None,
    **kwargs,
):
    """Render a management signal without changing signal logic."""
    if level is not None:
        status = level

    normalized = str(status or "VALIDATED PATTERN").strip().upper()
    color = _status_color(normalized)

    metric_html = ""
    if metric not in (None, ""):
        metric_html = f"""
        <div style="
            margin-top:8px;
            color:{COLORS["text"]};
            font-family:
                'JetBrains Mono',
                'SFMono-Regular',
                Consolas,
                monospace;
            font-size:22px;
            font-weight:700;
        ">{_safe(metric)}</div>
        """

    implication_html = ""
    if implication not in (None, ""):
        implication_html = f"""
        <div style="
            margin-top:13px;
            padding-top:11px;
            border-top:1px solid {COLORS["border_soft"]};
            color:{COLORS["text_muted"]};
            font-size:10px;
            line-height:1.6;
        ">
            <strong style="color:{COLORS["text"]};">
                Business implication:
            </strong>
            {_safe(implication)}
        </div>
        """

    _render(
        f"""
        <div style="
            background:{COLORS["surface"]};
            border:1px solid {COLORS["border"]};
            border-left:3px solid {color};
            border-radius:9px;
            padding:16px 18px;
            margin-bottom:12px;
        ">
            <div style="
                color:{color};
                font-size:8px;
                font-weight:750;
                letter-spacing:0.10em;
            ">{_safe(normalized)}</div>

            <div style="
                margin-top:7px;
                color:{COLORS["text"]};
                font-size:14px;
                font-weight:700;
                line-height:1.35;
            ">{_safe(title)}</div>

            {metric_html}

            <div style="
                margin-top:7px;
                color:{COLORS["text_muted"]};
                font-size:11px;
                line-height:1.6;
            ">{_safe(description)}</div>

            {implication_html}
        </div>
        """
    )


# ============================================================
# TRUST PANEL
# ============================================================

def trust_panel(
    title,
    message=None,
    status="DATA INTEGRITY VERIFIED",
    body=None,
    content=None,
    **kwargs,
):
    """
    Flexible trust panel compatible with all known NOVA call styles.

    Supported examples:
        trust_panel(title="Data Integrity Verified", message="...")
        trust_panel(title="NOVA Trust Boundary", body="...")
        trust_panel(title="...", content="...")
        trust_panel(title="...")
    """
    if message is None:
        message = body

    if message is None:
        message = content

    if message is None:
        message = kwargs.get("text", "")

    if message is None:
        message = ""

    normalized_status = str(status or "DATA INTEGRITY VERIFIED").strip().upper()
    status_color = _status_color(normalized_status, COLORS["emerald"])

    _render(
        f"""
        <div style="
            background:linear-gradient(
                135deg,
                rgba(16,185,129,0.055),
                rgba(34,211,238,0.025)
            );
            border:1px solid rgba(16,185,129,0.22);
            border-radius:9px;
            padding:16px 18px;
            margin:10px 0 18px 0;
        ">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:12px;
            ">
                <div style="
                    color:{COLORS["text"]};
                    font-weight:700;
                    font-size:13px;
                ">{_safe(title)}</div>

                <div style="
                    color:{status_color};
                    font-size:8px;
                    font-weight:750;
                    letter-spacing:0.09em;
                    white-space:nowrap;
                ">{_safe(normalized_status)}</div>
            </div>

            <div style="
                color:{COLORS["text_muted"]};
                font-size:10px;
                line-height:1.65;
                margin-top:8px;
                white-space:pre-line;
            ">{_safe(message)}</div>
        </div>
        """
    )


# ============================================================
# SCOPE BAR
# ============================================================

def scope_bar(
    product="All",
    region="All",
    channel="All",
    segment="All",
    records=0,
    transactions=None,
    date_range="Dataset period",
    filters=None,
    **kwargs,
):
    """Display the current analytical scope."""
    if transactions is not None:
        records = transactions

    if filters is None:
        active_filters = []
        for label, value in (
            ("Product", product),
            ("Region", region),
            ("Channel", channel),
            ("Segment", segment),
        ):
            if value not in (None, "", "All"):
                active_filters.append(f"{label}: {value}")

        filters = (
            "All available records"
            if not active_filters
            else " • ".join(active_filters)
        )

    try:
        record_text = f"{int(records):,}"
    except (TypeError, ValueError):
        record_text = _safe(records)

    _render(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            gap:15px;
            flex-wrap:wrap;
            background:{COLORS["surface"]};
            border:1px solid {COLORS["border_soft"]};
            border-radius:8px;
            padding:9px 12px;
            margin-bottom:18px;
        ">
            <div style="
                color:{COLORS["text_muted"]};
                font-size:10px;
            ">
                <strong style="color:{COLORS["text"]};">
                    SCOPE
                </strong>
                &nbsp; {_safe(record_text)} transactions
            </div>

            <div style="
                color:{COLORS["text_dim"]};
                font-size:9px;
                text-align:right;
            ">
                {_safe(date_range)}
                &nbsp; • &nbsp;
                {_safe(filters)}
            </div>
        </div>
        """
    )


# ============================================================
# KNOWLEDGE / EVIDENCE PANEL
# ============================================================

def knowledge_panel(
    title=None,
    body=None,
    status="FACT",
    known=None,
    unknown=None,
    **kwargs,
):
    """
    Flexible evidence component.

    Supports the current app.py styles:
        knowledge_panel("Empirical Evidence", text, "SOURCE DATA")

    And the two-column knowledge view:
        knowledge_panel(known=[...], unknown=[...])

    Strings are always treated as ONE item, never as a character iterable.
    """
    # Allow callers to use content/message instead of body.
    if body is None:
        body = kwargs.get("content", kwargs.get("message"))

    # Two-column knowledge view.
    if known is not None or unknown is not None:
        known_items = _normalize_items(known)
        unknown_items = _normalize_items(unknown)

        known_rows = []
        for item in known_items:
            known_rows.append(
                f"""
                <div style="
                    padding:9px 0;
                    color:{COLORS["text_muted"]};
                    font-size:10px;
                    line-height:1.55;
                    border-bottom:1px solid {COLORS["border_soft"]};
                ">
                    <span style="
                        color:{COLORS["emerald"]};
                        font-weight:850;
                    ">✓</span>
                    &nbsp; {_safe(item)}
                </div>
                """
            )

        unknown_rows = []
        for item in unknown_items:
            unknown_rows.append(
                f"""
                <div style="
                    padding:9px 0;
                    color:{COLORS["text_muted"]};
                    font-size:10px;
                    line-height:1.55;
                    border-bottom:1px solid {COLORS["border_soft"]};
                ">
                    <span style="
                        color:{COLORS["amber"]};
                        font-weight:850;
                   ">?</span>
                    &nbsp; {_safe(item)}
                </div>
                """
            )

        known_html = "".join(known_rows)
        unknown_html = "".join(unknown_rows)

        if not known_html:
            known_html = (
                f'<div style="color:{COLORS["text_dim"]};font-size:10px;'
                'padding-top:12px;">No explicit evidence items supplied.</div>'
            )

        if not unknown_html:
            unknown_html = (
                f'<div style="color:{COLORS["text_dim"]};font-size:10px;'
                'padding-top:12px;">No explicit unknowns supplied.</div>'
            )

        _render(
            f"""
            <div style="
                display:grid;
                grid-template-columns:repeat(2,minmax(0,1fr));
                gap:14px;
                margin:14px 0;
            ">
                <div style="
                    background:{COLORS["surface"]};
                    border:1px solid {COLORS["border"]};
                    border-radius:9px;
                    padding:15px 17px;
                ">
                    <div style="
                        color:{COLORS["emerald"]};
                        font-size:9px;
                        font-weight:800;
                        letter-spacing:0.10em;
                    ">WHAT NOVA KNOWS</div>
                    {known_html}
                </div>

                <div style="
                    background:{COLORS["surface"]};
                    border:1px solid {COLORS["border"]};
                    border-radius:9px;
                    padding:15px 17px;
                ">
                    <div style="
                        color:{COLORS["amber"]};
                        font-size:9px;
                        font-weight:800;
                        letter-spacing:0.10em;
                    ">WHAT NOVA DOES NOT KNOW</div>
                    {unknown_html}
                </div>
            </div>
            """
        )
        return

    if title is None:
        title = "Evidence"

    normalized = str(status or "FACT").strip().upper()
    color = _status_color(normalized)

    # Render list-like bodies as separate evidence rows.
    body_items = _normalize_items(body)
    if isinstance(body, (list, tuple, set)):
        body_html = "<br>".join(
            f"• {_safe(item)}" for item in body_items
        )
    elif isinstance(body, dict):
        body_html = _safe(_display_text(body))
    else:
        body_html = _safe(body)

    _render(
        f"""
        <div style="
            background:{COLORS["surface"]};
            border:1px solid {COLORS["border"]};
            border-radius:9px;
            padding:15px 17px;
            margin:12px 0;
        ">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:12px;
                flex-wrap:wrap;
            ">
                <div style="
                    color:{COLORS["text"]};
                    font-size:13px;
                    font-weight:700;
                ">{_safe(title)}</div>

                <div style="
                    color:{color};
                    font-size:8px;
                    font-weight:750;
                    letter-spacing:0.09em;
                    white-space:nowrap;
                ">{_safe(normalized)}</div>
            </div>

            <div style="
                color:{COLORS["text_muted"]};
                font-size:10px;
                line-height:1.7;
                margin-top:9px;
                white-space:pre-line;
            ">{body_html}</div>
        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

def nova_footer():
    _render(
        f"""
        <div style="
            margin-top:45px;
            padding-top:15px;
            border-top:1px solid {COLORS["border_soft"]};
            text-align:center;
            color:{COLORS["text_dim"]};
            font-size:9px;
            letter-spacing:0.04em;
        ">
            NOVA Executive Copilot
            &nbsp; • &nbsp;
            Evidence Before Interpretation
            &nbsp; • &nbsp;
            NovaTech Sales Dataset
        </div>
        """
    )

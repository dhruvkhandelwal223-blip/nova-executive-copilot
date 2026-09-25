"""
============================================================
NOVA — EXECUTIVE COPILOT
UI DESIGN SYSTEM — V2
============================================================

Stitch-inspired presentation layer for NOVA.

This module controls:
    - Visual design
    - UI components
    - NOVA branding
    - Epistemic status presentation
    - Executive cards
    - Signal cards
    - Trust panels
    - Scope presentation

This module does NOT control:
    - Business calculations
    - Dataset manipulation
    - AI reasoning
    - Validation logic
    - Signal detection logic

Core principle:
    EVIDENCE BEFORE INTERPRETATION
============================================================
"""

import html
import streamlit as st


# ============================================================
# DESIGN TOKENS
# ============================================================

COLORS = {
    "bg": "#0B0F17",
    "surface": "#0F131C",
    "surface_2": "#141A24",
    "surface_3": "#18202C",
    "border": "#253044",
    "border_soft": "#1B2433",
    "text": "#F8FAFC",
    "text_muted": "#94A3B8",
    "text_dim": "#64748B",
    "emerald": "#10B981",
    "cyan": "#06B6D4",
    "indigo": "#6366F1",
    "purple": "#A855F7",
    "amber": "#F59E0B",
    "rose": "#F43F5E",
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
}


def _safe(value):
    """Escape dynamic text before inserting it into HTML."""
    if value is None:
        return ""
    return html.escape(str(value))


def _render_html(content):
    """Render controlled NOVA HTML through Streamlit."""
    st.html(content)


# ============================================================
# GLOBAL THEME
# ============================================================

def apply_nova_theme():
    css = f"""
    <style>
        .stApp {{
            background:
                radial-gradient(
                    circle at 85% 5%,
                    rgba(16, 185, 129, 0.055),
                    transparent 28%
                ),
                {COLORS["bg"]};
            color: {COLORS["text"]};
        }}

        .main {{
            background: {COLORS["bg"]};
        }}

        .block-container {{
            max-width: 1500px;
            padding-top: 1.7rem;
            padding-bottom: 4rem;
        }}

        html, body, [class*="css"] {{
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

        section[data-testid="stSidebar"] {{
            background: {COLORS["surface"]};
            border-right: 1px solid {COLORS["border_soft"]};
        }}

        section[data-testid="stSidebar"] > div {{
            background: {COLORS["surface"]};
        }}

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {{
            background: {COLORS["surface_2"]};
            border-color: {COLORS["border"]};
            color: {COLORS["text"]};
        }}

        input {{
            color: {COLORS["text"]} !important;
        }}

        .stButton > button {{
            background: {COLORS["surface_2"]};
            color: {COLORS["text"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.15s ease;
        }}

        .stButton > button:hover {{
            border-color: {COLORS["emerald"]};
            color: {COLORS["emerald"]};
        }}

        .stButton > button[kind="primary"] {{
            background: rgba(16, 185, 129, 0.12);
            border-color: rgba(16, 185, 129, 0.42);
            color: {COLORS["emerald"]};
        }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid {COLORS["border"]};
            border-radius: 8px;
            overflow: hidden;
        }}

        hr {{
            border-color: {COLORS["border_soft"]};
        }}

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
    </style>
    """

    _render_html(css)


# ============================================================
# BRAND
# ============================================================

def render_brand():
    _render_html(
        f"""
        <div style="
            padding: 4px 0 18px 0;
            border-bottom: 1px solid {COLORS["border_soft"]};
            margin-bottom: 18px;
        ">
            <div style="
                font-size: 23px;
                font-weight: 800;
                letter-spacing: 0.10em;
                color: {COLORS["text"]};
            ">NOVA</div>

            <div style="
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 0.16em;
                color: {COLORS["emerald"]};
                margin-top: 4px;
            ">EXECUTIVE COPILOT</div>

            <div style="
                font-size: 10px;
                color: {COLORS["text_dim"]};
                margin-top: 8px;
                letter-spacing: 0.03em;
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
):
    """
    Compatible with the NOVA app router.

    active_view:
        Current NOVA module.

    record_count:
        Number of records in the current scope.
    """

    if title is None:
        title = active_view

    if subtitle is None:
        subtitle = (
            f"Executive intelligence workspace • "
            f"{int(record_count):,} records in scope"
        )

    _render_html(
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
                    font-size:11px;
                    font-weight:700;
                    color:{COLORS["emerald"]};
                    letter-spacing:0.13em;
                    text-transform:uppercase;
                    margin-bottom:6px;
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
                border-radius:6px;
                background:rgba(16,185,129,0.06);
                color:{COLORS["emerald"]};
                font-size:9px;
                font-weight:750;
                letter-spacing:0.08em;
                white-space:nowrap;
            ">DATA INTEGRITY VERIFIED</div>
        </div>
        """
    )


# ============================================================
# SECTION HEADER
# ============================================================

def section_header(title, subtitle=None, status=None):
    status_html = ""

    if status:
        status_color = EPISTEMIC_COLORS.get(
            str(status).upper(),
            COLORS["emerald"],
        )
        status_html = f"""
        <span style="
            margin-left:10px;
            padding:3px 8px;
            border-radius:999px;
            background:{status_color}12;
            border:1px solid {status_color}55;
            color:{status_color};
            font-size:9px;
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

    _render_html(
        f"""
        <div style="margin:10px 0 18px 0;">
            <div style="
                display:flex;
                align-items:center;
                gap:4px;
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

def epistemic_badge(level, label=None):
    normalized = str(level).strip().upper()
    color = EPISTEMIC_COLORS.get(
        normalized,
        COLORS["text_dim"],
    )

    label_html = ""
    if label:
        label_html = f"""
        <span style="
            margin-left:8px;
            color:{COLORS["text_dim"]};
            font-size:9px;
        ">{_safe(label)}</span>
        """

    _render_html(
        f"""
        <span style="
            display:inline-block;
            padding:4px 9px;
            border-radius:5px;
            border:1px solid {color}55;
            background:{color}12;
            color:{color};
            font-size:9px;
            font-weight:750;
            letter-spacing:0.075em;
            white-space:nowrap;
        ">{_safe(normalized)}{label_html}</span>
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
):
    status_color = EPISTEMIC_COLORS.get(
        str(status).upper(),
        COLORS["emerald"],
    )

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
    if delta:
        delta_html = f"""
        <div style="
            margin-top:7px;
            color:{COLORS["text_muted"]};
            font-size:10px;
        ">{_safe(delta)}</div>
        """

    _render_html(
        f"""
        <div style="
            background:linear-gradient(
                145deg,
                {COLORS["surface_2"]},
                {COLORS["surface"]}
            );
            border:1px solid {COLORS["border"]};
            border-radius:8px;
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
):
    """
    Compatible with both current and future NOVA signal calls.
    """

    if level is not None:
        status = level

    normalized = str(status).strip().upper()
    color = EPISTEMIC_COLORS.get(
        normalized,
        COLORS["text_dim"],
    )

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
    if implication:
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

    _render_html(
        f"""
        <div style="
            background:{COLORS["surface"]};
            border:1px solid {COLORS["border"]};
            border-left:3px solid {color};
            border-radius:7px;
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
    message,
    status="DATA INTEGRITY VERIFIED",
):
    _render_html(
        f"""
        <div style="
            background:rgba(16,185,129,0.045);
            border:1px solid rgba(16,185,129,0.22);
            border-radius:8px;
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
                    color:{COLORS["emerald"]};
                    font-size:8px;
                    font-weight:750;
                    letter-spacing:0.09em;
                    white-space:nowrap;
                ">{_safe(status)}</div>
            </div>

            <div style="
                color:{COLORS["text_muted"]};
                font-size:10px;
                line-height:1.6;
                margin-top:8px;
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
):
    """
    Displays the current analytical scope.

    Supports the app.py call:
        scope_bar(
            product=...,
            region=...,
            channel=...,
            segment=...,
            records=...,
            date_range=...,
            filters=...,
        )
    """

    if transactions is not None:
        records = transactions

    if filters is None:
        active_filters = []

        for label, value in [
            ("Product", product),
            ("Region", region),
            ("Channel", channel),
            ("Segment", segment),
        ]:
            if value not in (None, "", "All"):
                active_filters.append(
                    f"{label}: {value}"
                )

        filters = (
            "All available records"
            if not active_filters
            else " • ".join(active_filters)
        )

    _render_html(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            gap:15px;
            background:{COLORS["surface"]};
            border:1px solid {COLORS["border_soft"]};
            border-radius:6px;
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
                &nbsp; {_safe(int(records))} transactions
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
    title,
    body=None,
    status="FACT",
    known=None,
    unknown=None,
):
    """
    Flexible evidence panel.

    Primary NOVA usage:
        knowledge_panel(title, body, status)

    Legacy-compatible usage:
        knowledge_panel(known=[...], unknown=[...])
    """

    if known is not None or unknown is not None:
        known_items = known or []
        unknown_items = unknown or []

        known_html = "".join(
            f"""
            <div style="
                margin-top:7px;
                color:{COLORS["text_muted"]};
                font-size:10px;
                line-height:1.5;
            ">
                <span style="
                    color:{COLORS["emerald"]};
                    font-weight:800;
                ">✓</span>
                &nbsp; {_safe(item)}
            </div>
            """
            for item in known_items
        )

        unknown_html = "".join(
            f"""
            <div style="
                margin-top:7px;
                color:{COLORS["text_muted"]};
                font-size:10px;
                line-height:1.5;
            ">
                <span style="
                    color:{COLORS["amber"]};
                    font-weight:800;
                ">?</span>
                &nbsp; {_safe(item)}
            </div>
            """
            for item in unknown_items
        )

        _render_html(
            f"""
            <div style="
                display:grid;
                grid-template-columns:repeat(2,minmax(0,1fr));
                gap:12px;
                margin:14px 0;
            ">
                <div style="
                    background:{COLORS["surface"]};
                    border:1px solid {COLORS["border"]};
                    border-radius:7px;
                    padding:15px;
                ">
                    <div style="
                        color:{COLORS["emerald"]};
                        font-size:9px;
                        font-weight:750;
                        letter-spacing:0.09em;
                    ">WHAT NOVA KNOWS</div>
                    {known_html}
                </div>

                <div style="
                    background:{COLORS["surface"]};
                    border:1px solid {COLORS["border"]};
                    border-radius:7px;
                    padding:15px;
                ">
                    <div style="
                        color:{COLORS["amber"]};
                        font-size:9px;
                        font-weight:750;
                        letter-spacing:0.09em;
                    ">WHAT NOVA DOES NOT KNOW</div>
                    {unknown_html}
                </div>
            </div>
            """
        )
        return

    if isinstance(body, (list, tuple)):
        body_text = "<br>".join(
            f"• {_safe(item)}" for item in body
        )
    else:
        body_text = _safe(body)

    normalized = str(status).strip().upper()
    color = EPISTEMIC_COLORS.get(
        normalized,
        COLORS["text_dim"],
    )

    _render_html(
        f"""
        <div style="
            background:{COLORS["surface"]};
            border:1px solid {COLORS["border"]};
            border-radius:7px;
            padding:15px 17px;
            margin:12px 0;
        ">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:12px;
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
                line-height:1.65;
                margin-top:9px;
            ">{body_text}</div>
        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

def nova_footer():
    _render_html(
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

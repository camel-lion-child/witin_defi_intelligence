import streamlit as st
from layout import setup_page
from styles import card

setup_page("WITIN")



st.markdown(
    """
    <div class="hero-title">The future of finance, decoded.</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="muted" style="max-width:820px;">
    WITIN is a research-driven analytics company focused on the future of finance, turning on-chain data into actionable insights on DeFi protocols and market dynamics.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

st.divider()

st.markdown("## Who we serve")
c1, c2, c3 = st.columns(3)
with c1:
    card("Private investors", "Clarity", "Independent, research-grade analysis.")
with c2:
    card("Institutions", "Risk signals", "Protocol behavior & systemic exposure.")
with c3:
    card("Analysts", "Transparency", "Clean data + reproducible logic.")

st.divider()

st.markdown("## What we deliver")
left, right = st.columns([1, 1], gap="large")
with left:
    st.markdown(
        """
        <div class="card">
          <div class="card-title">Research focus</div>
          <ul class="muted" style="margin-top:10px;">
            <li>Liquidation dynamics & risk concentration.</li>
            <li>Protocol monitoring & behavior.</li>
            <li>Market-level liquidity & flows.</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        """
        <div class="card">
          <div class="card-title">Approach</div>
          <ul class="muted" style="margin-top:10px;">
            <li>ETL pipelines + structured storage.</li>
            <li>Transparent assumptions.</li>
            <li>Reproducible analytics.</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    "<div class='muted' style='margin-top:12px;'>WITIN focuses on research and analytics — not financial advice.</div>",
    unsafe_allow_html=True,
)

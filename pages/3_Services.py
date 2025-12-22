import streamlit as st
from app.layout import setup_page

setup_page("Dashboards — WITIN")

st.title("Services")
st.caption("Clean deliverables. Minimal noise.")

st.markdown("""
### What We Do
- On-Chain Research & Analysis: Deep analysis of DeFi protocols, user behavior, and systemic risk using raw on-chain data.
- Decision Intelligence: Translating complex blockchain data into clear insights for strategic financial decisions.
- Protocol & Market Monitoring: Ongoing analysis of protocol health, liquidity dynamics, and structural changes.
- Custom Research: Bespoke research tailored to investors, builders, and capital allocators.

### Who We Help & How
- Understand DeFi protocol risk and mechanics.
- Evaluate on-chain liquidity and user behavior.
- Monitor market stress and systemic vulnerabilities.
- Support long-term allocation and strategy decisions.

### Our Focus
- DeFi Research.
- On-Chain Data Analysis.
- Decision Intelligence.
""")

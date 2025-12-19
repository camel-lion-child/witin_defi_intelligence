import streamlit as st
from app.layout import setup_page

setup_page("Dashboards — WITIN")

st.title("About")

st.markdown("""
"WITIN was born from my long-standing interest in finance, data, and how financial systems evolve under stress.

With a background in data analysis and experience working with financial data, I became increasingly drawn to decentralized finance — not for speculation, but for the questions it raises around risk, transparency, and capital allocation.

While WITIN is rooted in my own research, it is not a solo effort.
I actively collaborate with a network of data analysts, data scientists, and data engineers who share the same curiosity and analytical rigor around DeFi and financial systems.

Together, we study decentralized finance with depth and discipline, working directly with raw on-chain data to transform complex blockchain activity into insights that support thoughtful, long-term decision-making."
            
Huyen Tran, Founder.
            """)

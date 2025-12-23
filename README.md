# WITIN — DeFi & Market Intelligence Platform

**WITIN** is a research-driven analytics platform focused on decoding the future of finance.
The project delivers clean, macro-level intelligence on decentralized financial markets by
transforming raw on-chain and market data into decision-ready insights.

This repository represents a **production-style data product** combining:
- Automated data pipelines (ETL).
- Structured storage (analytics-ready marts).
- A Streamlit-based research interface for distribution.

---

## Purpose

WITIN is designed for:

- Private investors
- Institutions
- Analysts and researchers

who seek **clarity**, **structure**, and **context** in modern financial systems built on
transparent, decentralized infrastructure.

The platform prioritizes:
- Market structure over short-term price noise.
- Capital allocation and protocol dynamics.
- Research-grade presentation over trading interfaces.

---

## What’s Inside

### 1) Macro DeFi Dashboards (DefiLlama-style)
- Total DeFi TVL (time-series).
- TVL trends and short-term changes.
- Protocol landscape (Top protocols by TVL).
- Category-level capital allocation (derived from protocol data).

> Focus: *Where is capital deployed, and how is the system evolving?*

---

### 2) Markets Page (Binance-based)
- Clean price context for major crypto assets.
- Multi-asset comparison.
- Adjustable time windows.
- Research-oriented presentation (not a trading terminal).

Assets include BTC, ETH, SOL, ADA, XRP, LINK, UNI, DOGE, TRX, AAVE, and others.

---

### 3) Research-Oriented Frontend
Built with **Streamlit** as a lightweight research website:
- Home: positioning & narrative.
- Dashboards: macro intelligence.
- Markets: price context.
- Services / About / Contact: company-facing pages.

---

## Architecture

- Streamlit multi-page app used for interactive analytics and visualization.
- Market data fetched from Binance public REST API (US endpoint for cloud stability) and DefiLlama.
- Data ingestion and transformations handled via lightweight Python pipelines.
- Analytical datasets stored as Parquet and DuckDB for fast local access.

---

## Tech Stack

- Python 3.9+.

- Pandas.

- Requests.

- Parquet / PyArrow.

- Streamlit.

- DefiLlama API (DeFi macro data).

- Binance API (market prices).

---

## Roadmap (High-level)

- Chain-level capital flow dashboards.

- DeFi risk & stress indicators.

- Protocol deep-dives (lending, DEX, perps).

- External dashboard references (e.g. Dune).

- Advanced on-chain position analysis.




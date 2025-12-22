import streamlit as st

def inject_global_styles():
    st.markdown(
        """
        <style>
        /* ===== Base ===== */
        .stApp { background: #0f1115; color: #e7e7e7; }
        html, body, [class*="css"]  {
            font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
        }
        .block-container { padding-top: 2.2rem; padding-bottom: 2.6rem; max-width: 1080px; }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #0c0e12;
            border-right: 1px solid rgba(255,255,255,0.06);
        }

        /* ===== Typography ===== */
        h1, h2, h3 { letter-spacing: -0.02em; }
        .muted {
            color: rgba(231,231,231,0.70);
            font-size: 0.95rem;
            line-height: 1.55rem;
        }

        /* ===== HERO TYPOGRAPHY (luxury) ===== */
        .hero-title {
            font-size: 2.6rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            line-height: 1.15;
            margin-bottom: 0.6rem;
        }
        .hero-subtitle {
            font-size: 1.05rem;
            font-weight: 400;
            letter-spacing: 0.01em;
            line-height: 1.6;
            color: rgba(231,231,231,0.75);
            max-width: 720px;
        }

        /* ===== Cards ===== */
        .card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 16px 18px;
        }
        .card-title {
            font-size: 0.9rem;
            color: rgba(231,231,231,0.70);
            margin-bottom: 6px;
        }
        .card-value {
            font-size: 1.55rem;
            font-weight: 650;
            margin: 0;
        }
        .pill {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            color: rgba(231,231,231,0.85);
            font-size: 0.82rem;
        }

        /* Buttons */
        .stButton>button {
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(255,255,255,0.06);
            color: #e7e7e7;
            padding: 0.55rem 1rem;
        }
        .stButton>button:hover {
            border-color: rgba(255,255,255,0.20);
            background: rgba(255,255,255,0.10);
        }

        /* Dataframe */
        [data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.08);
        }

        /* Divider */
        hr { border-color: rgba(255,255,255,0.08) !important; }

        /* Hide Streamlit footer */
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def card(title: str, value: str, caption=None):
    cap_html = f'<div class="muted" style="margin-top:6px;">{caption}</div>' if caption else ""
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
            {cap_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


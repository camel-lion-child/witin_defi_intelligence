from pathlib import Path
import streamlit as st
from app.styles import inject_global_styles

ROOT = Path(__file__).resolve().parents[1]
LOGO_PATH = ROOT / "app" / "assets" / "witin.png"

def setup_page(page_title: str = "WITIN"):
    st.set_page_config(page_title=page_title, layout="wide")
    inject_global_styles()

    with st.sidebar:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=60)  
        st.markdown("### WITIN")
        st.markdown(
            "<div class='muted'>Where Data Becomes Conviction.</div>",
            unsafe_allow_html=True,
        )
        st.divider()


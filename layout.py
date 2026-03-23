"""I set up the Streamlit page layout by configuring the page, injecting global styles, 
and defining a consistent sidebar with branding elements.

Ce module configure la mise en page Streamlit en définissant les paramètres de page, 
en injectant les styles globaux et en créant une sidebar cohérente avec les éléments de branding."""

from pathlib import Path
import streamlit as st
from styles import inject_global_styles

ROOT = Path(__file__).resolve().parents[1] #resolve project root to build absolute paths
LOGO_PATH = ROOT / "app" / "assets" / "witin.png" #path for logo

def setup_page(page_title: str = "WITIN"):
    st.set_page_config(page_title=page_title, layout="wide") #configure streamlit page
    inject_global_styles() #inject global CSS style
    #sidebar layout
    with st.sidebar:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=60)  
        st.markdown("### WITIN")
        st.markdown(
            "<div class='muted'>Where Data Becomes Conviction.</div>",
            unsafe_allow_html=True,
        )
        st.divider() #visual separator


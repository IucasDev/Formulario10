import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="Sistema EKT - Formulario de Viabilidade",
    page_icon="EKT",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header[data-testid="stHeader"] { display: none; }
    .stDeployButton { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

html_path = Path(__file__).parent / "index.html"

if not html_path.exists():
    st.error("Arquivo index.html nao encontrado.")
    st.stop()

html_content = html_path.read_text(encoding="utf-8")

components.html(html_content, height=1150, scrolling=True)

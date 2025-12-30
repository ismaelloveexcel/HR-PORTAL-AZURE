#!/usr/bin/env python3
"""
HR Portal - React Application
Serves the pre-built React app through Streamlit.
"""
import streamlit as st
import os

st.set_page_config(
    page_title="HR Portal | Baynunah",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    .main .block-container {padding-top: 0 !important;}
    section.main > div {padding: 0 !important;}
    .stApp {background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);}
    iframe {border: none !important;}
</style>
""", unsafe_allow_html=True)

html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'index.html')

if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=800, scrolling=True)
else:
    st.error("Application not built. Please run 'npx vite build' first.")

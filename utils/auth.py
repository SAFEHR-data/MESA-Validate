"""
auth.py - basic authentication and authorization using auth.yaml
"""
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
import yaml

with open(Path(__file__).parents[1] / 'auth.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.loader.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

def require_login():
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)
"""
auth.py - basic authentication and authorization using auth.yaml
"""
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit.logger import get_logger

logger = get_logger(__name__)


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
    finally:
        if st.session_state.get('authentication_status'):
            # Add logout button
            authenticator.logout()
            username = st.session_state.get("name")
            logger.info(f"Pageload by {username}")
            st.write(f"Welcome *{username}*")
        else: 
            st.stop()


import streamlit as st
from utils.api import login as api_login, register as api_register, get_me

def init_session():
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "Beranda"

def is_authenticated():
    return st.session_state.token is not None and st.session_state.user is not None

def is_admin():
    return is_authenticated() and st.session_state.user.get("role") == "admin"

def get_token():
    return st.session_state.token

def get_username():
    if st.session_state.user:
        return st.session_state.user.get("username", "")
    return ""

def do_login(username, password):
    data, err = api_login(username, password)
    if err:
        return data.get("error", "Login gagal")
    st.session_state.token = data["access_token"]
    user_data, _ = get_me(st.session_state.token)
    if not user_data.get("error"):
        st.session_state.user = user_data
    return None

def do_register(username, password):
    data, err = api_register(username, password)
    if err:
        return data.get("error", "Registrasi gagal")
    st.session_state.token = data["access_token"]
    user_data, _ = get_me(st.session_state.token)
    if not user_data.get("error"):
        st.session_state.user = user_data
    return None

def do_logout():
    st.session_state.token = None
    st.session_state.user = None
    st.rerun()

def refresh_user():
    if st.session_state.token:
        user_data, err = get_me(st.session_state.token)
        if not err and not user_data.get("error"):
            st.session_state.user = user_data
            return True
        st.session_state.token = None
        st.session_state.user = None
    return False

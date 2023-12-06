import streamlit as st
st.set_page_config(layout="wide", page_title="Tools for the IAL community")
from predict_page import show_predict_page
from explore_page import show_explore_page
from suggestion_page import show_suggestion_page
from worldviews_page import show_worldviews_page
from MainPage import show_main_page

page = st.sidebar.selectbox("Choose a page", ("Main Page", "Topic Comparison", "Quality Comparison", "Views per country"))#, "Suggestion Page"))

if page == "Topic Comparison":
    show_predict_page()
elif page == "Quality Comparison":
    show_explore_page()
elif page == "Main Page":
    show_main_page()
else:
    show_worldviews_page()
'''elif page == "Suggestion Page":
    show_suggestion_page()'''
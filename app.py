import streamlit as st
st.set_page_config(layout="wide", page_title="Tools for the IAL community")
from topics_page import show_topics_page
from quality_page import show_quality_page
from suggestion_page import show_suggestion_page
from worldviews_page import show_worldviews_page
from MainPage import show_main_page

page = st.sidebar.selectbox("Choose a page", ("Main Page", "Topic Comparison", "Quality Comparison", "Views per country", "Suggestion Page"))

if page == "Topic Comparison":
    show_topics_page()
elif page == "Quality Comparison":
    show_quality_page()
elif page == "Main Page":
    show_main_page()
elif page == 'Views per country':
    show_worldviews_page()
else:
    show_suggestion_page()
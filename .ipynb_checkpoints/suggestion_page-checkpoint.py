import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
import plotly.express as px
import numpy as np

@st.cache
def load_data(file_name):
    df = pd.read_csv(file_name)
    return df

df = load_data('mean_predicted_quality.csv')
df=df.drop(columns=['Unnamed: 0'])
df_qualities_features_top100 = load_data('df_qualities_features_top100.csv')


def show_suggestion_page():
    st.markdown("<h1 style='text-align: center; color: #307473;'>Suggestions Page</h1>", unsafe_allow_html=True)
    
    st.write("""## Recomendations Searcher""")
    with st.form("my_form"):
        st.write("Choose a wiki and an IAL to get suggestions of popular nontranslated articles that you can write on")
        from_lang = st.text_input('Language code', placeholder='-- e.g., en for English')
        ial = st.selectbox("Choose an IAL", ('Simple English', 'Esperanto', 'Ido', 'Volapuk', 'Interlingua', 'Interlingue', 'Novial'))
        slider_val = st.slider("Number of suggestions", 1, 30, 5)
        #checkbox_val = st.checkbox("Form checkbox")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        #if submitted:
         #   st.write("slider", slider_val, "checkbox", checkbox_val)
            
    if submitted:
            show_suggestions()
    #st.write("Outside the form")
    
def show_suggestions():
    st.markdown("<h1 style='text-align: center; color: #307473;'>Results:</h1>", unsafe_allow_html=True)
    col0, col1, col2 = st.columns(3)
    col1.write("## [Cat](https://en.wikipedia.org/wiki/Cat) - 10k views")
    col1.write("## [Dog](https://en.wikipedia.org/wiki/Dog) - 8k views")
    col1.write("## [United States](https://en.wikipedia.org/wiki/United_States) - 7k views")
    col1.write("## [Lady Gaga](https://en.wikipedia.org/wiki/Lady_Gaga) - 6k views")
    col1.write("## [Catalonia](https://en.wikipedia.org/wiki/Catalonia) - 6k views")
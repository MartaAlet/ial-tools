import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
import plotly.express as px
import pypopulation
import pickle

@st.cache
def load_data(file_name):
    df = pd.read_csv(file_name)
    return df
def load_dict(dict_name):
    data = pd.read_pickle(dict_name)
    return data
topics = load_dict('geo_views.pkl')
#df = load_data('mean_predicted_quality.csv')
#df=df.drop(columns=['Unnamed: 0'])
#df_qualities_features_top100 = load_data('df_qualities_features_top100.csv')


def show_worldviews_page():
    st.markdown("<h1 style='text-align: center; color: #307473;'>Views per country</h1>", unsafe_allow_html=True)
    st.write("""## Geographic distribution of views""")
    list_of_langs = ['en', 'es', 'ca', 'simple', 'eo', 'io', 'ia', 'vo', 'ie', 'nov']
    lang_to_language={'simple':'Simple English', 'eo':'Esperanto', 'io':'Ido', 'vo':'Volapuk', 'ia':'Interlingua', 'ie':'Interlingue', 'nov':'Novial', 'en': 'English', 'es':'Spanish', 'ca':'Catalan'}
    for lang in list_of_langs:
        language = lang_to_language[lang]
        fig = px.choropleth(views_per_country_df[lang], locations="Alpha-3 code",
                            color="Views/Population", 
                            hover_name="Country",
                            color_continuous_scale=px.colors.sequential.Plasma,
                            title = "Views/Population per country of the "+language+" Wikipedia")
        st.plotly_chart(fig)
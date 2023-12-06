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
views_per_country_df = load_dict('geo_views.pkl')
#df = load_data('mean_predicted_quality.csv')
#df=df.drop(columns=['Unnamed: 0'])
#df_qualities_features_top100 = load_data('df_qualities_features_top100.csv')

def show_worldviews_page():
    st.markdown("<h1 style='text-align: center; color: #307473;'>Views per country</h1>", unsafe_allow_html=True)
    st.write("""## Geographic distribution of views""")
    st.write("Below you can see the distribution of views for each language. The color is according to the views/population of the country ratio. To see the information of each country please hover over the map, this will also show you the exact number of views (views_ceil).")
    list_of_langs = ['en', 'es', 'ca', 'simple', 'eo', 'io', 'ia', 'vo', 'ie', 'nov']
    lang_to_language={'simple':'Simple English', 'eo':'Esperanto', 'io':'Ido', 'vo':'Volapük', 'ia':'Interlingua', 'ie':'Interlingue', 'nov':'Novial', 'en': 'English', 'es':'Spanish', 'ca':'Catalan'}
    for lang in list_of_langs:
        language = lang_to_language[lang]
        fig = px.choropleth(views_per_country_df[lang], locations="Alpha-3 code", color="Views/Population", hover_name="Country", color_continuous_scale=px.colors.sequential.Plasma, title = "Views/Population per country of the "+language+" Wikipedia",  hover_data=['views_ceil'])
        fig.update_layout(title=dict(font=dict(size=20)), title_y=0.76, paper_bgcolor='white', plot_bgcolor='white')
        fig.update_layout(
        margin={'l':0,'r':0, 'b':0}
    )
        st.plotly_chart(fig)
        st.write(len(views_per_country_df[lang][views_per_country_df[lang]['rank'].isna()==False]))
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
import plotly.express as px
import pypopulation

@st.cache
def load_data(file_name):
    df = pd.read_csv(file_name)
    return df

df = load_data('mean_predicted_quality.csv')
df=df.drop(columns=['Unnamed: 0'])
df_qualities_features_top100 = load_data('df_qualities_features_top100.csv')


def show_worldviews_page():
    st.markdown("<h1 style='text-align: center; color: #307473;'>Views per country</h1>", unsafe_allow_html=True)
    
    st.write("""## Mean Predicted Quality""")
    
    col0, col1 = st.columns(2)
    col0.dataframe(df)
    fig = px.bar(df, x="language", y="mean predicted quality", color="language", title="Mean Predicted Quality")
    col1.plotly_chart(fig)
    st.write("""## Analysis for the top 100 articles of each IAL""")
    features = ['length (bytes)', 'media', 'wikilinks', 'categories', 'headings', 'references']
    for feature in features:
        fig = px.bar(df_qualities_features_top100[df_qualities_features_top100['feature']==feature], x="language", y="count", color="language", title=feature+" count for each IAL")
        st.plotly_chart(fig)
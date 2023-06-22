import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.offline as pyo
import json

'''
def load_dict(dict_name):
    with open(dict_name, 'rb') as file:
        data = pickle.load(file)
    return data'''
def load_dict(dict_name):
    data = pd.read_pickle(dict_name)
    return data

regions_top100 = load_dict('regions_top100.pkl')
topics = load_dict('topics.pkl')
topics_minus_geo = load_dict('topics_minus_geo.pkl')
regions_per_lang = load_dict('regions_per_lang.pkl')
topics_langs_relevant100 = load_dict('topics_langs_relevant.pkl')
topics_minus_geo_top100 = load_dict('topics_minus_geo_top100.pkl')
#df_topics = pd.read_csv("topicsForAllWikidataItems2023-01-16_ials_plus_en_es_ca.csv.gz")

def display_scatter_polar(dic, topic, score, title):
    lang_to_language={'simple':'Simple English', 'eo':'Esperanto', 'io':'Ido', 'vo':'Volapuk', 'ia':'Interlingua', 'ie':'Interlingue', 'nov':'Novial'}
    data=[]
    for lang in dic.keys():
        topics = dic[lang][topic]
        scores_1 = list(dic[lang][score])
        #scores_1 = [*scores_1, scores_1[0]]
        print(scores_1)

        data.append(go.Scatterpolar(r=scores_1, theta=topics, fill='toself', name=lang_to_language[lang]))
    fig = go.Figure(
        data=data,
        layout=go.Layout(
            title=go.layout.Title(text=title),
            polar={'radialaxis': {'visible': True}},
            showlegend=True
        )
    )

    return fig

def rename_col_1(col_name):
    list_ = col_name.split('.')
    return list_[0]
def rename_col_2(col_name):
    list_ = col_name.split('.')
    return list_[1]
def rename_col_3(col_name):
    list_ = col_name.split('.')
    if len(list_)<3:
        return list_[1]
    return list_[2]

def show_predict_page():
    st.markdown("<h1 style='text-align: center; color: #307473;'>Topic comparison among IALs</h1>", unsafe_allow_html=True)
    #st.write("check out this [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
    st.write("Using the [Language-agnostic Topic Classification API](https://wiki-topic.toolforge.org/topic) developed by Isaac (WMF) as part of Wikimedia Research, we can view the distribution of topics of the articles of each of the pages. If we give the API the wikipedia’s language and an article title we will get for each of the topics in this page the probability that the article belongs to that topic.")
    st.markdown("<h3 style='text-align: left; color: #307473;'>Topics of articles for each IAL:</h3>", unsafe_allow_html=True)
    '''with open('figure_topics.json', 'r') as f:
        v = json.loads(f.read())
    fig = go.Figure(data=v['data'], layout=v['layout'])
    st.plotly_chart(fig)'''
    col0, col1 = st.columns(2)
    col0.plotly_chart(display_scatter_polar(topics, 'topic', 'value', 'Topics comparison'))
    col1.plotly_chart(display_scatter_polar(topics_langs_relevant100, 'topic', 'score', 'Topics comparison - Top 100 articles'))
    st.write('In both cases we see that Geography.Regions is a very popular topic, meaning we can easily relate the subject of the articles to a region. For this region I decided to do this once more but without this topic so that we could get a better image.')
    st.markdown("<h3 style='text-align: left; color: #307473;'>Topics of articles for each IAL without Geography.Regions:</h3>", unsafe_allow_html=True)
    col2, col3 = st.columns(2)
    col2.plotly_chart(display_scatter_polar(topics_minus_geo, 'topic', 'value', 'Topics comparison (Without Geography.Regions)'))
    col3.plotly_chart(display_scatter_polar(topics_minus_geo_top100, 'topic', 'score', 'Topics comparison (Without Geography.Regions) - Top 100 articles'))
    st.markdown("<h3 style='text-align: left; color: #307473;'>Regions of articles for each IAL:</h3>", unsafe_allow_html=True)
    #st.write(regions_top100)
    regions_per_lang_ = dict()
    for lang in regions_per_lang.keys():
        regions_per_lang_[lang]= pd.DataFrame({'topic':regions_per_lang[lang].index, 'value':regions_per_lang[lang].values})
        regions_per_lang_[lang]=regions_per_lang_[lang].sort_values(by = 'topic')
    col4, col5 = st.columns(2)
    col4.plotly_chart(display_scatter_polar(regions_per_lang_, 'topic', 'value', 'Geography.Regions comparison'))
    col5.plotly_chart(display_scatter_polar(regions_top100, 'topic', 'score', 'Geography.Regions comparison - Top 100 articles'))
        
def plot_topics():
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots

    # create a 5x2 subplot grid with pie subplots
    #fig = make_subplots(rows=5, cols=2, specs=[[{'type':'pie'}]*2]*5)
    fig = make_subplots(rows=5, cols=2, specs=[[{'type':'pie'}]*2]*5,
                        vertical_spacing=0.01, horizontal_spacing=0.05,
                        ) #subplot_titles=[f"Dataframe {i+1}" for i in range(10)],

    # iterate over the list of dataframes and plot a pie chart for each one
    for i, df in enumerate(list_of_dataframes):
        # calculate the value counts for the 'topic' column
        counts = df['topic'].value_counts()
        dt = pd.DataFrame(df[['topic_level1', 'topic', 'topic_full']].value_counts()).reset_index().rename(columns={0: 'count'})
        dt['lang']='  '#list_of_langs[i]
        # create a pie chart with the value counts
        pie = px.sunburst(dt, path=['lang', 'topic_level1', 'topic'], values='count')

        # add the pie chart to the subplot grid
        fig.add_trace(pie.data[0], row=i//2+1, col=i%2+1)#, text = lang_to_language[list_of_langs[i]])
        #fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    # update the layout with title and axis labels
    j_ = [0.915, 0.711, 0.50, 0.29, 0.09]
    i_ = [0.22, 0.78]
    fig.update_layout(
        height=2000, width=1000,
        title="Distribution of Topics",
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        annotations=[dict(text=lang, x=i_[i%2], y=j_[i//2], font_size=20, showarrow=False, align="center") for i,lang in enumerate(list_of_langs)]
    )
    #fig.update_traces(textposition='inside')
    '''
    fig.update_layout(
        height=2000, width=1000,
        title="Distribution of Topics")'''
    # show the figure
    st.plotly_chart(fig)

import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.offline as pyo

'''
def load_dict(dict_name):
    with open(dict_name, 'rb') as file:
        data = pickle.load(file)
    return data'''
def load_dict(dict_name):
    data = pd.read_pickle(dict_name)
    return data

'''
regions_top100 = load_dict('regions_top100.pkl')
topics = load_dict('topics.pkl')
topics_minus_geo = load_dict('topics_minus_geo.pkl')
regions_per_lang = load_dict('regions_per_lang.pkl')
topics_langs_relevant100 = load_dict('topics_langs_relevant.pkl')
topics_minus_geo_top100 = load_dict('topics_minus_geo_top100.pkl')'''
regions_top100 = load_dict('regions_top100.pkl')
topics = load_dict('topics.pkl')
topics_minus_geo = load_dict('topics_minus_geo.pkl')
regions_per_lang = load_dict('regions_per_lang.pkl')
topics_langs_relevant100 = load_dict('topics_langs_relevant.pkl')
topics_minus_geo_top100 = load_dict('topics_minus_geo_top100.pkl')
'''
regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def cluster_data(data):
    clustering = AgglomerativeClustering(linkage='ward', n_clusters=5).fit(data[['Annual_income','Spending_score']])
    cluster_id = clustering.labels_
    return cluster_id
    
def predict_cluster_id(point, data, cluster_id):
    dict_distances = dict()
    cluster_ids = [0,1,2,3,4]
    for cluster in cluster_ids:
        data_cluster=data.iloc[[x for x in range(len(cluster_id)) if cluster_id[x]==cluster]]
        mean_ai = data_cluster['Annual_income'].mean()
        mean_ss = data_cluster['Spending_score'].mean()
        centroid = np.array([mean_ai, mean_ss])
        dict_distances[cluster] = np.linalg.norm(point - centroid)
    return min(dict_distances, key=dict_distances.get)

def load_data():
    df = pd.read_table('../topics_all_wikipedia_articles_202012_SAMPLE_1pct.tsv')
    return df

data = load_data()

def display_metrics_cluster(cluster, cluster_id, data):
    data_cluster=data.iloc[[x for x in range(len(cluster_id)) if cluster_id[x]==cluster]]
    max_ai=data_cluster['Annual_income'].max()
    min_ai=data_cluster['Annual_income'].min()
    std_ai=data_cluster['Annual_income'].std()

    max_ss=data_cluster['Spending_score'].max()
    min_ss=data_cluster['Spending_score'].min()
    std_ss=data_cluster['Spending_score'].std()
    st.write(f"#### Cluster {cluster} metrics") 
    col0, col1, col2, col3 = st.columns(4)
    col0.write("**Annual\n Income:**")
    col1.metric("Maximum", str(max_ai), "%.2f" % (max_ai-60.56))
    col2.metric("Minimum", str(min_ai), "%.2f" % (min_ai-60.56))
    col3.metric("Standard Deviation", "%.2f" %(std_ai), "")
    col0, col1, col2, col3 = st.columns(4)
    col0.write("**Spending\n Score:**")
    col1.metric("Maximum", str(max_ss), "%.2f" % (max_ss-50.2))
    col2.metric("Minimum", str(min_ss), "%.2f" % (min_ss-50.2))
    col3.metric("Standard Deviation", "%.2f" %(std_ss), "")
    
'''
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


def show_predict_page():
    st.markdown("<h1 style='text-align: center; color: #307473;'>Topic comparison among IALs</h1>", unsafe_allow_html=True)
    #st.write("check out this [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
    st.write("Using the [Language-agnostic Topic Classification API](https://wiki-topic.toolforge.org/topic) developed by Isaac (WMF) as part of Wikimedia Research, we can view the distribution of topics of the articles of each of the pages. If we give the API the wikipedia’s language and an article title we will get for each of the topics in this page the probability that the article belongs to that topic.")
    st.markdown("<h3 style='text-align: left; color: #307473;'>Topics of articles for each IAL:</h3>", unsafe_allow_html=True)
    col0, col1 = st.columns(2)
    col0.plotly_chart(display_scatter_polar(topics, 'topic', 'value', 'Topics comparison'))
    col1.plotly_chart(display_scatter_polar(topics_langs_relevant100, 'topic', 'score', 'Topics comparison - Top 100 articles'))
    st.write('In both cases we see that Geography.Regions is a very popular topic, meaning we can easily relate the subject of the articles to a region. For this region I decided to do this once more but without this topic so that we could get a better image.')
    st.markdown("<h3 style='text-align: left; color: #307473;'>Topics of articles for each IAL without Geography.Regions:</h3>", unsafe_allow_html=True)
    col2, col3 = st.columns(2)
    col2.plotly_chart(display_scatter_polar(topics_minus_geo, 'topic', 'value', 'Topics comparison (Without Geography.Regions)'))
    col3.plotly_chart(display_scatter_polar(topics_minus_geo_top100, 'topic', 'score', 'Topics comparison (Without Geography.Regions) - Top 100 articles'))
    st.markdown("<h3 style='text-align: left; color: #307473;'>Regions of articles for each IAL:</h3>", unsafe_allow_html=True)
    '''
    fig, ax = plt.subplots()
    
    cluster_id = cluster_data(data)
    
    scatter=ax.scatter(data.Annual_income, data.Spending_score, c=cluster_id, cmap ='rainbow') 
    plt.title('Clustering of Annual income per Spending_score')
    plt.xlabel('Annual income')
    plt.ylabel('Spending_score')
    ax.legend(*scatter.legend_elements(),loc="upper right", title="Clusters")
    st.pyplot(fig)
    st.markdown("<h3 style='text-align: left; color: #307473;'>We need some information to predict the cluster ID of a customer:</h3>", unsafe_allow_html=True)
    
    annual_income = st.text_input('Annual Income')
    spending_score = st.slider("Spending Score", 0, 160, 3)

    ok = st.button("Calculate Cluster ID")
    text = dict()
    text[0] = "This group is composed by people with high annual income but low spending score. What the metrics tells us about this group of people is that even though they have high salaries, they refrain from spending a lot of money."
    text[1] = "This group has people who are in the middle of both the spending score and annual income ranges (they are the average customer). We find that this is the largest group out of the five. So even though this group has average metrics, it's highly valuable because it's the most common group and where we will find the largest amount of customers, so pleasing them should be important to the company."
    text[2] = "This group contains the customers that have high annual incomes and high spending scores. This maybe be the most important one of them all simply based on their high spending scores."
    text[3] = "This group has customers that have high spending scores despite their low salaries. Their are appealing to the company because of their high spendings."
    text[4] = "This group has low annual income and spending socre. Based on their salary values we can say that the spending scores of the customers in this group can't have that much grouth unless the prices are lowered to some extent."
    colors = {0: 'Purple', 1: 'SkyBlue', 2: 'LightGreen', 3: 'Orange', 4: 'Red'}
    if ok:
        if len(annual_income)==0 or int(annual_income)<=0:
            warning = '<p style="color:Red;">Please write an Annual income greater than 0</p>'
            st.markdown(warning, unsafe_allow_html=True)
        else:
            point = np.array([int(annual_income), int(spending_score)])
            point_id = predict_cluster_id(point, data, cluster_id)
            result = '<h4>The estimated cluster for this customer is: </h4><h3 style="text-align: center; color:'+colors[point_id]+';">Cluster '+str(point_id)+'</h3>'
            st.markdown(result, unsafe_allow_html=True)
            st.write(text[point_id])
            display_metrics_cluster(point_id, cluster_id, data)
            note = '<p style="text-align: center; color:Grey";>The arrows display the distance from the average values of the dataset</p>'
            st.markdown(note, unsafe_allow_html=True)
        '''
    st.write(regions_top100)
    regions_per_lang_ = dict()
    for lang in regions_per_lang.keys():
        regions_per_lang_[lang]= pd.DataFrame({'topic':regions_per_lang[lang].index, 'value':regions_per_lang[lang].values})
        regions_per_lang_[lang]=regions_per_lang_[lang].sort_values(by = 'topic')
    col4, col5 = st.columns(2)
    col4.plotly_chart(display_scatter_polar(regions_per_lang_, 'topic', 'value', 'Geography.Regions comparison'))
    col5.plotly_chart(display_scatter_polar(regions_top100, 'topic', 'score', 'Geography.Regions comparison - Top 100 articles'))
        

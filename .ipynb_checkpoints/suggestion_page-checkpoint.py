import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
import plotly.express as px
import numpy as np
import pageviewapi
import time
from xgboost.sklearn import XGBClassifier
import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from collections.abc import Mapping
import pageviewapi
import datetime
from PIL import Image
import xgboost as xgb

@st.cache
def load_data(file_name):
    df = pd.read_csv(file_name)
    return df
def load_model(model_name):
    model = pd.read_pickle(model_name)
    return model

df = load_data('mean_predicted_quality.csv')
df=df.drop(columns=['Unnamed: 0'])
df_qualities_features_top100 = load_data('df_qualities_features_top100.csv')


def show_suggestion_page():
    st.markdown("<h1 style='text-align: center; color: #307473;'>Suggestions Page</h1>", unsafe_allow_html=True)
    
    st.write("""## Recomendations Searcher""")
    with st.form("my_form"):
        st.write("Choose an IAL to get suggestions of popular nontranslated articles that you can write on")
        #from_lang = st.text_input('Language code', placeholder='-- e.g., en for English')
        ial_ = st.selectbox("Choose an IAL", ('Simple English', 'Esperanto', 'Ido', 'Volapük', 'Interlingua', 'Interlingue', 'Novial'))
        slider_val = st.slider("Number of suggestions", 1, 30, 5)
        #checkbox_val = st.checkbox("Form checkbox")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        #if submitted:
         #   st.write("slider", slider_val, "checkbox", checkbox_val)
            
    if submitted:
        language_to_ial={'Simple English': 'simple', 'Esperanto':'eo', 'Ido':'io', 'Volapük':'vo', 'Interlingua': 'ia', 'Interlingue':'ie', 'Novial':'nov'}
        ial = language_to_ial[ial_]
        if ial == 'nov':
            st.write("Unfortunatelly, due to a low rate of article creation we were not able to develop a system that can suggest articles for Novial. However, we recommend looking at the [List of articles every Wikipedia should have](https://meta.wikimedia.org/wiki/List_of_articles_every_Wikipedia_should_have) for inspiration.")
        else:
            my_bar = st.progress(0)
            model_ial = XGBClassifier()
            model_ial_2 = xgb.Booster()
            model_ial.load_model('model_'+ial+".json")
            model_ial_2.load_model('model_'+ial+".json")
            #model_ial = .load_model("model.json")
            #model_ial = load_model('model_'+ial+'.pkl')
            columns_d = model_ial_2.feature_names
            input_data = get_input_data(ial, my_bar)
            for col in columns_d:
                if col not in list(input_data.columns):
                    input_data[col]=np.nan
            print("Columns", input_data.columns)
            my_bar.progress(90)
            dt = input_data[['Qid', 'title']]
            input_data = input_data[columns_d]
            print("Columns", input_data.columns)
            list_of_langs = ['en', 'es', 'ca', 'simple', 'eo', 'io', 'ia', 'vo', 'ie', 'nov']
            for l in list_of_langs:
                if l == 'nov' or l == ial:
                    continue
                input_data['is_top_'+l] = input_data['is_top_'+l].fillna(False)
            input_data = input_data.fillna(-1.0)
            #i_data = xgb.DMatrix(input_data)
            y_pred = model_ial.predict(input_data)
            l = len(dt)
            results = [row for i, row in dt.iterrows() if y_pred[i]==1]
            probs = model_ial.predict_proba(input_data)
            dict_results = {i:list(probs[i])[1] for i in range(len(input_data)) if y_pred[i]==1}
            print(dict_results)
            list_results = sorted(dict_results)
            print(list_results)
            show_suggestions(slider_val, list_results, dt, my_bar)
            if ial_== 'Volapük':
                ial_ = 'Volapuk'
            image = Image.open('Confusion Matrix - '+ial_+'.png')
            st.write("""## Characteristics of the model that classifies articles based on popularity:""")
            #col1, col2, col3 = st.columns(3)
            st.image(image, caption='Confusion Matrix of the model used for suggesting articles for '+ial_, width=800)
            
    #st.write("Outside the form")

def views_next_days(title, time, wiki, days):
    views = []
    print(title)
    date_init = datetime.datetime.strptime(time, '%Y%m%d').date() + datetime.timedelta(days=1)
    date_final = datetime.datetime.strptime(time, '%Y%m%d').date() + datetime.timedelta(days=1+days)
    try:
        views = [d['views'] for d in dict(pageviewapi.per_article(wiki+'.wikipedia', title, date_init.strftime("%Y%m%d"), date_final.strftime("%Y%m%d"), access='all-access', agent='all-agents', granularity='daily'))['items']]
        if views != []:
            return views
        else:
            print("P"+title)
            return np.NaN
    except:
        return np.NaN        

def get_article_creation_date(lang, title):
    url = f"https://{lang}.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={title}&rvprop=timestamp&rvdir=newer"

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        page_id = next(iter(data['query']['pages']))
        revisions = dict(data['query']['pages'][page_id])
        if 'revisions' in revisions.keys():
            revisions = revisions['revisions']
            creation_timestamp = revisions[0]['timestamp']
            return creation_timestamp.split('T')[0]
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

    return None

def compute_features_views(list_views):
    if list_views==[-1]:
        return np.NaN, np.NaN, np.NaN, np.NaN
    return np.mean(list_views), np.median(list_views), np.sum(list_views), np.argmax(list_views)

def get_wikipedia_qid(title, language):
    # Set the API endpoint URL
    api_url = "https://{0}.wikipedia.org/w/api.php".format(language)

    # Set the parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageprops",
        "titles": title
    }

    # Send the API request
    response = requests.get(api_url, params=params)
    data = response.json()

    # Extract the QID from the API response
    pages = data["query"]["pages"]
    try:
        qid = next(iter(pages.values()))["pageprops"]["wikibase_item"]
    except:
        return None
    return qid
    
def exists(article_title, lang1, lang2):
    url = f"https://{lang1}.wikipedia.org/w/api.php?action=query&format=json&prop=langlinks|pageprops&titles={article_title}&lllang={lang2}"
    response = requests.get(url)
  
    if response.status_code == 200:
        data = response.json()
        pages = data['query']['pages']
        #print(pages)
        for page_id in pages:
            lang_links = pages[page_id].get('langlinks')
            page_props = pages[page_id].get('pageprops')
            qid = page_props.get('wikibase_item') if page_props else None

        if lang_links and qid:
            lang2_title = next((link['*'] for link in lang_links if link['lang'] == lang2), None)
            if lang2_title:
                return True
        return False  
    else:
        return False
    
def get_topics(title, lang):
    url = f"https://wikipedia-topic.wmcloud.org/api/v1/topic?threshold=0.5&lang={lang}&title={title}"
    response = requests.get(url)

    try:
        response.raise_for_status()
        data = response.json()
        topics = data['results']
        dict_ = {'topic_Culture': 0, 'topic_STEM': 0, 'topic_History_and_Society': 0, 'topic_Geography': 0}
        topics = set(x['topic'] for x in topics)
        for topic in topics:
            topic = topic.split('.')[0]
            dict_['topic_'+topic] = 1
        return dict_
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print("An error occurred:", e)

    return {'topic_Culture': 0, 'topic_STEM': 0, 'topic_History_and_Society': 0, 'topic_Geography': 0}


def get_titles_in_other_lang(article_titles, lang1, lang2):
    lang2_titles_with_qid = []

    for title in article_titles:
        url = f"https://{lang1}.wikipedia.org/w/api.php?action=query&format=json&prop=langlinks|pageprops&titles={title}&lllang={lang2}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            pages = data['query']['pages']
            for page_id in pages:
                lang_links = pages[page_id].get('langlinks')
                page_props = pages[page_id].get('pageprops')
                qid = page_props.get('wikibase_item') if page_props else None

                if lang_links and qid:
                    lang2_title = next((link['*'] for link in lang_links if link['lang'] == lang2), None)
                    if lang2_title:
                        lang2_titles_with_qid.append({'title': lang2_title, 'qid': qid})
        else:
            break

    return lang2_titles_with_qid

def get_top_articles(lang1, lang2):
    #url = f"https://{lang1}.wikipedia.org/w/api.php?action=query&format=json&prop=views&list=mostviewed&formatversion=2&pvlimit=100"
    #response = requests.get(url)
    # Get today's date
    current_date = datetime.datetime.now().date()

    # Calculate the date of a week ago
    week_ago_date = current_date - datetime.timedelta(weeks=1)

    # Get the year, month, and day from the week ago date
    year = week_ago_date.year
    month = week_ago_date.strftime("%m")
    day = week_ago_date.strftime("%d")
    month = str(month).zfill(2)
    day = str(day).zfill(2)
    print(day, month)
    response = pageviewapi.top(lang1+'.wikipedia', year, month, day, access='all-access')
    count = 0  # Counter to track the number of articles retrieved
    top_articles = []  # List to store the top articles

    #if response.status_code == 200:
    #data = response.json()
    data = dict(response)
    #articles = data['query']['mostviewed']
    print(data)
    articles = list(data['items'][0]['articles'])
    print("data", data)
    for index, article in enumerate(articles, start=1):
        article_title = article['article']
        if str(get_article_creation_date(lang1, article_title)) >'2015':
            if exists(article_title, lang1, lang2)==False:
                top_articles.append(article_title)
                count += 1

                if count == 200:
                    break
    print(len(top_articles))
    return top_articles
    '''
    # Check if there are more results and make additional requests
    while count < 100 and 'continue' in data:
        print("patata")
        continue_params = data['continue']
        continue_url = url + '&'.join(f"&{param}={value}" for param, value in continue_params.items())
        response = requests.get(continue_url)
        if response.status_code == 200:
            data = response.json()
            articles = data['query']['mostviewed']
            for index, article in enumerate(articles, start=index):
                article_title = article['title']
                if str(get_article_creation_date(lang1, article_title)) >'2015':
                    if exists(article_title, lang1, lang2)==False:
                        top_articles.append(article_title)
                        count += 1
                        if count == 50:
                            break
            else:
                break'''
   
    
def get_input_data(lang, my_bar):
    list_of_langs = ['en', 'es', 'ca', 'simple', 'eo', 'io', 'ia', 'vo', 'ie', 'nov']
    jacsim = {'en': 'es', 'es':'en', 'ca':'es', 'simple':'ie', 'eo':'io', 'io':'ia', 'ia':'io', 'vo':'ie', 'ie':'vo'}
    threshold = {'en': 1200, 'es':200, 'ca':40, 'simple':40, 'eo':10, 'io':10, 'ia':10, 'vo':10, 'ie':10}
    input_data = pd.DataFrame(columns=['Qid'])
    print(input_data.head())
    #get current month
    #get top100 articles in jacsim[lang]
    my_bar.progress(0)
    top100 = get_top_articles(jacsim[lang], lang)
    print(top100)
    percentage = 1
    for lang2 in list_of_langs:
        time.sleep(3)
        my_bar.progress(percentage)
        if lang2 == lang or lang2 == 'nov':
            continue
        top_ = get_titles_in_other_lang(top100, jacsim[lang], lang2)
        df2 = pd.DataFrame()
        if lang2 != jacsim[lang]:
            for article in top_:
                if article['qid']==None:
                    continue
                #get views first month
                timestamp = ''.join(get_article_creation_date(lang2, article['title']).split('-'))
                if timestamp:
                    views = views_next_days(article['title'],  timestamp, lang2, 30)
                    print(article['title'],  timestamp, lang2, views)
                    mean_, median_, sum_, peak = compute_features_views(views)
                    b = sum_>=threshold[lang2]
                    #df2 = df2.append(, ignore_index = True)
                    row = {'Qid' : article['qid'], 'views_mean_'+lang2 : mean_, 'views_median_'+lang2 : median_, 'views_sum_'+lang2:sum_, 'views_peak_'+lang2:peak, 'is_top_'+lang2:b}
                    df1 = pd.DataFrame([row])
                    df2 = pd.concat([df2, df1], axis=0)
        else:
            for article in top100:
                qid = get_wikipedia_qid(article, lang2)
                if qid==None:
                    continue
              #get views first month
                timestamp = ''.join(get_article_creation_date(lang2, article).split('-'))
                if len(timestamp)>4:
                    views = views_next_days(article,  timestamp, lang2, 30)
                    mean_, median_, sum_, peak = compute_features_views(views)
                    b = sum_>=threshold[lang2]
                    topics = get_topics(article, lang2)
                    print(topics)
                    row = {'Qid' : qid, 'title': article, 'views_mean_'+lang2 : mean_, 'views_median_'+lang2 : median_, 'views_sum_'+lang2:sum_, 'views_peak_'+lang2:peak, 'is_top_'+lang2:b}
                    row = {**row, **topics}
                    df1 = pd.DataFrame([row])
                    #df2 = df2.append(row, ignore_index = True)
                    df2 = pd.concat([df2, df1], axis=0)

        print(input_data.head())
        print(df2.head())
        if 'Qid' in list(df2.columns):
            input_data = pd.merge(input_data, df2, on='Qid', how='outer')
        percentage+=10
        print(input_data.head())
    return input_data
      
def show_suggestions(slider_val, list_top, dt, my_bar):
    my_bar.progress(100)
    st.markdown("<h1 style='text-align: center; color: #307473;'>Results:</h1>", unsafe_allow_html=True)
    #col0, col1, col2 = st.columns(3)
    size = len(list_top)
    if slider_val<size:
        size = slider_val
    for i in range(size):
        qid = dt.iloc[list_top[i]]['Qid']
        title = dt.iloc[list_top[i]]['title']
        st.markdown(f"<h3 style='text-align: center;'>{title} - <a href='https://www.wikidata.org/wiki/{qid}'>{qid}</a></h3>", unsafe_allow_html=True)
        #col1.write(f"## {title} - [{qid}](https://www.wikidata.org/wiki/{qid})")
    #col1.write("## [Dog](https://en.wikipedia.org/wiki/Dog) - 8k views")
    #col1.write("## [United States](https://en.wikipedia.org/wiki/United_States) - 7k views")
    #col1.write("## [Lady Gaga](https://en.wikipedia.org/wiki/Lady_Gaga) - 6k views")
    #col1.write("## [Catalonia](https://en.wikipedia.org/wiki/Catalonia) - 6k views")
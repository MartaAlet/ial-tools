import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
import plotly.express as px

@st.cache

def footer():
    footer="""<style>
    a:link , a:visited{
    color: blue;
    background-color: transparent;
    text-decoration: underline;
    }

    a:hover,  a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
    }

    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    }
    </style>
    <div class="footer">
    <p>Developed by <a style='display: block; text-align: center;' href="https://www.mediawiki.org/w/index.php?title=User:MartaAlet" target="_blank">Marta Alet Puig</a></p>
    </div>
    """
    st.markdown(footer,unsafe_allow_html=True)

def show_main_page():
    st.markdown("<h1 style='text-align: center; color: #307473;'>Main Page</h1>", unsafe_allow_html=True)
    st.write("This website provides editors with an analysis and visualization of some characteristics of the International Auxiliary Language (IAL) community of Wikipedia. The IALs that have been analyzed are [Simple English](https://simple.wikipedia.org/wiki/Main_Page), [Esperanto](https://eo.wikipedia.org/wiki/Vikipedio:%C4%88efpa%C4%9Do), [Ido](https://io.wikipedia.org/wiki/Frontispico), [Interlingua](https://ia.wikipedia.org/wiki/Pagina_principal), [Volapük](https://vo.wikipedia.org/wiki/Cifapad), and [Interlingue](https://ie.wikipedia.org/wiki/Principal_p%C3%A1gine). We also considered the [English](https://en.wikipedia.org/wiki/Main_Page), [Spanish](https://es.wikipedia.org/wiki/Wikipedia:Portada), and [Catalan](https://ca.wikipedia.org/wiki/Viquip%C3%A8dia:Portal) for comparison purposes.")
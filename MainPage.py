import streamlit as st
#import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
#from sklearn.cluster import AgglomerativeClustering
#import plotly.express as px
#from PIL import Image

#@st.cache(suppress_st_warning=True)


def show_main_page():
    st.markdown("<h1 style='text-align: center; color: #307473;'>Main Page</h1>", unsafe_allow_html=True)
    st.write("This website provides editors with an analysis and visualization of some characteristics of the International Auxiliary Language (IAL) community of Wikipedia. The IALs that have been analyzed are [Simple English](https://simple.wikipedia.org/wiki/Main_Page), [Esperanto](https://eo.wikipedia.org/wiki/Vikipedio:%C4%88efpa%C4%9Do), [Ido](https://io.wikipedia.org/wiki/Frontispico), [Interlingua](https://ia.wikipedia.org/wiki/Pagina_principal), [Volapük](https://vo.wikipedia.org/wiki/Cifapad), and [Interlingue](https://ie.wikipedia.org/wiki/Principal_p%C3%A1gine). We also considered the [English](https://en.wikipedia.org/wiki/Main_Page), [Spanish](https://es.wikipedia.org/wiki/Wikipedia:Portada), and [Catalan](https://ca.wikipedia.org/wiki/Viquip%C3%A8dia:Portal) for comparison purposes.")
    
    st.markdown(
        """
        <style>
        .footer {
          position: fixed;
          left: 0;
          bottom: 0;
          width: 100%;
          background-color: #54ccca;
          color: white;
          text-align: center;
        }
        </style>

        <div class="footer">
          <p style='text-align: center;'>Developed by <a href="https://www.mediawiki.org/w/index.php?title=User:MartaAlet">Marta Alet Puig</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )







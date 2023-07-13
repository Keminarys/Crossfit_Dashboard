import pandas as pd
import numpy as np
import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

### Variables fixes 
df = pd.read_csv('./database.csv')
list_Type = ['EMOM','AMRAP','RM1']
list_Exercice = [['CHELSEA'],['CINDY'],['POWER CLEAN']]
list_Name = list(df['Nom'].unique())
list_Name.append("Nouveau profil")
list_Unité = ["kg", "min", "tours"]

### Configuration de la page

st.set_page_config(layout="wide")

st.title('Crossfit83 Le Beausset')
st.write('Application permettant de tracer les différents WOD de référence et ainsi voir l\'évolution de chaque athlète.')
st.divider()
with st.sidebar.expander("Ajouter une ligne de benchmark."):
  name_ = st.selectbox('Choisir votre nom dans la liste déroulante ou Nouveau profil pour débuter.', list_Name)
  if name_ == "Nouveau profil" : 
    st.divider()
    new_ = st.text_input("Merci de renseigner votre prénom uniquement.")
  type_ = st.selectbox('Choisir dans la liste déroulante le type de WOD', list_Type)
  if type_ == 'EMOM' : 
    ex_ = st.selectbox('Choisir dans la liste déroulante l\'exercice', list_Exercice[0])
  elif type_ == 'AMRAP' : 
    ex_ = st.selectbox('Choisir dans la liste déroulante l\'exercice', list_Exercice[1])
  elif type_ == 'RM1' : 
    ex_ = st.selectbox('Choisir dans la liste déroulante l\'exercice', list_Exercice[2])
  value_ = st.number_input('Merci de renseigner la valeur.')
  unite_ = st.radio('Merci de sélectionner une unité.', list_Unité)
  date_ = st.date_input('Merci de sélectionner la date du WOD', datetime.date.today())


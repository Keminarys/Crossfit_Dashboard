import pandas as pd
import numpy as np
import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

### Fonctions

def form_callback(name_, type_, ex_, date_, value_, unite_, dif_):    
    with open('database.csv', 'a+') as f:    #Append & read mode
        f.write(f"{name_}, {type_}, {ex_}, {date_}, {value_}, {unite_}, {dif_}\n")
        f.close()

### Variables fixes 

list_Unité = ["kg", "min", "tours"]
list_Dif = ['RX','Scaled']

### Configuration de la page

st.set_page_config(layout="wide")

st.title('Crossfit83 Le Beausset')
st.write('Application permettant de tracer les différents WOD de référence et ainsi voir l\'évolution de chaque athlète.')
st.divider()


with st.form(key="Ajouter un nouveau benchmark",clear_on_submit=True):
    
    st.write("Ajouter un nouveau benchmark")
    st.write('Pour des soucis de RGPD, merci de renseigner seulement votre les 3 premières lettre de votre prénom et la première lettre de votre nom de famille')
    name_ = st.text_input('Nom', key='Nom')
    type_ = st.text_input('Type', key='Type')
    ex_ = st.text_input('Exercice', key='Exercice')
    date_ = st.date_input('Merci de sélectionner la date du WOD', datetime.date.today())
    value_ = st.number_input('Merci de renseigner la valeur.')
    unite_ = st.radio('Merci de sélectionner une unité.', list_Unité)
    dif_ = st.radio('Merci de sélectionner une difficulté.', list_Dif)
    submitted = st.form_submit_button("Ajouter à mon profil")
    if submitted:
        st.write("Benchmark ajouté à votre profil !")
        form_callback(name_, type_, ex_, date_, value_, unite_, dif_)

with st.container():
    st.info("Si vous souhaitez voir votre profil, ça se passe par ici ! :point_down:")
    st.dataframe(pd.read_csv('database.csv'),height=300)
    # list_Type = list(df['Type'].unique())
    # list_Exercice = list(df['Exercice'].unique())
    # list_Name = list(df['Nom'].unique())
    # profile_ = st.selectbox('Merci de selectionner votre nom dans la liste déroulante', list_Name)
    # if profile_ in list_Name :
    #     st.dataframe(df.loc[df['Nom'] == profile_],height=300)


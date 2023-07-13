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

### Variables fixes 
df = pd.read_csv('./database.csv')
list_Type = ['EMOM','AMRAP','RM1']
list_Exercice = [['CHELSEA'],['CINDY'],['POWER CLEAN']]
list_Name = list(df['Nom'].unique())
list_Name.append("Nouveau profil")
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
        st.write("Nom",name_,"Type",type_,"Exercice",ex_,"Date",date_,"Valeur",value_,"Unité",unite_,"Difficulté",dif_)
        form_callback(name_, type_, ex_, date_, value_, unite_, dif_)
      
st.info(" #### Show contents of the CSV file :point_down:")
st.dataframe(pd.read_csv("database.csv"),height=300)

# with st.sidebar.expander("Ajouter une ligne de benchmark."):
#   name_ = st.selectbox('Choisir votre nom dans la liste déroulante ou Nouveau profil pour débuter.', list_Name)
#   if name_ == "Nouveau profil" : 
#     st.divider()
#     new_ = st.text_input("Merci de renseigner votre prénom uniquement.")
#   type_ = st.selectbox('Choisir dans la liste déroulante le type de WOD', list_Type)
#   if type_ == 'EMOM' : 
#     ex_ = st.selectbox('Choisir dans la liste déroulante l\'exercice', list_Exercice[0])
#   elif type_ == 'AMRAP' : 
#     ex_ = st.selectbox('Choisir dans la liste déroulante l\'exercice', list_Exercice[1])
#   elif type_ == 'RM1' : 
#     ex_ = st.selectbox('Choisir dans la liste déroulante l\'exercice', list_Exercice[2])
#   value_ = st.number_input('Merci de renseigner la valeur.')
#   unite_ = st.radio('Merci de sélectionner une unité.', list_Unité)
#   date_ = st.date_input('Merci de sélectionner la date du WOD', datetime.date.today())

# if name_ != "Nouveau profil" :
#   row_to_add = [name_, type_, ex_, date_, value_, unite_]
#   df.loc[len(df)] = row_to_add
# else : 
#   row_to_add = [new_, type_, ex_, date_, value_, unite_]
#   df.loc[len(df)] = row_to_add


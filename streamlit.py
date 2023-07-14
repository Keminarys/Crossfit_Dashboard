import pandas as pd
import numpy as np
import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from google.oauth2 import service_account
from gspread_pandas import Spread, Client

### Fonctions

def send_to_database(row):
    df = pd.DataFrame(worksheet.get_all_records())
    to_add = pd.DataFrame(row)
    df_upt = pd.concat([df, to_add], ignore_index=True)
    spread.df_to_sheet(df = df_upt ,sheet = "Sheet1" ,index = False)
    return st.success("Benchmark ajouté à votre profil !")

    
### Variables fixes 

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "Database_CF83"
spread = Spread(spreadsheetname,client = client)
sh = client.open(spreadsheetname)
worksheet = sh.worksheet("Sheet1")
df = pd.DataFrame(worksheet.get_all_records())
list_Exercice = list(df['Exercice'].unique())
list_Name = list(df['Nom'].unique())
list_Unité = ["kg", "min", "tours"]
list_Dif = ['RX','Scaled']

### Configuration de la page

st.set_page_config(layout="wide")

st.title('Crossfit83 Le Beausset')
st.write('### Application permettant de tracer les différents WOD de référence et ainsi voir l\'évolution de chaque athlète.')
st.divider()


with st.form(key="Ajouter un nouveau benchmark",clear_on_submit=True):
    
    st.write("### Ajouter un nouveau benchmark")
    st.write('Pour des soucis de RGPD, merci de renseigner seulement votre les 3 premières lettre de votre prénom et la première lettre de votre nom de famille')
    name_ = st.text_input('Nom', key='Nom')
    st.write('Merci d\'écrire en MAJUSCULE')
    type_ = st.text_input('Type', key='Type')
    st.write('Merci d\'écrire en MAJUSCULE')
    ex_ = st.text_input('Exercice', key='Exercice')
    date_ = st.date_input('Merci de sélectionner la date du WOD', datetime.date.today())
    value_ = st.number_input('Merci de renseigner la valeur.')
    unite_ = st.radio('Merci de sélectionner une unité.', list_Unité)
    dif_ = st.radio('Merci de sélectionner une difficulté.', list_Dif)
    submitted = st.form_submit_button("Ajouter à mon profil")
    if submitted:
        new_row = {'Nom' : [name_], 'Type' : [type_], 
                   'Exercice' : [ex_], 'Date' : [date_], 
                   'Valeur' : [value_], 'Unité' : [unite_], 'Difficulté' : [dif_]}
        send_to_database(new_row)
        
with st.container():
    choice = st.checkbox(':point_left: Souhaitez-vous voir votre profil ?')
    if choice :
        profile_ = st.selectbox('Merci de selectionner votre nom dans la liste déroulante', list_Name)
        st.dataframe(df.loc[df['Nom'] == profile_],height=300)

with st.container() :
    choice_2 = st.checkbox(":point_left: Souhaitez-vous visualiser votre progression à l'aide de graphique ?")
    if choice_2 :
        graph_ex = st.selectbox('Choisissez un type d\'exercice.', list_Exercice)
        #fig = px.line(df.loc[df['Nom'] == profile_], x="lifeExp", y="gdpPercap", color="country", text="year")
        


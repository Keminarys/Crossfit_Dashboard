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

list_Unité = ["kg", "min", "tours"]
list_Dif = ['RX','Scaled']

### Configuration de la page

st.set_page_config(layout="wide")

st.title('Crossfit83 Le Beausset')
st.write('### Application permettant de tracer les différents WOD de référence et ainsi voir l\'évolution de chaque athlète.')
st.write(spread.url)
st.divider()


with st.form(key="Ajouter un nouveau benchmark",clear_on_submit=True):
    
    st.write("### Ajouter un nouveau benchmark")
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
        new_row = {'Nom' : [name_], 'Type' : [type_], 
                   'Exercice' : [ex_], 'Date' : [date_], 
                   'Valeur' : [value_], 'Unité' : [unite_], 'Difficulté' : [dif_]}
        send_to_database(new_row)
        
with st.container():
    st.info("Si vous souhaitez voir votre profil, ça se passe par ici ! :point_down:")
    df = pd.DataFrame(worksheet.get_all_records())
    list_Type = list(df['Type'].unique())
    list_Exercice = list(df['Exercice'].unique())
    list_Name = list(df['Nom'].unique())
    profile_ = st.selectbox('Merci de selectionner votre nom dans la liste déroulante', list_Name)
    if profile_ in list_Name :
        st.dataframe(df.loc[df['Nom'] == profile_],height=300)


import pandas as pd
import numpy as np
import datetime
import re
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from google.oauth2 import service_account
from gspread_pandas import Spread, Client

### Fonctions

def load_client(): 
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
    client = Client(scope=scope,creds=credentials)
    return client
    

def load_spread():
    spread = Spread("Database_CF83",client = client)
    return spread


def load_worksheet() :
    sh = client.open("Database_CF83")
    worksheet = sh.worksheet("Sheet1")
    return worksheet

def send_to_database(row):
    df = pd.DataFrame(worksheet.get_all_records())
    to_add = pd.DataFrame(row)
    df_upt = pd.concat([df, to_add], ignore_index=True)
    spread.df_to_sheet(df = df_upt ,sheet = "Sheet1" ,index = False)
    return st.success("Benchmark ajouté à votre profil !")


def perso_df(df, profile_, chex = None, rmwod = [None, 'WOD', 'RM']):
    perso = df.loc[df['Nom'] == profile_]
    if (chex == None) and (rmwod == None): 
        pass
    elif rmwod == 'WOD': 
        perso = perso.loc[perso['WOD'].str.upper() == chex]
    elif rmwod == 'RM': 
        perso = perso.loc[perso['RM'].str.upper() == chex]
    return perso

def clear_ws(string):
    return str(np.char.replace(string, ' ', ''))
    
### Variables fixes 

client = load_client()
spread=load_spread()
worksheet = load_worksheet()
df = pd.DataFrame(worksheet.get_all_records())
df['WOD'] = df['WOD'].apply(lambda x : clear_ws(x))
df['RM'] = df['RM'].apply(lambda x : clear_ws(x))
list_WOD = list(df['WOD'].str.upper().unique())
list_WOD = [v for v in list_WOD if v != ""]
list_RM = list(df['RM'].str.upper().unique())
list_RM = [v for v in list_RM if v != ""]
list_Name = list(df['Nom'].unique())
list_Unité = ["kg", "min", "tours"]
list_Dif = ['RX','Scaled']

### Configuration de la page

st.set_page_config(layout="centered",
                  initial_sidebar_state="collapsed")

st.title('Crossfit83 Le Beausset')
st.write('### Application permettant de tracer les performances dans les différents WOD de référence et ainsi voir l\'évolution de chaque athlète.')
profile_ = st.selectbox('Merci de selectionner votre nom dans la liste déroulante', list_Name)
st.write('Si vous ne vous trouvez pas, Merci d\'ajouter votre premier WOD ou RM pour continuer !')
st.divider()

with st.sidebar :
    
    st.selectbox('Tous les WOD dans la base de données', list_WOD)
    st.divider()
    st.selectbox('Tous les RM dans la base de données', list_RM)
    
with st.form(key="Ajouter un nouveau RM ou WOD",clear_on_submit=True):
    
    st.write("### Ajouter un nouveau RM ou WOD")
    st.write('Pour des soucis de RGPD, merci de renseigner seulement les 3 premières lettre de votre prénom et la première lettre de votre nom de famille (ex : DylL)')
    st.write('Si c\'est votre premier WOD ou RM remplacez le nom ci-dessous :point_down: par le votre')
    name_ = st.text_input('Nom', key='Nom', value=profile_)
    st.divider()
    type_ = st.text_input('RM (en majuscule)', key='Type')
    st.divider()
    ex_ = st.text_input('WOD (en majuscule)', key='Exercice')
    st.divider()
    date_ = st.date_input('Merci de sélectionner la date du WOD', datetime.date.today())
    st.divider()
    value_ = st.number_input('Merci de renseigner la valeur.')
    st.divider()
    unite_ = st.radio('Merci de sélectionner une unité.', list_Unité)
    st.divider()
    rep_ = st.number_input('Merci de renseigner le nombre de répétitions.')
    rep_ = int(rep_)
    st.divider()
    dif_ = st.radio('Merci de sélectionner une difficulté.', list_Dif)
    st.divider()
    submitted = st.form_submit_button("Ajouter à mon profil")
    if submitted:
        new_row = {'Nom' : [name_], 'RM' : [type_], 
                   'WOD' : [ex_], 'Date' : [date_], 
                   'Valeur' : [value_], 'Unité' : [unite_], 
                   'Rep': [rep_],'Difficulté' : [dif_]}
        send_to_database(new_row)
        st.experimental_rerun()

with st.form(key=":point_left: Merci de bien vérifier que les informations renseigner à l\'instant soient justes",clear_on_submit=True):
    st.write("### :point_down: Merci de bien vérifier que les informations renseigner à l\'instant soient justes")
    st.dataframe(df.tail(1))
    last_row = (int(len(df)) + 1)
    st.write('Si les informations sont erronées, cliquez sur le bouton ci dessous.')
    deletion_ = st.form_submit_button("Supprimer la dernière ligne de mon profil")
    if deletion_:
        worksheet.delete_row(last_row)

        
with st.container():
    choice = st.checkbox(':point_left: Souhaitez-vous voir votre profil ?')
    if choice :
        perso = perso_df(df, profile_, chex = None)
        st.dataframe(perso)

with st.container() :
    choice_2 = st.checkbox(":point_left: Souhaitez-vous visualiser votre progression à l'aide de graphique ?")
    if choice_2 :
        rm_wod = st.radio('Souhaitez vous voir votre progression sur un WOD ou un RM', ['WOD','RM'])
        if rm_wod == 'WOD' : 
            graph_ex = st.selectbox('Choisissez un WOD.', list_WOD)
            perso = perso_df(df, profile_, chex = graph_ex, rmwod = rm_wod)
            if len(perso) > 0:
                fig = px.line(x=perso["Date"], y=perso["Valeur"], color=perso["Difficulté"], markers=True)
                fig.update_layout(
                title=f'Progression sur l\'exercice {graph_ex}',
                xaxis_title="Date",
                yaxis_title=str(perso.Unité.unique()[0]),
                autosize=False,
                width=500,
                height=300)
                st.plotly_chart(fig,use_container_width=True)
            else : 
                st.write(':no_entry_sign: Vous n\'avez pas encore de référence sur ce WOD :no_entry_sign:')
        if rm_wod == 'RM' : 
            graph_ex = st.selectbox('Choisissez une RM.', list_RM)
            perso = perso_df(df, profile_, chex = graph_ex, rmwod = rm_wod)
            rep_ex = st.selectbox('Choisissez un nombre de répétition.', perso.Rep.unique())
            perso = perso.loc[perso['Rep'] == rep_ex]
            if len(perso) > 0:
                fig = px.line(x=perso["Date"], y=perso["Valeur"], color=perso["Difficulté"], markers=True)
                fig.update_layout(
                title=f'Progression sur l\'exercice {graph_ex} pour {rep_ex} répétitions',
                xaxis_title="Date",
                yaxis_title=str(perso.Unité.unique()[0]),
                autosize=False,
                width=500,
                height=300)
                st.plotly_chart(fig,use_container_width=True)
            else : 
                st.write(':no_entry_sign: Vous n\'avez pas encore de référence sur cet RM :no_entry_sign:')
        
        


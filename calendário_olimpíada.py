# rodar no terminal: 
# cd C:\Users\bserpellone\Desktop\Python\github
# streamlit run calendário_olimpíada.py

import streamlit as st
import pandas as pd

# Carregar o DataFrame
arquivo = r"C:\Users\bserpellone\Desktop\Python\github\horario olimpiada.csv"
df_horarios = pd.read_csv(arquivo, delimiter=';')

# Criar uma coluna 'Data_Para_Selecao' combinando Data e Dia
df_horarios['Data_Para_Selecao'] = df_horarios['Data'].str[:5] + ' - ' + df_horarios['Dia']

# Criar lista de modalidades e datas
def extrair_modalidade_resumida(modalidade):
    return modalidade.split(':')[0].strip()

df_horarios['modalidade_resumida'] = df_horarios['Modalidade'].apply(extrair_modalidade_resumida)
modalidades_resumidas = df_horarios['modalidade_resumida'].unique()
modalidades_display = ["Atletismo" if modalidade.startswith("Atletismo") else modalidade for modalidade in modalidades_resumidas]
modalidades_display = sorted(set(modalidades_display))  # Remover duplicatas e ordenar

datas_display = sorted(df_horarios['Data_Para_Selecao'].unique())

# Seleção de Modalidade e Data
modalidade_selecionada = st.selectbox("Escolha a Modalidade", ["Todos"] + modalidades_display)
data_selecionada = st.selectbox("Escolha a Data", ["Todas"] + datas_display)

# Aplicando os filtros
if modalidade_selecionada != "Todos" and data_selecionada != "Todas":
    if modalidade_selecionada == "Atletismo":
        filtro = df_horarios[df_horarios['modalidade_resumida'].str.startswith("Atletismo") & (df_horarios['Data_Para_Selecao'] == data_selecionada)]
    else:
        filtro = df_horarios[(df_horarios['modalidade_resumida'] == modalidade_selecionada) & (df_horarios['Data_Para_Selecao'] == data_selecionada)]
elif modalidade_selecionada != "Todos":
    if modalidade_selecionada == "Atletismo":
        filtro = df_horarios[df_horarios['modalidade_resumida'].str.startswith("Atletismo")]
    else:
        filtro = df_horarios[df_horarios['modalidade_resumida'] == modalidade_selecionada]
elif data_selecionada != "Todas":
    filtro = df_horarios[df_horarios['Data_Para_Selecao'] == data_selecionada]
else:
    filtro = df_horarios

# Exibindo o DataFrame filtrado ou completo
st.write("**Dados**")

# Excluindo a coluna 'modalidade_resumida' e 'Data_Para_Selecao' do DataFrame exibido
df_exibicao = filtro.drop(columns=['modalidade_resumida', 'Data_Para_Selecao'])

# Exibindo o DataFrame sem o índice
st.dataframe(df_exibicao.style.hide(axis="index"))

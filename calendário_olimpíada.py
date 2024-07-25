# rodar no terminal: 
# cd C:\Users\bserpellone\Desktop\Python\github
# streamlit run calendário_olimpíada.py

import streamlit as st
import pandas as pd
from datetime import datetime

# Adicionar cabeçalho com link para o LinkedIn e alinhar à esquerda
st.markdown(
    """
    <style>
    .footer {
        text-align: left;
        font-size: 12px;
        margin: 20px 0;
    }
    </style>
    <div class="footer">
        Feito por <a href='https://www.linkedin.com/in/brunoserp/' target='_blank'>Bruno Serpellone</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Adicionar estilo CSS para ajustar a largura das colunas e alinhar o cabeçalho à esquerda
st.markdown(
    """
    <style>
    .dataframe {
        width: 100%;
    }
    .dataframe th, .dataframe td {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        text-align: left;
    }
    .dataframe th {
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar o DataFrame
arquivo = r"C:\Users\bserpellone\Desktop\Python\github\horario olimpiada.csv"
df_horarios = pd.read_csv(arquivo, delimiter=';')

# Converter a coluna 'Data' para formato datetime
df_horarios['Data'] = pd.to_datetime(df_horarios['Data'], format='%d/%m/%Y')

# Criar uma coluna 'Data_Para_Selecao' combinando Data e Dia
df_horarios['Data_Para_Selecao'] = df_horarios['Data'].dt.strftime('%d/%m') + ' - ' + df_horarios['Dia']

# Criar lista de modalidades e datas
def extrair_modalidade_resumida(modalidade):
    return modalidade.split(':')[0].strip()

df_horarios['modalidade_resumida'] = df_horarios['Modalidade'].apply(extrair_modalidade_resumida)
modalidades_resumidas = df_horarios['modalidade_resumida'].unique()
modalidades_display = ["Atletismo" if modalidade.startswith("Atletismo") else modalidade for modalidade in modalidades_resumidas]
modalidades_display = sorted(set(modalidades_display))  # Remover duplicatas e ordenar

datas_display = sorted(df_horarios['Data_Para_Selecao'].unique())

# Seleção de Múltiplas Modalidades e Datas
modalidades_selecionadas = st.multiselect("Escolha as Modalidades", modalidades_display)
datas_selecionadas = st.multiselect("Escolha as Datas", datas_display)

# Checkbox para filtrar eventos a partir da data atual
filtrar_data_atual = st.checkbox("Mostrar apenas eventos a partir do dia atual")

# Aplicando os filtros
filtro = df_horarios

if modalidades_selecionadas:
    filtro = filtro[filtro['modalidade_resumida'].isin(modalidades_selecionadas)]

if datas_selecionadas:
    filtro = filtro[filtro['Data_Para_Selecao'].isin(datas_selecionadas)]

if filtrar_data_atual:
    hoje = datetime.today().date()
    filtro = filtro[filtro['Data'].dt.date >= hoje]

# Formatar a coluna 'Data' para exibir apenas dia e mês
filtro['Data'] = filtro['Data'].dt.strftime('%d/%m')

# Excluindo a coluna 'modalidade_resumida' e 'Data_Para_Selecao' do DataFrame exibido
df_exibicao = filtro.drop(columns=['modalidade_resumida', 'Data_Para_Selecao'])

# Converter o DataFrame para HTML sem o índice
df_html = df_exibicao.to_html(index=False, escape=False)

# Exibir o DataFrame como HTML no Streamlit
st.markdown(df_html, unsafe_allow_html=True)

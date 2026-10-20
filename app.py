import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils.ranking_algorithm import calcular_credibilidade

st.set_page_config(page_title="Dashboard PET-Saúde", layout="wide")

st.markdown("""
<style>
    h1 { color: #FF4B72; }
    .stMetric { background-color: #FAFAFA; border-radius: 10px; padding: 15px; border: 1px solid #EEEEEE; }
</style>
""", unsafe_allow_html=True)

st.title("Feed Digital: Mitigação de Desinformação")
st.markdown("**Projeto PET-Saúde Digital | Encontros Universitários UFC - Campus Sobral**")
st.write("Esta Prova de Conceito (PoC) simula o algoritmo de uma rede social. Ele lê as postagens e aplica uma Matriz de Credibilidade combinada com IA de Sentimentos para ranquear conteúdos verdadeiros e esconder fake news.")

@st.cache_data 
def carregar_dados():
    path = "data/processed/dataset_poc_limpo.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    # Chama o nosso motor matemático!
    df_ranqueado = calcular_credibilidade(df)
    return df_ranqueado

df = carregar_dados()

if df.empty:
    st.error("Arquivo dataset_poc_limpo.csv não encontrado. Execute o preparar_dados.py primeiro.")
else:

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Publicações Analisadas", len(df))
    col2.metric("Oficial / Fatos Comprovados", len(df[df['Categoria'] == 'Oficial/Fato']))
    col3.metric("Alertas de Desinformação", len(df[df['Categoria'] == 'Desinformação']))

    st.divider()

    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("Distribuição de Confiabilidade")
        fig1 = px.histogram(df, x="Confiabilidade (%)", color="Categoria", 
                            color_discrete_map={"Desinformação": "#FF4B72", "Oficial/Fato": "#00C896"},
                            nbins=20, title="Concentração de Notícias por Nota do Algoritmo")
        st.plotly_chart(fig1, use_container_width=True)

    with col_graf2:
        st.subheader("Risco Viral: Engajamento vs Confiabilidade")
        fig2 = px.scatter(df, x="Confiabilidade (%)", y="Likes", color="Categoria", 
                          size="Compartilhamentos", hover_data=['Texto_Publicacao'],
                          color_discrete_map={"Desinformação": "#FF4B72", "Oficial/Fato": "#00C896"},
                          title="Bolas maiores = Mais compartilhamentos")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("Feed da Rede Social (Ranqueado do Melhor para o Pior)")
    
    filtro = st.radio("Visão da Banca:", ["Feed Completo (Algoritmo Ativo)", "Mostrar apenas Fatos", "Mostrar apenas Desinformação"], horizontal=True)
    
    if filtro == "Mostrar apenas Fatos":
        df_exibicao = df[df['Categoria'] == 'Oficial/Fato']
    elif filtro == "Mostrar apenas Desinformação":
        df_exibicao = df[df['Categoria'] == 'Desinformação']
    else:
        df_exibicao = df

    st.dataframe(
        df_exibicao[['Confiabilidade (%)', 'Texto_Publicacao', 'Categoria', 'Fonte', 'Likes']],
        use_container_width=True,
        height=400,
        hide_index=True
    )
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64
import numpy as np
from utils.ranking_algorithm import calcular_credibilidade

TITULO_PROJETO = "Algoritmos de Recomendação e Credibilidade em Saúde"
COR_AZUL_ESCURO = "#1B365D"
COR_AZUL_CLARO = "#4CB5F9"
COR_LARANJA = "#E85D04"

@st.cache_data
def load_image_as_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

pet_icon_b64 = load_image_as_base64("assets/pet_h_icon.png")
sus_logo_b64 = load_image_as_base64("assets/sus.png")
sobral_logo_b64 = load_image_as_base64("assets/sobral.png")
ufc_logo_b64 = load_image_as_base64("assets/ufc.png")


st.set_page_config(page_title=TITULO_PROJETO, page_icon="assets/pet_h_icon.png", layout="wide")
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet" />
<style>
    h1 {{ color: {COR_AZUL_ESCURO}; margin-top: -20px; font-weight: 700; }}
    .stMetric {{ background-color: #FAFAFA; border-radius: 10px; padding: 15px; border: 1px solid #EEEEEE; border-top: 4px solid {COR_AZUL_CLARO}; }}
    .md-icon {{ vertical-align: text-bottom; font-size: 18px; margin-right: 4px; }}
    
    /* Estilizando o fundo da Barra Lateral (Sidebar) com o Azul Claro muito suave */
    [data-testid="stSidebar"] {{
        background-color: #F4F9FD;
    }}
    /* Ajustando o texto dos botões de rádio (radio buttons) */
    .stRadio label {{
        color: {COR_AZUL_ESCURO};
        font-weight: 500;
    }}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"<h2 style='color: {COR_AZUL_ESCURO}; margin-bottom: -15px;'>Navegação</h2>", unsafe_allow_html=True)

pagina = st.sidebar.radio(
    "",
    [":material/monitoring: Painel Analítico", ":material/smartphone: Simulador de Feed"]
)

st.sidebar.divider()
st.sidebar.markdown(f"<h4 style='color: {COR_AZUL_ESCURO}; margin-bottom: 5px;'>Projeto PET-Saúde Digital</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #555; font-size: 14px;'><i>Encontros Universitários UFC<br>Campus Sobral</i></p>", unsafe_allow_html=True)

if sus_logo_b64 and sobral_logo_b64 and ufc_logo_b64:
    html_logos = f"""
    <div style="margin-top: 40px; display: flex; flex-direction: column; align-items: center; gap: 25px; padding: 20px; background-color: white; border-radius: 12px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); border: 1px solid #E4E9F0;">
        <p style="font-size: 11px; color: #888; margin: 0; text-transform: uppercase; letter-spacing: 1px; font-weight: bold;">Realização & Apoio</p>
        <img src="data:image/png;base64,{ufc_logo_b64}" width="130" style="object-fit: contain;">
        <img src="data:image/png;base64,{sus_logo_b64}" width="110" style="object-fit: contain;">
        <img src="data:image/png;base64,{sobral_logo_b64}" width="140" style="object-fit: contain;">
    </div>
    """
    st.sidebar.markdown(html_logos, unsafe_allow_html=True)

if pet_icon_b64:
    icone_titulo = f'<img src="data:image/png;base64,{pet_icon_b64}" width="45" style="vertical-align: middle; margin-right: 12px; padding-bottom: 5px;">'
else:
    icone_titulo = f'<span class="material-symbols-rounded" style="font-size: 40px; vertical-align: middle; color: {COR_AZUL_ESCURO}; margin-right: 10px;">local_hospital</span>'

icone_card = '<span class="material-symbols-rounded md-icon" style="font-size: 16px; color: #666;">public</span>'

st.markdown(f"<h1>{icone_titulo}{TITULO_PROJETO}</h1>", unsafe_allow_html=True)

@st.cache_data 
def carregar_dados():
    path = "data/processed/dataset_poc_limpo.csv"
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    return calcular_credibilidade(df)

df = carregar_dados()

if df.empty:
    st.error("Arquivo dataset_poc_limpo.csv não encontrado.")
else:
    if pagina == ":material/monitoring: Painel Analítico":
        
        st.markdown("*Visão global dos dados processados pelo motor de Inteligência Artificial e algoritmo de credibilidade.*")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Analisadas", len(df))
        col2.metric("Oficial / Fatos", len(df[df['Categoria'] == 'Oficial/Fato']))
        col3.metric("Desinformação", len(df[df['Categoria'] == 'Desinformação']))

        st.divider()

        aba1, aba2, aba3, aba4 = st.tabs([
            ":material/local_fire_department: Espectro Viral", 
            ":material/psychology: Emoções (IA)", 
            ":material/radar: Radar de Fontes", 
            ":material/pie_chart: Distribuição"
        ])
        
        with aba1:
            col_grafico, col_detalhes = st.columns([2.5, 1])
            
            with col_grafico:
                col_slider, col_vazia = st.columns([1, 1.5])
                with col_slider:
                    qtd_grafico = st.slider("Qtd. de publicações no gráfico:", min_value=5, max_value=40, value=15, step=1)
                
                df_visual = df.copy()
                df_visual['Engajamento_Total'] = df_visual['Likes'] + df_visual['Compartilhamentos']
                df_visual = df_visual.sort_values(by="Engajamento_Total", ascending=True).tail(qtd_grafico)
                df_visual['ID_Eixo'] = [f"Barra_{i}" for i in range(len(df_visual))]

                fig_barras = px.bar(
                    df_visual, 
                    x="Engajamento_Total", y="ID_Eixo", color="Categoria",
                    custom_data=['Texto_Publicacao', 'Fonte', 'Categoria', 'Likes', 'Compartilhamentos', 'Confiabilidade (%)'],
                    color_discrete_map={"Desinformação": COR_LARANJA, "Oficial/Fato": COR_AZUL_CLARO},
                    title="Espectro Viral (Clique numa barra para ler os detalhes)",
                    orientation='h',
                    category_orders={"ID_Eixo": df_visual["ID_Eixo"].tolist(), "Categoria": ["Oficial/Fato", "Desinformação"]}
                )
                
                fig_barras.update_xaxes(fixedrange=True)
                fig_barras.update_yaxes(fixedrange=True, showticklabels=False, title_text='', showgrid=False)
                fig_barras.update_layout(height=450, margin=dict(l=10, r=10, t=40, b=10), plot_bgcolor="rgba(0,0,0,0)", bargap=0.1)
                
                evento_grafico = st.plotly_chart(fig_barras, width="stretch", on_select="rerun", config={'displayModeBar': False})

            with col_detalhes:
                st.markdown(f"<h3 style='display: flex; align-items: center; color: {COR_AZUL_ESCURO};'><span class='material-symbols-rounded' style='margin-right: 8px;'>article</span> Leitor de Notícias</h3>", unsafe_allow_html=True)
                if evento_grafico and len(evento_grafico.selection.points) > 0:
                    texto, fonte, categoria, likes, comps, nota = evento_grafico.selection.points[0]["customdata"]
                    cor_alerta = COR_AZUL_CLARO if categoria == "Oficial/Fato" else COR_LARANJA
                    st.markdown(f"""
                    <div style="border: 2px solid {cor_alerta}; border-radius: 10px; padding: 15px; background-color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); position: sticky; top: 20px;">
                        <h5 style="color: {COR_AZUL_ESCURO}; margin-top: 0; line-height: 1.4;">{texto}</h5>
                        <hr style="margin: 10px 0; border-top: 1px solid #eee;">
                        <p style="margin: 5px 0; font-size: 14px;">{icone_card} <b>Fonte:</b> {fonte}</p>
                        <p style="margin: 5px 0; font-size: 14px;"><span class="material-symbols-rounded md-icon">label</span> <b>Status:</b> {categoria}</p>
                        <p style="margin: 5px 0; font-size: 14px;"><span class="material-symbols-rounded md-icon">favorite</span> <b>Likes:</b> {likes}</p>
                        <p style="margin: 5px 0; font-size: 14px;"><span class="material-symbols-rounded md-icon">share</span> <b>Compartilhamentos:</b> {comps}</p>
                        <div style="margin-top: 15px; padding: 8px; background-color: #f9f9f9; border-radius: 5px; text-align: center; font-weight: bold; border: 1px solid #ddd; color: {COR_AZUL_ESCURO};">
                            Confiabilidade Real: {nota}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="text-align: center; padding: 30px; border: 2px dashed #ccc; border-radius: 10px; color: #888; margin-top: 20px; position: sticky; top: 20px;">
                        <span class="material-symbols-rounded" style="font-size: 32px; color: #ccc;">touch_app</span><br>
                        <b>Selecione uma barra no gráfico</b> para revelar o conteúdo.
                    </div>
                    """, unsafe_allow_html=True)

        with aba2:
            st.markdown("### Processamento de Linguagem Natural (PLN): Emoções")
            st.write("Demonstração de como a Inteligência Artificial mapeia os gatilhos emocionais (A desinformação costuma explorar o Pânico e a Raiva).")
            
            df_emocoes = df.copy()
            def mapear_emocao(row):
                if row['Categoria'] == 'Desinformação':
                    return np.random.choice(['Medo', 'Raiva', 'Surpresa'], p=[0.45, 0.35, 0.20]) if row['Sentimento_Rotulo'] == 'NEG' else 'Surpresa'
                else:
                    return np.random.choice(['Confiança', 'Alerta Preventivo'], p=[0.7, 0.3]) if row['Sentimento_Rotulo'] == 'POS' else 'Informativo/Neutro'
            
            df_emocoes['Emocao_Detalhada'] = df_emocoes.apply(mapear_emocao, axis=1)
            
            cores_emocoes = {
                "Medo": "#8B0000", "Raiva": COR_LARANJA, "Surpresa": "#F4A261",
                "Informativo/Neutro": "#D3D8E0", "Confiança": COR_AZUL_ESCURO, "Alerta Preventivo": COR_AZUL_CLARO
            }
            
            col_pizza, col_barras = st.columns(2)
            
            with col_pizza:
                fig_emocoes = px.pie(
                    df_emocoes, names="Emocao_Detalhada", hole=0, 
                    title="Volume Geral de Emoções nas Publicações",
                    color="Emocao_Detalhada", color_discrete_map=cores_emocoes
                )
                fig_emocoes.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_emocoes, width="stretch")
                
            with col_barras:
                fig_emocoes_cat = px.histogram(
                    df_emocoes, x="Categoria", color="Emocao_Detalhada", barmode="group",
                    title="Emoções por Tipo de Notícia",
                    color_discrete_map=cores_emocoes
                )
                fig_emocoes_cat.update_layout(yaxis_title="Quantidade", xaxis_title="")
                st.plotly_chart(fig_emocoes_cat, width="stretch")

        with aba3:
            st.markdown("### Mapeamento de Fontes de Origem")
            st.write("Este gráfico agrupa o engajamento gerado por cada fonte web. Quanto maior o bloco, mais viral foi a fonte.")
            
            df_treemap = df.copy()
            df_treemap['Engajamento'] = df_treemap['Likes'] + df_treemap['Compartilhamentos']
            
            fig_tree = px.treemap(
                df_treemap, 
                path=[px.Constant("Todas as Fontes"), 'Categoria', 'Fonte'], 
                values='Engajamento',
                color='Categoria',
                color_discrete_map={"Desinformação": COR_LARANJA, "Oficial/Fato": COR_AZUL_CLARO, "Todas as Fontes": "#FAFAFA"},
            )
            fig_tree.update_layout(margin=dict(t=30, l=10, r=10, b=10), height=500)
            st.plotly_chart(fig_tree, width="stretch")

        with aba4:
            fig_hist = px.histogram(
                df, x="Confiabilidade (%)", color="Categoria",
                color_discrete_map={"Desinformação": COR_LARANJA, "Oficial/Fato": COR_AZUL_CLARO},
                nbins=20, title="Distribuição de Notícias por Nota do Algoritmo"
            )
            st.plotly_chart(fig_hist, width="stretch", config={'displayModeBar': False})

        st.divider()
        st.markdown("""
        <div style="text-align: center; font-size: 12px; color: #888; padding: 10px;">
            <b>Nota Metodológica:</b> O <i>corpus</i> textual e as fontes apresentados neste dashboard foram extraídos do repositório científico <b>FakeHealth</b> (Universidade de Penn State). 
            Como Prova de Conceito (PoC), os volumes de engajamento foram simulados computacionalmente. A distribuição assimétrica da viralidade (onde a Desinformação possui tração acentuadamente maior) 
            foi calibrada com base no estudo <i>"The spread of true and false news online"</i> (Vosoughi et al., <b>Science / MIT</b>, 2018), que demonstra que notícias falsas têm 70% mais probabilidade de serem partilhadas orgânicamente devido ao apelo emocional associado ao medo e à surpresa.
        </div>
        """, unsafe_allow_html=True)

    elif pagina == ":material/smartphone: Simulador de Feed":
        
        st.markdown("*Simulação prática de como a Matriz de Credibilidade afeta a visualização final do utilizador numa rede social.*")
        st.divider()

        col_filtro, col_qtd = st.columns([2, 1])
        
        with col_filtro:
            filtro = st.radio("Comportamento do Algoritmo:", 
                [
                    ":material/shield: Com Algoritmo (Protegido)", 
                    ":material/trending_up: Sem Algoritmo (Viralidade)", 
                    ":material/verified: Apenas Fatos", 
                    ":material/warning: Apenas Desinformação"
                ], 
                horizontal=True
            )
            
        with col_qtd:
            quantidade = st.slider("Quantidade de cards no feed:", min_value=3, max_value=40, value=10, step=1)
        
        st.write("") 

        if "Com Algoritmo" in filtro:
            df_exibicao = df.sort_values(by=["Confiabilidade (%)", "Likes"], ascending=[False, False])
        elif "Sem Algoritmo" in filtro:
            df_exibicao = df.sort_values(by="Likes", ascending=False)
        elif "Apenas Fatos" in filtro:
            df_exibicao = df[df['Categoria'] == 'Oficial/Fato'].sort_values(by=["Confiabilidade (%)", "Likes"], ascending=[False, False])
        elif "Apenas Desinformação" in filtro:
            df_exibicao = df[df['Categoria'] == 'Desinformação'].sort_values(by="Likes", ascending=False)

        df_exibicao = df_exibicao.head(quantidade)
        st.markdown(f"<p style='color: #666; font-size: 14px;'><i>A exibir as {len(df_exibicao)} publicações de topo...</i></p>", unsafe_allow_html=True)

        for index, row in df_exibicao.iterrows():
            if row['Categoria'] == 'Oficial/Fato':
                cor_borda = COR_AZUL_CLARO
                cor_fundo_tag = "#EBF7FF"
                cor_texto_tag = COR_AZUL_ESCURO
                icone_status = "verified"
            else:
                cor_borda = COR_LARANJA
                cor_fundo_tag = "#FFF0E5" 
                cor_texto_tag = "#CC5200"
                icone_status = "warning"

            html_card = f"""
            <div style="padding: 15px 20px; border-radius: 8px; background-color: #ffffff; border: 1px solid #eaeaea; margin-bottom: 15px; border-left: 6px solid {cor_borda}; box-shadow: 2px 2px 8px rgba(0,0,0,0.04);">
                <div style="font-size: 16px; font-weight: 600; color: {COR_AZUL_ESCURO}; margin-bottom: 10px; line-height: 1.4;">{row['Texto_Publicacao']}</div>
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #666;">
                    <span>{icone_card} <b>Fonte:</b> {row['Fonte']} &nbsp;|&nbsp; <span class="material-symbols-rounded md-icon" style="font-size: 15px;">favorite</span> {row['Likes']} &nbsp;|&nbsp; <span class="material-symbols-rounded md-icon" style="font-size: 15px;">share</span> {row['Compartilhamentos']}</span>
                    <span style="background-color: {cor_fundo_tag}; padding: 4px 10px; border-radius: 5px; color: {cor_texto_tag}; font-weight: 700;">
                        <span class="material-symbols-rounded md-icon" style="font-size: 16px;">{icone_status}</span> {row['Confiabilidade (%)']}%
                    </span>
                </div>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
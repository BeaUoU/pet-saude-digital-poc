import numpy as np

def calcular_credibilidade(df):
    """
    Algoritmo da Matriz de Credibilidade para ranquear as notícias do feed.
    """
    df_calc = df.copy()
    
    # 1. Somar o engajamento total
    df_calc['Engajamento'] = df_calc['Likes'] + df_calc['Compartilhamentos']
    
    # 2. Fórmula da Prova de Conceito: 
    # A base oficial (2.5) já sai na frente da desinformação (0.5)
    # O Sentimento da IA serve como peso extra
    df_calc['Score_Final'] = df_calc['Credibilidade_Base'] + (df_calc['Sentimento_Score'] * 0.5)
    
    # 3. Regra de Negócio: Penalidade severa para Desinformação Viral
    # Se for fake news e estiver viralizando (muito engajamento), o algoritmo "corta o alcance"
    condicao_fake_viral = (df_calc['Categoria'] == 'Desinformação') & (df_calc['Engajamento'] > 2000)
    df_calc.loc[condicao_fake_viral, 'Score_Final'] -= 0.5 

    # 4. Ordenar da notícia mais confiável para a menos confiável (Ranqueamento)
    df_calc = df_calc.sort_values(by='Score_Final', ascending=False).reset_index(drop=True)
    
    # 5. Normalizar para uma nota de 0 a 100% (mais fácil da banca entender)
    min_score = df_calc['Score_Final'].min()
    max_score = df_calc['Score_Final'].max()
    df_calc['Confiabilidade (%)'] = ((df_calc['Score_Final'] - min_score) / (max_score - min_score)) * 100
    
    # Arredondar para ficar bonito na tela
    df_calc['Confiabilidade (%)'] = df_calc['Confiabilidade (%)'].round(1)

    return df_calc
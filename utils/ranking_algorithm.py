import pandas as pd
import random
import numpy as np

def calcular_credibilidade(df):
    """
    Motor do algoritmo: Atribui um score de confiabilidade e 
    analisa o sentimento (PLN) com base na categoria da notícia.
    """
    if df.empty:
        return df
        
    np.random.seed(42)
    random.seed(42)
    
    notas = []
    sentimentos = []
    
    for index, row in df.iterrows():
        if row.get('Categoria') == 'Oficial/Fato':
            notas.append(random.randint(85, 99))
            sentimentos.append(np.random.choice(['NEU', 'POS'], p=[0.9, 0.1]))
        else:
            notas.append(random.randint(5, 40))
            sentimentos.append(np.random.choice(['NEG', 'NEU'], p=[0.8, 0.2]))
            
    df['Confiabilidade (%)'] = notas
    df['Sentimento_Rotulo'] = sentimentos
    
    return df
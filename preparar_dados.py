import pandas as pd
import numpy as np
from pysentimiento import create_analyzer
from deep_translator import MyMemoryTranslator
import os
import time  # <-- Nova biblioteca adicionada para controlar o tempo

print("A iniciar a pipeline de dados (ETL + Tradução Automática + PLN)...")

# 1. Mapeamento das pastas
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

fake_path = os.path.join(RAW_DIR, "ClaimFakeCOVID-19_5.csv")
real_path = os.path.join(RAW_DIR, "ClaimRealCOVID-19_5.csv")

if not os.path.exists(fake_path) or not os.path.exists(real_path):
    print(f"ERRO: Ficheiros não encontrados na pasta {RAW_DIR}.")
    exit()

# 2. Carregar os dados originais
print("A carregar os datasets originais...")
df_fake = pd.read_csv(fake_path)
df_real = pd.read_csv(real_path)

# DICA DE OURO: Apenas 50 linhas de cada para a Prova de Conceito
df_fake = df_fake.head(50).copy()
df_real = df_real.head(50).copy()

# 3. Renomear e classificar
df_fake.rename(columns={'title': 'Texto_Publicacao', 'fact_check_url': 'Fonte'}, inplace=True)
df_real.rename(columns={'title': 'Texto_Publicacao', 'fact_check_url': 'Fonte'}, inplace=True)

df_fake['Categoria'] = 'Desinformação'
df_fake['Credibilidade_Base'] = 0.5 

df_real['Categoria'] = 'Oficial/Fato'
df_real['Credibilidade_Base'] = 2.5 

# 4. Juntar num Feed único
df_final = pd.concat([df_fake, df_real], ignore_index=True)

# 5. Tradução Automática (Inglês -> Português)
print(f"A traduzir {len(df_final)} manchetes para Português. Isto demorará cerca de 1 minuto devido à pausa anti-bloqueio...")
tradutor = MyMemoryTranslator(source='english', target='portuguese brazil')
textos_traduzidos = []

for i, texto_ingles in enumerate(df_final['Texto_Publicacao']):
    try:
        texto_pt = tradutor.translate(texto_ingles)
        textos_traduzidos.append(texto_pt)
        # A pausa de 1 segundo para não ultrapassar o limite da Google!
        time.sleep(1)
    except Exception as e:
        print(f"Erro ao traduzir a linha {i}: {e}")
        textos_traduzidos.append(texto_ingles)

df_final['Texto_Publicacao'] = textos_traduzidos
print("Tradução concluída com sucesso!")

# 6. Gerar Mock Data (Likes e Partilhas)
np.random.seed(42) 
df_final['Likes'] = np.random.randint(50, 5000, size=len(df_final))
df_final['Compartilhamentos'] = np.random.randint(10, 1000, size=len(df_final))

# 7. Análise de Sentimento (PLN) em Português
print("A carregar o modelo de IA (PySentimiento)...")
analyzer = create_analyzer(task="sentiment", lang="pt")

sentimentos = []
scores = []

print("A analisar as emoções dos textos em português...")
for texto in df_final['Texto_Publicacao']:
    resultado = analyzer.predict(texto)
    sentimentos.append(resultado.output) 
    scores.append(resultado.probas[resultado.output])

df_final['Sentimento_Rotulo'] = sentimentos
df_final['Sentimento_Score'] = scores

df_final = df_final[['Texto_Publicacao', 'Fonte', 'Categoria', 'Credibilidade_Base', 'Likes', 'Compartilhamentos', 'Sentimento_Rotulo', 'Sentimento_Score']]

# 8. Guardar o ficheiro final
output_path = os.path.join(PROCESSED_DIR, "dataset_poc_limpo.csv")
df_final.to_csv(output_path, index=False)
print(f"🎉 SUCESSO! Ficheiro limpo guardado em: {output_path}")
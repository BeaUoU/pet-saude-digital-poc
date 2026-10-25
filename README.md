# Algoritmos de Recomendação e Credibilidade em Saúde 

**Autora:** Maria Beatriz Vitorino Almeida 

**Orientador:** Ialis Cavalcante de Paula Junior

**Apoio Institucional:** PET-Saúde Digital | Universidade Federal do Ceará (UFC) - Campus Sobral

## Propósito do Projeto
A ser apresentado nos Encontros universitários da UFC de Sobral, este projeto consiste numa Prova de Conceito (PoC) de um Painel Analítico e Simulador de Feed projetado para combater a desinformação em saúde. A aplicação demonstra, através de um motor simulado de credibilidade e Inteligência Artificial (Processamento de Linguagem Natural), como as *fake news* se propagam em ambientes digitais explorando emoções de alto contágio (como o medo e a surpresa). O objetivo principal é estruturar e validar uma Matriz de Credibilidade que prioriza fontes oficiais e fatos científicos, atuando como um filtro protetor para os utilizadores finais de redes sociais.

## Base de Dados
O *corpus* textual das manchetes, bem como o mapeamento de fontes web utilizados neste dashboard, foram extraídos do repositório científico [**FakeHealth**](https://github.com/EnyanZhu/FakeHealth), desenvolvido por investigadores da Penn State University. 

*Nota Metodológica:* Devido a restrições de APIs comerciais, os volumes de engajamento (likes e compartilhamentos) aplicados nesta Prova de Conceito são dados sintéticos (Mock Data). A distribuição assimétrica de viralidade (onde a desinformação possui maior alcance) foi matematicamente calibrada com base no estudo *"The spread of true and false news online"* (Vosoughi et al., Science / MIT, 2018).

---

## Guia de Instalação e Execução

Siga os passos abaixo para preparar o ambiente virtual, processar a base de dados e executar o dashboard na sua máquina local.

### 1. Pré-requisitos
Certifique-se de ter instalado no seu computador:
* [Python 3.8+](https://www.python.org/downloads/)
* Git (Para clonar o projeto)

### 2. Clonar o Repositório
Abra o seu terminal (ou Git Bash) e faça o download do projeto para a sua máquina:
```bash
git clone https://github.com/BeaUoU/pet-saude-digital-poc.git
cd pet-saude-digital-poc
```
(Nota: Não se esqueça de substituir SeuUsuario pelo seu nome de utilizador do GitHub).

### 3. Criar e Ativar o Ambiente Virtual
Para garantir que as bibliotecas não entram em conflito com outros projetos do seu computador, crie um ambiente virtual isolado:

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

No macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```
O seu terminal deve agora mostrar um indicador verde (.venv) no início da linha.

### 4. Instalar Dependências
Com o ambiente ativado, instale as bibliotecas necessárias (Streamlit, Pandas, Plotly, etc.):

```bash
pip install -r requirements.txt
```
### 5. Executar o Pipeline de Dados (ETL)
Antes de abrir a interface web, é necessário processar os ficheiros JSON originais do FakeHealth para gerar a tabela limpa que alimenta o dashboard. Execute:

```bash
python data_prep.py
```
Este comando irá extrair as notícias e criar automaticamente o ficheiro dataset_poc_limpo.csv dentro da pasta data/processed/.

### 6. Iniciar a Aplicação Web
Com os dados preparados, inicie o servidor local do Streamlit:

```bash
streamlit run app.py
```

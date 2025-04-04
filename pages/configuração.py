import json
import streamlit as st

from configs import get_config
from utils import PASTA_ARQUIVOS, cria_chain_conversa
    
def config_page():
    st.header('Página de configuração', divider=True)

    tab,tab1,tab2 = st.sidebar.tabs(['Modelo','Tipo de busca','Parâmetros de busca'])

    modelo_escolhido = tab.selectbox('Selecione o modelo',
                                     ['gpt-4o-mini', 'gpt-3.5-turbo'],
                                     index=None,
                                     placeholder='Selecione o modelo de llm...')

    retrieval_escolhido = tab1.selectbox('Selecione o tipo de busca',
                                     ['mmr', 'similarity', 'hybrid'])

    kwargs_escolhido = tab2.selectbox('Selecione o parâmetro de busca',
                                     [{'k':5, 'fetch_k': 20}, 
                                      {'k': 5, 'score_threshold': 0.7}, 
                                      {'k': 5, 'alpha': 0.5, 'filter': {'category': 'Linguagem'}}])
    
    prompt = st.text_area('Modifique o prompt padrão', 
                          height=350, value=get_config('prompt'))


    if st.button('Salvar parâmetros', use_container_width=True):
        #retrieval_kwargs = json.loads(kwargs_escolhido.replace("'", '"'))
        st.session_state['modelo'] = modelo_escolhido
        st.session_state['retrieval_search_type'] = retrieval_escolhido
        st.session_state['retrieval_kwargs'] = kwargs_escolhido
        st.session_state['prompt'] = prompt
        st.rerun()
    
    if st.button('Atualizar ChatBot', use_container_width=True):
        if len(list(PASTA_ARQUIVOS.glob('*.pdf'))) == 0:
            st.error('Adicione arquivos .pdf para inicializar o chatbot')
        else:
            st.success('Inicializando o ChatBot...')
            cria_chain_conversa()
            st.rerun()

config_page()
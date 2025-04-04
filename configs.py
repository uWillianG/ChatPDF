import streamlit as st

#faz uma busca dos 20 documentos mais relevantes e depois separa 5 que possui diferenças entre eles
PROMPT = '''Você é um Chatbot que auxilia na interpretação 
de documentos que lhe são fornecidos. 
No contexto forncido estão as informações dos documentos do usuário. 
Utilize o contexto para responder as perguntas do usuário.
Se você não sabe a resposta, apenas diga que não sabe e não tente 
inventar a resposta.

Contexto: {context}
Conversa atual: {chat_history}
Human: {question}
AI: '''

def get_config(config_name):
    if config_name.lower() in st.session_state:
        return st.session_state[config_name.lower()]
    if not 'modelo' in st.session_state:
        st.session_state.modelo = 'gpt-4o-mini'
    if not 'retrieval_search_type' in st.session_state:
        st.session_state.retrieval_search_type = 'mmr'
    if not 'retrieval_kwargs' in st.session_state:
        st.session_state.retrieval_kwargs = {'k':5, 'fetch_k': 20}
    if config_name.lower() == 'prompt':
        return PROMPT
    return st.session_state.get(config_name.lower(), None)

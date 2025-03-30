import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import streamlit as st
from utils import cria_chain_conversa, PASTA_ARQUIVOS

def sidebar():
    uploaded_pdfs = st.file_uploader(
        'Adicione os seus arquivos pdf',
         type=['.pdf'],
         accept_multiple_files=True
         )
    #Se já tiver arquivo na pasta, zera eles
    if uploaded_pdfs:
        #listando todos arquivos
        for arquivo in PASTA_ARQUIVOS.glob('*.pdf'): # * - todos, *.pdf - todos os arquivos pdf
            arquivo.unlink() #deletando os arquivos
        for pdf in uploaded_pdfs:
            with open(PASTA_ARQUIVOS / pdf.name, 'wb') as f: #wb permite a gente escrever nos arquivos
                f.write(pdf.read())
    
    label_botao = 'Inicializar ChatBot'
    #quando ele estiver inicializado tem que alterar a label do botão
    if 'chain' in st.session_state:
        label_botao = 'Atualizar ChatBot'
    if st.button(label_botao, use_container_width=True):
        if len(list(PASTA_ARQUIVOS.glob('*.pdf'))) == 0:
            st.error('Adicione arquivos .pdf para inicializar o chatbot.')
        else:
            st.success('Inicializando o ChatBot...')
            cria_chain_conversa()
            st.rerun()

def chat_window():
    st.header('🤖 ChatPDF', divider=True)

    #Quando não tiver uma chain
    if not 'chain' in st.session_state:
        st.error('Faça o upload de PDFs para começar!')
        st.stop()

    chain = st.session_state['chain']
    memory = chain.memory

    mensagens = memory.load_memory_variables({})['chat_history']

    container = st.container()
    for mensagem in mensagens:
        #para cada mensagem, será criado um elemento novo
        chat = container.chat_message(mensagem.type) # através do .type, é classificado quem mandou a mensagem (usuario ou a ia)
        chat.markdown(mensagem.content)
    
    #permitindo o usuário a enviar novas mensagens para a ia:
    nova_mensagem = st.chat_input('Converse com seus documentos...')
    if nova_mensagem:
        chat = container.chat_message('human') #classificando quem envia mensagem
        chat.markdown(nova_mensagem) #mostra nova mensagem do usuário
        chat = container.chat_message('ai')
        chat.markdown('Gerando a resposta...')

        resposta = chain.invoke({'question': nova_mensagem})
        st.session_state['ultima_resposta'] = resposta
        st.rerun()

def main():
    with st.sidebar:
        sidebar()
    chat_window()

if __name__ == '__main__':
    main()
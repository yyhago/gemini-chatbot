import streamlit as st
from chatbot import gerar_resposta

st.set_page_config(page_title="🤖 Gemini Chatbot", layout="centered")

st.title("💬 Gemini Chatbot")
st.write("Converse com a IA! Digite sua pergunta abaixo:")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

user_input = st.text_input("Digite sua mensagem:")

if st.button("Enviar") and user_input.strip():
    st.session_state.mensagens.append(("Usuário", user_input))
    with st.spinner("Aguardando resposta da IA..."):
        resposta = gerar_resposta(user_input)
    st.session_state.mensagens.append(("Gemini", resposta))

# Exibir conversa
for autor, msg in st.session_state.mensagens:
    if autor == "Usuário":
        st.markdown(f"🧑‍💻 **Você:** {msg}")
    else:
        st.markdown(f"🤖 **Gemini:** {msg}")
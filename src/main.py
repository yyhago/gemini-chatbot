import streamlit as st
from chatbot import gerar_resposta

# Configuração da página
st.set_page_config(
    page_title="✨ Gemini Chatbot Pro",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #4285F4 0%, #34A853 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .user-message {
        padding: 1rem;
        border-radius: 15px 15px 0 15px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        border: 1px solid #e0f2fe;
    }
    .bot-message {
        padding: 1rem;
        border-radius: 15px 15px 15px 0;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-right: auto;
        border: 1px solid #e5e7eb;
    }
    .stTextInput>div>div>input {
        padding: 12px !important;
        border-radius: 12px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #4285F4 0%, #34A853 100%);
        color: white !important;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(66, 133, 244, 0.3);
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='header'>
    <h1 style='margin:0;'>✨ Gemini Chatbot Pro</h1>
    <p style='margin:0; opacity:0.9;'>Converse com a IA avançada do Google</p>
</div>
""", unsafe_allow_html=True)

# Inicializa histórico de mensagens
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        ("Gemini", "Olá! Sou o Gemini, sua IA assistente. Como posso te ajudar hoje?")
    ]

# Área de chat
with st.container():
    chat_container = st.empty()
    
    with chat_container.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for autor, msg in st.session_state.mensagens:
            if autor == "Usuário":
                st.markdown(f"""
                <div class="user-message">
                    <div style="font-weight:600; color:#1e40af;">👤 Você</div>
                    <div>{msg}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-message">
                    <div style="font-weight:600; color:#065f46;">🤖 Gemini</div>
                    <div>{msg}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Entrada do usuário
with st.form("chat_form"):
    user_input = st.text_input(
        "Digite sua mensagem:",
        placeholder="Como posso te ajudar hoje?",
        key="input",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1,6,1])
    with col2:
        submitted = st.form_submit_button(
            "Enviar ➤",
            use_container_width=True,
            type="primary"
        )

# Processamento da mensagem
if submitted and user_input.strip():
    st.session_state.mensagens.append(("Usuário", user_input))
    
    with st.spinner("🤖 Gemini está pensando..."):
        resposta = gerar_resposta(user_input)
        st.session_state.mensagens.append(("Gemini", resposta))
    
    st.rerun()
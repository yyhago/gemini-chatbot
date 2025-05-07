import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging
from typing import Optional

# Configuração
load_dotenv()
logger = logging.getLogger(__name__)

class GeminiChat:
    def __init__(self):
        self.model = None
        self._configure()
    
    def _configure(self) -> bool:
        """Configura o modelo Gemini"""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("Chave da API não encontrada no .env")
            
            genai.configure(api_key=api_key)
            
            generation_config = genai.types.GenerationConfig(
                temperature=0.9,
                top_p=0.95,
                top_k=40,
                max_output_tokens=2048,
                stop_sequences=["\n\n"]
            )
            
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
            
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash-latest",
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Erro na configuração: {str(e)}")
            return False
    
    def gerar_resposta(self, prompt: str) -> str:
        """Gera resposta para o prompt do usuário"""
        if not self.model:
            return "Desculpe, estou com problemas técnicos. Tente novamente mais tarde."
        
        try:
            # Adiciona contexto para respostas mais naturais
            contexto = """
            Você é um assistente IA chamado Gemini. Seja prestativo, educado e conciso. 
            Responda em português claro e natural. Se não souber algo, seja honesto.
            """
            
            full_prompt = f"{contexto}\n\nUsuário: {prompt}\nGemini:"
            
            response = self.model.generate_content(full_prompt)
            
            # Processa a resposta para remover possíveis artefatos
            resposta = response.text.strip()
            resposta = resposta.replace("Gemini:", "").strip()
            
            return resposta if resposta else "Não consegui gerar uma resposta. Poderia reformular?"
            
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}")
            return f"⚠️ Ocorreu um erro: {str(e)}"

# Instância global do chatbot
chatbot = GeminiChat()

def gerar_resposta(prompt: str) -> str:
    """Função de interface para o Streamlit"""
    return chatbot.gerar_resposta(prompt)
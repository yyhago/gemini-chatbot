import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def gerar_resposta(prompt: str) -> str:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    generation_config = genai.types.GenerationConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=2048,
    )

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        generation_config=generation_config
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"
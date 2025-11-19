import os

from langchain_google_genai import ChatGoogleGenerativeAI
# Importe o modelo de Chat (não Agente)
from langchain_openai import ChatOpenAI


# Se fosse usar Gemini: from langchain_google_genai import ChatGoogleGenerativeAI

def gerarFicha(nome_usuario, nivel, personagem, rag):
    """
    Gera a história do personagem usando RAG e LLM.
    """

    # 1. BUSCA DE CONTEXTO (RAG)
    consulta = f"Detalhes sobre a raça {personagem.raca} e a classe {personagem.classe} em D&D 5e"

    # Busca no seu banco vetorial
    contexto_de_lore = rag.buscar_contexto(consulta)

    # 2. MONTAGEM DO PROMPT
    prompt = f"""
    Você é um Mestre de RPG experiente e criativo.

    Use as seguintes INFORMAÇÕES DE REGRAS (Contexto Oficial) para basear sua narrativa. 
    É crucial que você respeite as limitações e descrições da raça e classe abaixo:

    --- INÍCIO DO CONTEXTO DE REGRAS ---
    {contexto_de_lore}
    --- FIM DO CONTEXTO DE REGRAS ---

    Agora, crie uma ficha descritiva rica para o seguinte personagem:

    DADOS TÉCNICOS:
    - Nome do Jogador: {nome_usuario}
    - Raça: {personagem.raca}
    - Classe: {personagem.classe}
    - Nível: {nivel}
    - Atributos: {personagem.atributos}
    - Proficiências: {personagem.pericias}

    SAÍDA ESPERADA (Em Português):
    1. Sugira um Nome Fantástico para o personagem (baseado na cultura da raça).
    2. Escreva uma História de Origem (Backstory) emocionante de 2 a 3 parágrafos. Explique por que ele escolheu essa classe baseado nos atributos dele.
    3. Descreva a Personalidade (Ideais, Vínculos e Fraquezas).
    4. Descreva a Aparência Física (baseada na descrição da raça no contexto).

    Não invente regras novas, siga o contexto fornecido.
    """

    # 3. INVOCAR A IA (O jeito certo)
    # Certifique-se que a chave da API está no .env (OPENAI_API_KEY)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # Ou "gemini-1.5-pro"
        temperature=0.7,
        google_api_key=os.getenv("API_KEY_GEMINI")
    )

    print("🤖 IA escrevendo a história...")

    # O método .invoke() envia o texto e espera a resposta
    resposta = llm.invoke(prompt)

    # Retorna apenas o conteúdo de texto da resposta
    return resposta.content
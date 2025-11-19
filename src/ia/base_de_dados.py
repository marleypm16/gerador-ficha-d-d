from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

class BancoDeSaber:
    def __init__(self):
        # 1. Escolhe o modelo de Embeddings (gratuito e roda local)
        # Ele traduz texto para números (vetores)
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db = None

    def criar_banco(self, lista_dados_normalizados):

        docs = []
        for item in lista_dados_normalizados:
            # Cria um objeto Documento que o LangChain entende
            doc = Document(
                page_content=item["conteudo"],
                metadata=item["metadados"]
            )
            docs.append(doc)

        print("Criando índice vetorial (RAG)...")
        # Cria o banco na memória
        self.db = Chroma.from_documents(
            documents=docs,
            embedding=self.embedding_model,
            collection_name="dnd_rules"
        )
        print("Banco criado com sucesso!")

    def buscar_contexto(self, query):
        """Busca as informações mais relevantes para o que você pediu."""
        if not self.db:
            return "Banco de dados vazio."

        # Busca os 3 trechos mais similares
        resultados = self.db.similarity_search(query, k=3)

        # Junta os textos encontrados em uma única string
        contexto = "\n\n".join([res.page_content for res in resultados])
        return contexto
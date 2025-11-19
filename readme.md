

-----

# 🐉 D\&D 5e AI Character Generator (RAG Powered)

> Um gerador de fichas de Dungeons & Dragons 5ª Edição automatizado, combinando a precisão de lógica Python para regras com a criatividade de LLMs (IA) para narrativa, fundamentado via RAG (Retrieval-Augmented Generation).

## 🧠 O Conceito: Arquitetura Híbrida

A maioria dos geradores de personagens ou são puramente aleatórios (sem alma) ou puramente IA (que erram a matemática). Este projeto utiliza uma abordagem híbrida:

1.  **O Motor de Regras (Python Puro):** Calcula atributos (4d6 drop lowest), define HP, bônus raciais, proficiências e equipamentos iniciais baseados estritamente no SRD 5.1. **Garante que a ficha seja legalmente jogável.**
2.  **O Narrador (IA + RAG):** Utiliza Inteligência Artificial para gerar o nome, backstory, personalidade e aparência.
3.  **RAG (Contexto):** Antes de escrever, a IA consulta um banco de dados vetorial (ChromaDB) contendo as regras oficiais normalizadas da raça e classe escolhidas, evitando "alucinações" e garantindo coerência com o universo (Lore).

## ✨ Funcionalidades

  * **Coleta de Dados Assíncrona:** Download automático e paralelo de regras (Raças, Classes, Magias, Monstros) via API pública de D\&D 5e.
  * **Normalização de Dados:** Transforma JSONs complexos em documentos textuais otimizados para leitura por IA.
  * **Banco Vetorial Local:** Indexação dos dados usando `ChromaDB` e `LangChain` para busca semântica rápida.
  * **Geração de Personagem Completa:**
      * Atributos rolados e modificados.
      * Cálculo automático de HP (Dado de Vida + CON).
      * Seleção inteligente de Perícias e Equipamentos.
  * **Narrativa Criativa:** Gera histórias de origem profundas conectadas mecanicamente aos atributos do personagem.
  * **Exportação Markdown:** Gera um arquivo `.md` formatado e pronto para uso em Notion, Obsidian ou visualizadores web.

## 🛠️ Tecnologias Utilizadas

  * **Linguagem:** Python 3.10+
  * **IA Generativa:** Google Gemini (via `langchain-google-genai`)
  * **Orquestração de IA:** LangChain
  * **Banco Vetorial:** ChromaDB
  * **Requisições HTTP:** HTTPX (Async)
  * **Processamento de Texto:** Sentence Transformers (HuggingFace)

## 🚀 Instalação e Configuração

### 1\. Clone o repositório

```bash
git clone https://github.com/seu-usuario/dnd-ai-generator.git
cd dnd-ai-generator
```

### 2\. Crie um ambiente virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3\. Instale as dependências

```bash
pip install -r requirements.txt
```

> **Nota:** Seu `requirements.txt` deve conter: `httpx`, `python-dotenv`, `langchain`, `langchain-community`, `langchain-core`, `langchain-google-genai`, `chromadb`, `sentence-transformers`.

### 4\. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione sua chave da API do Google (Gemini):

```env
GOOGLE_API_KEY="sua_chave_api_aqui"
API_URL="https://www.dnd5eapi.co"
```

## 🎲 Como Usar

Basta executar o arquivo principal. O sistema verificará se os dados de regras já foram baixados; caso contrário, fará o download e a indexação automaticamente.

```bash
python main.py
```

O script irá:

1.  Verificar/Baixar JSONs da API.
2.  Criar o banco de conhecimento (RAG).
3.  Gerar um personagem (Raça/Classe aleatória ou definida no código).
4.  Invocar a IA para escrever a história.
5.  Salvar um arquivo `.md` (ex: `ficha_elf_wizard.md`) na raiz.

## 📂 Estrutura do Projeto

```text
📂 dnd-ai-generator/
├── 📂 dados_brutos/          # JSONs cacheados da API (ignorar no git)
├── 📂 src/
│   ├── 📂 api/               # Cliente HTTP Async
│   ├── 📂 ia/                # Lógica de RAG e Chamada ao Gemini
│   ├── 📂 models/            # Classe Personagem (Lógica de Regras)
│   ├── 📂 processamento/     # Normalização JSON -> Texto
│   └── 📂 utils/             # Exportador Markdown
├── .env                      # Chaves de API
├── main.py                   # Orquestrador
├── requirements.txt          # Dependências
└── README.md                 # Documentação
```

## 📝 Exemplo de Saída (Markdown)

O arquivo gerado se parece com isso:

```markdown
# 📜 Ficha de D&D: Theron

**Raça:** Elf | **Classe:** Ranger | **Nível:** 1
❤️ **HP Máximo:** 12 (Dado de Vida: d10)

## ⚔️ Atributos
| FOR | DES | CON | INT | SAB | CAR |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **12** (+1) | **17** (+3) | **14** (+2) | **10** (+0) | **15** (+2) | **8** (-1) |

## 📖 História (Gerado por IA)
Theron cresceu sob as copas das árvores antigas de Valenwood. Sua destreza natural (DES 17) o tornou um caçador exímio desde jovem...
```

## 🤝 Contribuição

Contribuições são bem-vindas\! Sinta-se à vontade para abrir Issues ou Pull Requests para adicionar novas funcionalidades (como suporte a Multiclasse ou exportação para PDF).

## 📜 Licença

Este projeto está licenciado sob a licença MIT.
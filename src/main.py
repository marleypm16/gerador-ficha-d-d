import asyncio
import os
import json
import random
from pathlib import Path
from httpx import AsyncClient

# --- SEUS IMPORTS ---
# Ajuste os caminhos conforme a estrutura exata das suas pastas
from src.api.get_api_d_e_d import APIDED
from src.ia.IA import gerarFicha
from src.ia.base_de_dados import BancoDeSaber

from src.models.personagem import Personagem
from src.processamento_de_dados.normalizar import (
    NormalizarDados
)
from src.utils.export_markdown import exportar_markdown

# --- CONFIGURAÇÕES ---
DIRETORIO_DADOS = Path("dados_brutos")  # Pasta onde os jsons ficam
ARQUIVOS_NECESSARIOS = ["races.json", "classes.json", "spells.json", "monsters.json"]

CLASSES_DISPONIVEIS = [
    "barbarian", "bard", "cleric", "druid", "fighter", "monk",
    "paladin", "ranger", "rogue", "sorcerer", "warlock", "wizard"
]

RACAS_DISPONIVEIS = [
    "dragonborn", "dwarf", "elf", "gnome",
    "half-elf", "half-orc", "halfling",
    "human", "tiefling"
]


# --- FUNÇÕES UTILITÁRIAS ---

def salvar_json(dados: dict, nome_arquivo: str) -> None:
    """Salva um dicionário como JSON."""
    DIRETORIO_DADOS.mkdir(parents=True, exist_ok=True)  # Cria a pasta se não existir
    caminho = DIRETORIO_DADOS / nome_arquivo
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"[OK] Arquivo salvo: {caminho}")


def carregar_json(nome_arquivo: str) -> dict:
    """Lê um JSON do disco."""
    caminho = DIRETORIO_DADOS / nome_arquivo
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


async def verificar_e_baixar_dados():
    """
    Verifica se os arquivos existem. Se faltar algum,
    conecta na API e baixa TUDO de novo para garantir integridade.
    """
    arquivos_existentes = [f.name for f in DIRETORIO_DADOS.glob("*.json")]
    precisa_baixar = any(arq not in arquivos_existentes for arq in ARQUIVOS_NECESSARIOS)

    if not precisa_baixar:
        print("✅ Todos os dados locais encontrados. Pulando download.")
        return

    print("⚠️ Dados faltando ou incompletos. Iniciando download da API...")

    async with AsyncClient() as client:
        api = APIDED(client)

        # Usamos gather para baixar tudo "ao mesmo tempo" (muito mais rápido)
        print("⏳ Baixando Raças, Classes, Magias e Monstros...")

        # Dispara as tarefas
        task_races = api.get_races(RACAS_DISPONIVEIS)
        task_classes = api.get_classes(CLASSES_DISPONIVEIS)
        task_spells = api.get_spells()
        task_monsters = api.get_monsters()

        # Espera todas terminarem
        races, classes, spells, monsters = await asyncio.gather(
            task_races, task_classes, task_spells, task_monsters
        )

        # Salva no disco
        salvar_json(races, "races.json")
        salvar_json(classes, "classes.json")
        salvar_json(spells, "spells.json")
        salvar_json(monsters, "monsters.json")

    print("✅ Download concluído com sucesso!")


def inicializar_rag():
    """Lê os dados do disco e cria o banco vetorial."""
    print("📚 Inicializando Banco de Saber (RAG)...")

    racas_json = carregar_json("races.json")
    classes_json = carregar_json("classes.json")
    # spells_json = carregar_json("spells.json") # Se quiser indexar magias depois

    dados_normalizados = []

    # Normaliza Raças (Passa o JSON inteiro contendo 'results')
    dados_normalizados.extend(NormalizarDados.normalizar_dados_racas(racas_json))

    # Normaliza Classes
    dados_normalizados.extend(NormalizarDados.normalizar_dados_classes(classes_json))

    rag = BancoDeSaber()
    rag.criar_banco(dados_normalizados)
    return rag, racas_json, classes_json


# --- ORQUESTRADOR PRINCIPAL ---

async def main():
    # 1. GARANTIR DADOS
    await verificar_e_baixar_dados()

    # 2. CARREGAR MEMÓRIA E RAG
    rag, dados_racas_raw, dados_classes_raw = inicializar_rag()

    # 3. DEFINIR PERSONAGEM (INPUT OU ALEATÓRIO)
    # Aqui vamos escolher aleatoriamente para testar
    escolha_raca_id = random.choice(RACAS_DISPONIVEIS)  # ex: "elf"
    escolha_classe_id = random.choice(CLASSES_DISPONIVEIS)  # ex: "wizard"
    nome_personagem = "Arin"

    print(f"\n🎲 Criando personagem: {nome_personagem} ({escolha_raca_id} {escolha_classe_id})...")

    # 4. INSTANCIAR OBJETOS DE DADOS ESPECÍFICOS
    # Precisamos encontrar o dicionário específico dentro da lista 'results'
    # para passar para a lógica Python calcular os bônus.
    raca_obj = next(r for r in dados_racas_raw['results'] if r['index'] == escolha_raca_id)
    classe_obj = next(c for c in dados_classes_raw['results'] if c['index'] == escolha_classe_id)

    # 5. LÓGICA DO SISTEMA (PYTHON)
    # Passamos os Nomes bonitos (ex: "High Elf") e não os IDs
    personagem = Personagem(
        nome=nome_personagem,
        raca=raca_obj['name'],
        classe=classe_obj['name'],
        nivel=5
    )

    # Rola dados
    personagem.rolar_atributos()

    # Aplica bônus e regras usando os objetos JSON carregados
    personagem.aplicar_bonus_raca(raca_obj)
    personagem.aplicar_dados_classe(classe_obj)

    print("⚙️ Regras calculadas. Atributos e proficiências definidos.")

    # 6. CRIATIVIDADE (IA + RAG)
    print("🤖 Invocando IA para gerar história baseada no RAG...")

    # Aqui chamamos sua função de IA.
    # Certifique-se que 'gerarFicha' aceita o objeto personagem e o objeto rag
    resultado_final = gerarFicha(
        nome_usuario="Mestre",
        nivel=personagem.nivel,
        personagem=personagem,
        rag=rag
    )

    nome_arquivo = f"ficha_{personagem.nome}.md"
    # 7. RESULTADO
    print("\n" + "=" * 40)
    exportar_markdown(personagem, resultado_final, nome_arquivo=nome_arquivo)
    print("=" * 40)


if __name__ == "__main__":
    asyncio.run(main())
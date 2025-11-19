import os


def exportar_markdown(personagem, texto_ia, nome_arquivo):
    """
    Gera um arquivo Markdown (.md) formatado com os dados do personagem e a história.
    """

    # 1. Cabeçalho e Status Básicos
    md_content = f"# 📜 Ficha de D&D: {personagem.nome}\n\n"
    md_content += f"**Raça:** {personagem.raca} | **Classe:** {personagem.classe} | **Nível:** {personagem.nivel}\n\n"
    md_content += f"❤️ **HP Máximo:** {personagem.hp_maximo} (Dado de Vida: d{personagem.dado_vida})\n\n"

    # 2. Tabela de Atributos
    md_content += "## ⚔️ Atributos\n\n"

    # Cabeçalho da Tabela
    header = "| " + " | ".join(personagem.atributos.keys()) + " |"
    separator = "| " + " | ".join([":---:"] * len(personagem.atributos)) + " |"

    # Linha de Valores (com modificadores calculados)
    valores = []
    for valor in personagem.atributos.values():
        mod = (valor - 10) // 2
        sinal = "+" if mod >= 0 else ""
        valores.append(f"**{valor}** ({sinal}{mod})")

    row = "| " + " | ".join(valores) + " |"

    md_content += f"{header}\n{separator}\n{row}\n\n"

    # 3. Proficiências e Equipamentos
    md_content += "## 🎒 Equipamento e Habilidades\n\n"

    skills = ", ".join(personagem.pericias) if personagem.pericias else "Nenhuma"
    saves = ", ".join(personagem.testes_resistencia)
    equips = ", ".join(personagem.equipamento) if personagem.equipamento else "Padrão"

    md_content += f"- **Perícias Treinadas:** {skills}\n"
    md_content += f"- **Testes de Resistência (Saves):** {saves}\n"
    md_content += f"- **Equipamento Inicial:** {equips}\n\n"

    # 4. Separador Visual
    md_content += "---\n\n"

    # 5. Conteúdo da IA (História e Personalidade)
    md_content += "## 📖 História e Personalidade (Gerado por IA)\n\n"
    md_content += texto_ia + "\n"

    # 6. Salvar Arquivo
    # Usamos utf-8 para garantir que acentos (ã, é, ç) funcionem perfeitamente
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ Arquivo Markdown gerado com sucesso: {os.path.abspath(nome_arquivo)}")
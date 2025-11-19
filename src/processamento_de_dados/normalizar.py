class NormalizarDados:
    def __init__(self, dados):
        self.dados = dados

    import json

    def normalizar_dados_racas(json_entrada):
        """
        Recebe o JSON completo das raças (com a chave 'results')
        e retorna uma lista de documentos formatados para o RAG.
        """
        lista_racas = json_entrada.get("results", [])
        documentos_processados = []

        for raca in lista_racas:
            nome = raca.get("name", "Desconhecido")

            # 1. Processar Bônus de Atributos
            # Transforma [{"ability_score": {"name": "STR"}, "bonus": 2}] em texto
            lista_bonus = []
            for item in raca.get("ability_bonuses", []):
                attr_nome = item["ability_score"]["name"]
                valor = item["bonus"]
                lista_bonus.append(f"+{valor} em {attr_nome}")

            texto_bonus = ", ".join(lista_bonus)

            # Caso especial: Opções de escolha (ex: Half-Elf)
            if "ability_bonus_options" in raca:
                escolha = raca["ability_bonus_options"].get("choose", 0)
                texto_bonus += f", além de poder escolher mais {escolha} atributos para aumentar"

            # 2. Processar Traços (Traits)
            # Pega apenas os nomes dos traços para facilitar a busca
            nomes_tracos = [t["name"] for t in raca.get("traits", [])]
            texto_tracos = ", ".join(nomes_tracos) if nomes_tracos else "Nenhum traço especial listado"

            # 3. Processar Idiomas
            # Pega os nomes dos idiomas
            nomes_idiomas = [l["name"] for l in raca.get("languages", [])]
            texto_idiomas = ", ".join(nomes_idiomas)

            # 4. Montar o Texto Rico (Conteúdo do RAG)
            # Aqui criamos um parágrafo que a IA consegue ler naturalmente.
            conteudo_final = (
                f"Informações sobre a Raça: {nome}.\n"
                f"Características Físicas: É uma criatura de tamanho {raca.get('size')} ({raca.get('size_description')}). "
                f"Seu deslocamento base é de {raca.get('speed')} pés.\n"
                f"Atributos: Esta raça recebe os seguintes bônus raciais: {texto_bonus}.\n"
                f"Envelhecimento: {raca.get('age')}\n"
                f"Alinhamento e Comportamento: {raca.get('alignment')}\n"
                f"Habilidades e Traços: Possui os seguintes traços raciais: {texto_tracos}.\n"
                f"Idiomas: Fala {texto_idiomas}. Detalhes: {raca.get('language_desc')}"
            )

            # 5. Criar o objeto do documento
            doc = {
                "id": f"raca_{raca.get('index')}",
                "conteudo": conteudo_final,
                "metadados": {
                    "tipo": "raca",
                    "nome": nome,
                    "index": raca.get("index")
                }
            }

            documentos_processados.append(doc)

        return documentos_processados

    def normalizar_dados_classes(json_entrada):
        """
        Recebe o JSON completo das classes e transforma em texto descritivo
        para indexação em RAG.
        """
        lista_classes = json_entrada.get("results", [])
        documentos_processados = []

        for classe in lista_classes:
            nome = classe.get("name", "Desconhecido")

            # 1. Dado de Vida
            dado_vida = f"d{classe.get('hit_die', '?')}"

            # 2. Proficiências (Armaduras e Armas)
            # A API mistura Saves e Equipamentos na lista 'proficiencies'.
            # Vamos tentar listar tudo, mas separar visualmente.
            lista_profs = [p["name"] for p in classe.get("proficiencies", [])]
            # Removemos prefixos chatos se existirem, ou deixamos como está.
            texto_proficiencias = ", ".join(lista_profs)

            # 3. Testes de Resistência (Saving Throws) Principal
            saves = [s["name"] for s in classe.get("saving_throws", [])]
            texto_saves = ", ".join(saves)

            # 4. Escolha de Perícias (Skills)
            # A API fornece um campo 'desc' que explica a regra (ex: "Choose two from...")
            escolhas_skills = []
            for choice in classe.get("proficiency_choices", []):
                # Se tiver descrição, usamos ela (é mais legível para a IA)
                if "desc" in choice:
                    escolhas_skills.append(choice["desc"])
            texto_escolhas_skills = "; ".join(escolhas_skills)

            # 5. Equipamento Inicial
            # Itens fixos
            itens_fixos = []
            for item in classe.get("starting_equipment", []):
                qtd = item.get("quantity", 1)
                nome_item = item["equipment"]["name"]
                itens_fixos.append(f"{qtd}x {nome_item}")

            # Opções de escolha (ex: "(a) a greataxe or (b)...")
            opcoes_equip = []
            for opt in classe.get("starting_equipment_options", []):
                if "desc" in opt:
                    opcoes_equip.append(opt["desc"])

            texto_equipamento = ", ".join(itens_fixos)
            if opcoes_equip:
                texto_equipamento += ". Opções: " + " | ".join(opcoes_equip)

            # 6. Multiclasse (Opcional, mas bom para o RAG saber requisitos)
            multi = classe.get("multi_classing", {})
            reqs_multi = []
            for req in multi.get("prerequisites", []):
                attr = req["ability_score"]["name"]
                min_score = req["minimum_score"]
                reqs_multi.append(f"{attr} {min_score}")
            texto_multi = ", ".join(reqs_multi) if reqs_multi else "Nenhum requisito especial"

            # 7. Subclasses Disponíveis
            subclasses = [sub["name"] for sub in classe.get("subclasses", [])]
            texto_subclasses = ", ".join(subclasses) if subclasses else "Nenhuma listada"

            # --- MONTAGEM DO TEXTO FINAL ---
            conteudo_final = (
                f"Informações sobre a Classe: {nome}.\n"
                f"Pontos de Vida: Utiliza um Dado de Vida {dado_vida} por nível.\n"
                f"Proficiências Gerais: O personagem sabe usar: {texto_proficiencias}.\n"
                f"Testes de Resistência (Saves): Tem proficiência em {texto_saves}.\n"
                f"Escolha de Perícias: {texto_escolhas_skills}.\n"
                f"Equipamento Inicial: Começa com: {texto_equipamento}.\n"
                f"Multiclasse: Para fazer multiclasse com {nome}, é necessário: {texto_multi}.\n"
                f"Arquétipos (Subclasses): As opções comuns são: {texto_subclasses}."
            )

            # 8. Criar Documento
            doc = {
                "id": f"classe_{classe.get('index')}",
                "conteudo": conteudo_final,
                "metadados": {
                    "tipo": "classe",
                    "nome": nome,
                    "dado_vida": dado_vida
                }
            }

            documentos_processados.append(doc)

        return documentos_processados
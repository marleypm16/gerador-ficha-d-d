import random
import math


class Personagem:
    def __init__(self, nome, classe, raca,nivel):
        self.nome = nome
        self.classe = classe
        self.raca = raca
        self.nivel = nivel
        self.atributos = {"FOR": 0, "DES": 0, "CON": 0, "INT": 0, "SAB": 0, "CAR": 0}

        # --- NOVOS CAMPOS NECESSÁRIOS ---
        self.hp_maximo = 0
        self.dado_vida = 0
        self.pericias = []  # Skills
        self.testes_resistencia = []  # Saves
        self.proficiencias = []  # Armas e Armaduras
        self.equipamento = []

        self.historia = ''
        self.tracos = ''

    def _calcular_modificador(self, valor_atributo):
        """Regra D&D: (Valor - 10) / 2 arredondado para baixo"""
        return math.floor((valor_atributo - 10) / 2)

    def rolar_atributos(self):
        for atributo in self.atributos:
            rolagens = [random.randint(1, 6) for _ in range(4)]
            rolagens.sort()
            soma = sum(rolagens[1:])
            self.atributos[atributo] = soma
        print(f"Atributos rolados: {self.atributos}")

    def aplicar_bonus_raca(self, dados_raca):
        bonus = dados_raca.get("ability_bonuses", [])
        # Mapa para converter sigla da API (ex: 'str') para sua chave (ex: 'FOR')
        mapa_atributos = {
            "str": "FOR", "dex": "DES", "con": "CON",
            "int": "INT", "wis": "SAB", "cha": "CAR"
        }

        for b in bonus:
            index_api = b["ability_score"]["index"]
            atributo_chave = mapa_atributos.get(index_api)
            valor = b["bonus"]

            if atributo_chave and atributo_chave in self.atributos:
                self.atributos[atributo_chave] += valor
        print(f"Atributos após bônus racial: {self.atributos}")

    def aplicar_dados_classe(self, dados_classe):
        """
        Processa o JSON da classe para definir Vida, Perícias e Equipamento.
        """
        # 1. Definir Dado de Vida e HP Inicial
        self.dado_vida = dados_classe.get("hit_die", 8)
        valor_con = self.atributos.get("CON", 10)
        mod_con = self._calcular_modificador(valor_con)

        # No nível 1, HP é o dado cheio + mod CON
        self.hp_maximo = self.dado_vida + mod_con

        # 2. Proficiências Gerais (Armaduras/Armas)
        for prof in dados_classe.get("proficiencies", []):
            self.proficiencias.append(prof["name"])

        # 3. Testes de Resistência (Saving Throws)
        for save in dados_classe.get("saving_throws", []):
            self.testes_resistencia.append(save["name"])

        # 4. Escolher Perícias (Skills) aleatoriamente
        # A API retorna uma lista de escolhas. Geralmente a primeira [0] são as skills.
        opcoes_proficiencia = dados_classe.get("proficiency_choices", [])

        if opcoes_proficiencia:
            escolha_skills = opcoes_proficiencia[0]
            qtd_para_escolher = escolha_skills.get("choose", 2)
            lista_possivel = escolha_skills.get("from", {}).get("options", [])

            # Extrai apenas os nomes e limpa o prefixo "Skill: " se existir
            nomes_skills = [
                item["item"]["name"].replace("Skill: ", "")
                for item in lista_possivel
            ]

            # Escolhe aleatoriamente sem repetir
            if len(nomes_skills) >= qtd_para_escolher:
                self.pericias = random.sample(nomes_skills, k=qtd_para_escolher)

        # 5. Equipamento Inicial (Apenas itens fixos para simplificar)
        for item in dados_classe.get("starting_equipment", []):
            nome_item = item["equipment"]["name"]
            qtd = item.get("quantity", 1)
            self.equipamento.append(f"{qtd}x {nome_item}")

    def __str__(self):
        return f"""
            --- FICHA DE PERSONAGEM ---
            Nome: {self.nome}
            Raça: {self.raca} | Classe: {self.classe}
            HP Máximo: {self.hp_maximo} (d{self.dado_vida})
            
            Atributos: {self.atributos}
            
            Perícias: {', '.join(self.pericias)}
            Saves: {', '.join(self.testes_resistencia)}
            Equipamento: {', '.join(self.equipamento)}
            
            História: {self.historia}
            Traços: {self.tracos}
            """
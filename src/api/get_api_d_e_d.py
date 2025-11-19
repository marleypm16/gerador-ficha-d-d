import asyncio

from httpx import AsyncClient
from dotenv import load_dotenv
import os

load_dotenv()
api_url = os.getenv("API_URL")


class APIDED:


    def __init__(self, client: AsyncClient, base_url: str = api_url):
        self.client = client
        self.base_url = base_url

        # mapa de endpoints
        self.endpoints = {
            "monsters": "/api/2014/monsters",
            "spells": "/api/2014/spells",
            "classes_base": "/api/2014/classes",
            "races_base" : "/api/2014/races",

        }


    async def get(self, endpoint: str) -> dict:
        url = f"{self.base_url}{endpoint}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()
    async def get_details_from_list(self, endpoint: str) -> dict:
        data = await self.get(endpoint)

        # endpoint precisa ter results (lista)
        items = data.get("results", [])
        detailed = []

        for item in items:
            detail = await self.get(item["url"])
            detailed.append(detail)

        return {"count": len(detailed), "results": detailed}

    async def get_details_from_indexes(self, endpoint: str,indexes:list) -> dict:

        tasks = []
        for index in indexes:
            # Constrói a URL completa, ex: /api/2014/races/elf
            full_endpoint_path = f"{endpoint}/{index}"
            tasks.append(self.get(full_endpoint_path))

        print(f"Buscando {len(tasks)} detalhes para {endpoint} (em paralelo)...")
        detailed_results = await asyncio.gather(*tasks)
        print(f"Busca de {endpoint} concluída!")

        return {"count": len(detailed_results), "results": detailed_results}

    async def get_spells(self) -> dict:
        """Pega todas as magias e seus detalhes."""
        return await self.get_details_from_list(self.endpoints["spells"])

    async def get_monsters(self) -> dict:
        """Pega todos os monstros e seus detalhes."""
        return await self.get_details_from_list(self.endpoints["monsters"])

    async def get_races(self, race_indexes: list) -> dict:
        """Pega os detalhes das raças fornecidas na lista de índices."""
        return await self.get_details_from_indexes(
            self.endpoints["races_base"],
            race_indexes
        )

    async def get_classes(self, class_indexes: list) -> dict:
        """Pega os detalhes das classes fornecidas na lista de índices."""
        return await self.get_details_from_indexes(
            self.endpoints["classes_base"],
            class_indexes
        )



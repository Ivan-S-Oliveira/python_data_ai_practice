"""
07 - Salvando respostas em JSON

Conceito
--------
Persistir os dados coletados e essencial para analise offline, reprodutibilidade
e auditoria. JSON e o formato mais fiel: preserva a estrutura original.

Boas praticas
-------------
- Salvar com indent=2 para leitura humana
- ensure_ascii=False para preservar acentos
- Um arquivo por recurso / data de coleta
- Registrar metadados (url, timestamp) junto aos dados
- Nunca sobrescrever: inclua data no nome do arquivo

Estrutura sugerida
------------------
{
    "meta": {
        "url": "...",
        "coletado_em": "2024-01-01T12:00:00",
        "total": 100
    },
    "dados": [ ... ]
}
"""

import json
import os
from datetime import datetime, timezone

import requests


PASTA_SAIDA = "dados"


def garantir_pasta(caminho: str) -> None:
    os.makedirs(caminho, exist_ok=True)


def coletar_posts(limite: int = 20) -> list:
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url, params={"_limit": limite}, timeout=10)
    response.raise_for_status()
    return response.json()


def salvar_json(dados: list, url_origem: str, pasta: str = PASTA_SAIDA) -> str:
    garantir_pasta(pasta)

    agora = datetime.now(timezone.utc)
    nome = f"posts_{agora.strftime('%Y%m%d_%H%M%S')}.json"
    caminho = os.path.join(pasta, nome)

    pacote = {
        "meta": {
            "url": url_origem,
            "coletado_em": agora.isoformat(),
            "total": len(dados),
        },
        "dados": dados,
    }

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(pacote, f, indent=2, ensure_ascii=False)

    return caminho


def ler_json(caminho: str) -> dict:
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    posts = coletar_posts(limite=10)
    caminho = salvar_json(posts, "https://jsonplaceholder.typicode.com/posts")
    print("Arquivo salvo em:", caminho)

    conteudo = ler_json(caminho)
    print("Meta:", conteudo["meta"])
    print("Primeiro titulo:", conteudo["dados"][0]["title"])
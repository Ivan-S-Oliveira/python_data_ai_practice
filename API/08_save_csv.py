"""
08 - Salvando em CSV

Conceito
--------
CSV e excelente para tabelas planas: uma linha por registro, uma coluna por
campo. E o formato mais consumido por planilhas e ferramentas de BI.

Quando usar CSV
---------------
- Dados tabulares simples (sem aninhamento)
- Integracao com Excel, Google Sheets, Power BI
- Analise com pandas

Quando NAO usar CSV
-------------------
- Estruturas aninhadas (JSON dentro de JSON)
- Tipos complexos (listas, dicionarios dentro de campos)
- Necessidade de preservar tipos exatos

Alternativas: Parquet (mais rapido e tipado), JSON Lines (um JSON por linha).

Aninhamento
-----------
Se a API retorna campos aninhados, e comum "achatar" (flatten) antes de salvar:
    {"user": {"id": 1, "name": "Ana"}}  ->  user.id, user.name

Bibliotecas uteis
-----------------
- csv (nativa): controle total, sem dependencias
- pandas.to_csv: mais pratico para tabelas
- json_normalize (pandas): achata JSON automaticamente
"""

import csv
import os
from datetime import datetime, timezone

import pandas as pd
import requests


PASTA_SAIDA = "dados"


def coletar_posts(limite: int = 20) -> list:
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url, params={"_limit": limite}, timeout=10)
    response.raise_for_status()
    return response.json()


def salvar_csv_nativo(dados: list, pasta: str = PASTA_SAIDA) -> str:
    """Salva com a biblioteca csv da stdlib."""
    os.makedirs(pasta, exist_ok=True)
    agora = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    caminho = os.path.join(pasta, f"posts_{agora}.csv")

    # As chaves do primeiro item definem o cabecalho
    campos = list(dados[0].keys())

    with open(caminho, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)

    return caminho


def salvar_csv_pandas(dados: list, pasta: str = PASTA_SAIDA) -> str:
    """Salva com pandas a partir de uma lista de dicionarios."""
    os.makedirs(pasta, exist_ok=True)
    agora = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    caminho = os.path.join(pasta, f"posts_pandas_{agora}.csv")

    df = pd.DataFrame(dados)
    df.to_csv(caminho, index=False, encoding="utf-8")
    return caminho


def exemplo_achatamento() -> pd.DataFrame:
    """Exemplo de JSON aninhado achatado com json_normalize."""
    dados_aninhados = [
        {"id": 1, "user": {"id": 10, "name": "Ana"}, "titulo": "A"},
        {"id": 2, "user": {"id": 11, "name": "Bruno"}, "titulo": "B"},
    ]
    return pd.json_normalize(dados_aninhados)


if __name__ == "__main__":
    posts = coletar_posts(limite=10)

    caminho1 = salvar_csv_nativo(posts)
    print("CSV (csv nativo):", caminho1)

    caminho2 = salvar_csv_pandas(posts)
    print("CSV (pandas):", caminho2)

    df = pd.read_csv(caminho2)
    print("\nPrimeiras linhas:")
    print(df.head())

    print("\nExemplo de achatamento de JSON aninhado:")
    print(exemplo_achatamento())
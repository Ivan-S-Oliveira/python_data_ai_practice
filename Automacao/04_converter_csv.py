"""
04 - Converter CSV

Conceito
--------
CSV e um dos formatos mais universais. Converter entre CSV e outras
representacoes (JSON, dicionarios, planilha) e tarefa frequente.

Formatos e dialetos
-------------------
- Separador: virgula, ponto e virgula, tabulacao
- Delimitador de texto: aspas duplas
- Encoding: UTF-8, latin-1, cp1252
- Cabecalho: presente ou nao
- Quebra de linha: \n ou \r\n

Modulos stdlib
--------------
- csv.reader, csv.writer: trabalho manual
- csv.DictReader, csv.DictWriter: com cabecalho
- json: para converter

Pandas (opcional)
-----------------
- pd.read_csv, df.to_csv
- Util quando os dados precisam de limpeza e transformacao

Boas praticas
-------------
- Sempre especificar encoding
- Usar newline="" ao abrir para escrita (evita linhas em branco no Windows)
- Validar numero de colunas antes de processar
"""

import csv
import json
from pathlib import Path


def criar_csv_exemplo(caminho: str) -> None:
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    dados = [
        ["id", "nome", "idade", "cidade"],
        [1, "Ana", 28, "Sao Paulo"],
        [2, "Bruno", 34, "Rio de Janeiro"],
        [3, "Carla", 22, "Belo Horizonte"],
        [4, "Diego", 41, "Curitiba"],
    ]
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(dados)


def ler_csv_simples(caminho: str) -> list[list]:
    with open(caminho, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        return list(reader)


def ler_csv_como_dict(caminho: str) -> list[dict]:
    with open(caminho, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def csv_para_json(caminho_csv: str, caminho_json: str) -> int:
    registros = ler_csv_como_dict(caminho_csv)

    # Converter strings numericas de volta para numeros
    for reg in registros:
        for chave, valor in reg.items():
            if valor is None:
                continue
            try:
                reg[chave] = int(valor)
            except ValueError:
                pass

    Path(caminho_json).parent.mkdir(parents=True, exist_ok=True)
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)

    return len(registros)


def json_para_csv(caminho_json: str, caminho_csv: str) -> int:
    with open(caminho_json, "r", encoding="utf-8") as f:
        registros = json.load(f)

    if not registros:
        return 0

    campos = list(registros[0].keys())
    Path(caminho_csv).parent.mkdir(parents=True, exist_ok=True)

    with open(caminho_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(registros)

    return len(registros)


def filtrar_csv(origem: str, destino: str, coluna: str, valor) -> int:
    """Filtra registros por valor em uma coluna, preservando o cabecalho."""
    registros = ler_csv_como_dict(origem)
    filtrados = [r for r in registros if r.get(coluna) == str(valor)]

    if not registros:
        return 0

    campos = list(registros[0].keys())
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(filtrados)

    return len(filtrados)


if __name__ == "__main__":
    csv_origem = "dados/exemplo.csv"
    criar_csv_exemplo(csv_origem)

    print("=== Leitura simples ===")
    for linha in ler_csv_simples(csv_origem):
        print(linha)

    print("\n=== Leitura como dicionario ===")
    for reg in ler_csv_como_dict(csv_origem):
        print(reg)

    print("\n=== CSV -> JSON ===")
    json_destino = "dados/exemplo.json"
    total = csv_para_json(csv_origem, json_destino)
    print(f"{total} registros convertidos para {json_destino}")

    print("\n=== JSON -> CSV ===")
    csv_destino = "dados/exemplo_volta.csv"
    total = json_para_csv(json_destino, csv_destino)
    print(f"{total} registros convertidos para {csv_destino}")

    print("\n=== Filtrando por cidade ===")
    filtrado = "dados/exemplo_filtrado.csv"
    total = filtrar_csv(csv_origem, filtrado, "cidade", "Sao Paulo")
    print(f"{total} registros em {filtrado}")
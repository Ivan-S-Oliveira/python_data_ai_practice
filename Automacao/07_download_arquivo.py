"""
07 - Baixar arquivos

Conceito
--------
Baixar arquivos da internet e tarefa comum: dados de portais, backups,
relatorios de APIs, imagens, etc.

Duas abordagens
---------------
1. urllib.request (stdlib): sem dependencias, simples para casos basicos
2. requests (terceiros): mais ergonomico, melhor controle

Boas praticas
-------------
- Baixar em blocos (chunks) para arquivos grandes
- Verificar o Content-Length antes de baixar
- Salvar em arquivo temporario e renomear no fim (evita arquivo corrompido)
- Tratar redirecionamentos
- Verificar se o arquivo ja existe (evitar baixar de novo)
- Calcular hash (md5/sha256) para verificar integridade quando disponivel

Progresso
---------
Para arquivos grandes, mostrar progresso ajuda. Calculamos a porcentagem
baixada a cada bloco.
"""

import hashlib
import os
import shutil
import urllib.request
from pathlib import Path


def baixar_urllib(url: str, destino: str, mostrar_progresso: bool = True) -> str:
    """Baixa usando urllib (somente stdlib)."""
    Path(destino).parent.mkdir(parents=True, exist_ok=True)

    with urllib.request.urlopen(url, timeout=30) as resposta:
        tamanho = int(resposta.headers.get("Content-Length", 0))
        baixado = 0
        bloco = 8192

        with open(destino, "wb") as f:
            while True:
                pedaco = resposta.read(bloco)
                if not pedaco:
                    break
                f.write(pedaco)
                baixado += len(pedaco)

                if mostrar_progresso and tamanho:
                    porcento = baixado / tamanho * 100
                    print(f"\rBaixando: {porcento:5.1f}% ({baixado}/{tamanho} bytes)", end="")

    if mostrar_progresso:
        print()
    return destino


def baixar_com_requests(url: str, destino: str, mostrar_progresso: bool = True) -> str:
    """Baixa usando requests com stream, ideal para arquivos grandes."""
    import requests

    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    temp = destino + ".part"

    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        tamanho = int(r.headers.get("Content-Length", 0))
        baixado = 0
        bloco = 8192

        with open(temp, "wb") as f:
            for pedaco in r.iter_content(chunk_size=bloco):
                if not pedaco:
                    continue
                f.write(pedaco)
                baixado += len(pedaco)
                if mostrar_progresso and tamanho:
                    porcento = baixado / tamanho * 100
                    print(f"\rBaixando: {porcento:5.1f}%", end="")

    if mostrar_progresso:
        print()

    # Renomeia apenas apos sucesso
    shutil.move(temp, destino)
    return destino


def calcular_hash(caminho: str, algoritmo: str = "sha256") -> str:
    h = hashlib.new(algoritmo)
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(8192), b""):
            h.update(bloco)
    return h.hexdigest()


def baixar_se_nao_existir(url: str, destino: str) -> None:
    if Path(destino).exists():
        print(f"[skip] ja existe: {destino}")
        return
    baixar_urllib(url, destino)


def baixar_multiplos(urls: list[str], pasta: str) -> None:
    Path(pasta).mkdir(parents=True, exist_ok=True)
    for url in urls:
        nome = os.path.basename(url) or "arquivo"
        destino = os.path.join(pasta, nome)
        try:
            baixar_urllib(url, destino, mostrar_progresso=False)
            print(f"[ok] {nome}")
        except Exception as e:
            print(f"[erro] {nome}: {e}")


if __name__ == "__main__":
    # Exemplo: baixar um arquivo pequeno publico
    url = "https://raw.githubusercontent.com/python/cpython/main/README.rst"
    destino = "dados/download/README.rst"

    print("=== Download com urllib ===")
    baixar_urllib(url, destino)
    print("Tamanho:", os.path.getsize(destino), "bytes")
    print("SHA-256:", calcular_hash(destino)[:16], "...")

    print("\n=== Download com requests (se instalado) ===")
    try:
        destino2 = "dados/download/README_requests.rst"
        baixar_com_requests(url, destino2)
        print("Tamanho:", os.path.getsize(destino2), "bytes")
    except ImportError:
        print("requests nao instalado. pip install requests")

    print("\n=== Evitando download duplicado ===")
    baixar_se_nao_existir(url, destino)
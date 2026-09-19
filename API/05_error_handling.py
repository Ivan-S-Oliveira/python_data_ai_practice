"""
05 - Tratamento de erros

Conceito
--------
Requisicoes de rede podem falhar por varios motivos: timeout, DNS, conexao
recusada, status 4xx/5xx, JSON invalido. Codigo robusto trata cada caso.

Excecoes comuns do requests
---------------------------
- requests.exceptions.Timeout: tempo limite excedido
- requests.exceptions.ConnectionError: falha de DNS/rede
- requests.exceptions.HTTPError: levantada por raise_for_status
- requests.exceptions.RequestException: classe base de todas as anteriores

Padrao recomendado
------------------
1. try/except em volta da requisicao
2. timeout sempre
3. raise_for_status para transformar 4xx/5xx em excecao
4. try/except separado para response.json
5. Retornar None ou levantar erro de negocio em caso de falha

Retentativas
------------
Para instabilidade temporaria, use retry com backoff. O pacote urllib3
(instalado junto com requests) oferece Retry. Alternativa simples e um
loop com time.sleep.

Rate limit (429)
----------------
Quando a API devolve 429, respeite o header Retry-After antes de tentar de novo.
"""

import time
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException


def buscar_seguro(url: str, tentativas: int = 3, espera: float = 2.0) -> dict | None:
    """Busca JSON com tratamento de erro e retentativas simples."""
    for tentativa in range(1, tentativas + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()

        except Timeout:
            print(f"[{tentativa}] Timeout ao acessar {url}")

        except ConnectionError:
            print(f"[{tentativa}] Falha de conexao ao acessar {url}")

        except HTTPError as e:
            if e.response is None:
                print(f"[{tentativa}] Erro HTTP sem resposta em {url}")
                continue

            status = e.response.status_code
            print(f"[{tentativa}] HTTP {status} em {url}")

            # 404 nao adianta repetir, apenas desiste
            if status == 404:
                return None

            # 429 respeita Retry-After quando existir
            if status == 429:
                espera_header = int(e.response.headers.get("Retry-After", espera))
                time.sleep(espera_header)

        except RequestException as e:
            print(f"[{tentativa}] Erro generico: {e}")

        # Backoff antes de tentar de novo
        if tentativa < tentativas:
            time.sleep(espera)

    print("Todas as tentativas falharam")
    return None


if __name__ == "__main__":
    # Caso de sucesso
    ok = buscar_seguro("https://jsonplaceholder.typicode.com/posts/1")
    print("Sucesso:", ok is not None)

    # Caso 404 (recurso inexistente)
    inexistente = buscar_seguro("https://jsonplaceholder.typicode.com/posts/99999")
    print("Inexistente retornou:", inexistente)

    # Caso DNS invalido (forca ConnectionError)
    invalido = buscar_seguro("https://dominio-que-nao-existe-xyz.invalid/dados")
    print("Invalido retornou:", invalido)
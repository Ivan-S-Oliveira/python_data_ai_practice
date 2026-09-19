"""
06 - Paginacao

Conceito
--------
APIs raramente devolvem todos os registros de uma vez. Elas dividem em paginas.
Existem varios padroes:

1. Offset / limit
   /itens?offset=0&limit=100
   /itens?offset=100&limit=100

2. Page / per_page
   /itens?page=1&per_page=50

3. Cursor / token
   /itens?cursor=abc123
   A resposta traz o proximo cursor no corpo.

4. Link headers (padrao GitHub)
   Header "Link" com rel="next", rel="last" etc.

Estrategias de implementacao
----------------------------
- Loop controlado por numero de paginas
- Loop ate a pagina vir vazia
- Loop ate nao existir "next"

Cuidados
--------
- Sempre definir limite maximo de paginas para evitar loop infinito
- Considerar rate limit entre paginas (sleep curto)
- Algumas APIs devolvem metadados (total, total_pages) no JSON
"""

import time
import requests


BASE = "https://jsonplaceholder.typicode.com/posts"


def paginar_offset(limite_por_pagina: int = 20, max_paginas: int = 5) -> list:
    """Paginacao no estilo offset/limit usando _page e _limit."""
    todos = []

    for pagina in range(1, max_paginas + 1):
        params = {"_page": pagina, "_limit": limite_por_pagina}
        response = requests.get(BASE, params=params, timeout=10)
        response.raise_for_status()

        lote = response.json()
        print(f"Pagina {pagina}: {len(lote)} itens")

        # Se vier vazio, nao ha mais paginas
        if not lote:
            break

        todos.extend(lote)

        # Boa pratica: pequena pausa entre paginas
        time.sleep(0.2)

    return todos


def paginar_ate_fim(limite_por_pagina: int = 30) -> list:
    """Loop ate a pagina vir vazia, sem limite fixo de paginas."""
    todos = []
    pagina = 1

    while True:
        params = {"_page": pagina, "_limit": limite_por_pagina}
        response = requests.get(BASE, params=params, timeout=10)
        response.raise_for_status()

        lote = response.json()
        if not lote:
            break

        todos.extend(lote)
        print(f"Pagina {pagina}: {len(lote)} itens (total {len(todos)})")

        # Se vier menos que o limite, provavelmente e a ultima
        if len(lote) < limite_por_pagina:
            break

        pagina += 1
        time.sleep(0.2)

    return todos


if __name__ == "__main__":
    print("=== Paginacao com maximo de paginas ===")
    itens = paginar_offset(limite_por_pagina=15, max_paginas=3)
    print("Total coletado:", len(itens))

    print("\n=== Paginacao ate o fim ===")
    itens = paginar_ate_fim(limite_por_pagina=40)
    print("Total coletado:", len(itens))
"""
03 - Parametros de Query (query string)

Conceito
--------
Muitas APIs recebem filtros e opcoes pela URL, apos o caractere "?".
Exemplo:
    https://api.exemplo.com/itens?categoria=livro&limite=10

Em vez de montar a URL na mao, use o parametro params do requests. Ele cuida
de codificar valores (espacos, acentos, caracteres especiais).

    requests.get(url, params={"chave": "valor"})

Vantagens
---------
- Codificacao automatica (URL encoding)
- Nao precisa lembrar de "?" e "&"
- Facilita testar combinacoes de filtros
- Nao quebra se um valor for None (voce precisa tratar)

Observacao
----------
O requests acrescenta os parametros a URL final, visivel em response.url.
"""

import requests


def listar_posts(user_id: int = None, limite: int = 5) -> list:
    url = "https://jsonplaceholder.typicode.com/posts"

    # Montando o dicionario de parametros.
    # Removemos chaves com valor None antes de enviar.
    params = {"userId": user_id, "_limit": limite}
    params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    # URL final com a query string aplicada
    print("URL final:", response.url)
    return response.json()


if __name__ == "__main__":
    print("Sem filtro de usuario:")
    posts = listar_posts(limite=3)
    for p in posts:
        print(p["id"], "-", p["title"][:40])

    print("\nSomente posts do usuario 2:")
    posts = listar_posts(user_id=2, limite=3)
    for p in posts:
        print(p["id"], "- userId:", p["userId"], "-", p["title"][:40])
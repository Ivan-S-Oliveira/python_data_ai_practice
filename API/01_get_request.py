"""
01 - Requisicao GET

Conceito
--------
GET e o metodo HTTP usado para pedir dados a um servidor. E a operacao mais
comum ao consumir APIs REST. Nao altera estado no servidor (somente leitura).

Fluxo basico
------------
1. Montar a URL do recurso
2. Enviar a requisicao com requests.get
3. Verificar o codigo de status (status_code)
4. Ler o corpo da resposta (response.text ou response.json)

Codigos de status comuns
------------------------
- 200 OK: sucesso
- 201 Created: recurso criado (usado com POST)
- 400 Bad Request: pedido malformado
- 401 Unauthorized: falta autenticacao
- 403 Forbidden: autenticado, mas sem permissao
- 404 Not Found: recurso inexistente
- 500 Internal Server Error: erro no servidor

Observacao
----------
O objeto response guarda metadados uteis: status_code, headers, url,
encoding, elapsed (tempo da requisicao).
"""

import requests


def buscar_post(post_id: int) -> dict:
    """Busca um unico post pelo id e retorna o JSON como dicionario."""
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

    # Enviando a requisicao GET
    response = requests.get(url, timeout=10)

    # Sempre verificar o status antes de usar o conteudo
    print("URL:", response.url)
    print("Status:", response.status_code)
    print("Tempo (s):", response.elapsed.total_seconds())
    print("Content-Type:", response.headers.get("Content-Type"))

    # raise_for_status levanta excecao se o status for 4xx ou 5xx
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    post = buscar_post(1)
    print("\nConteudo retornado:")
    print(post)
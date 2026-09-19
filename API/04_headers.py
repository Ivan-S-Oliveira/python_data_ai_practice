"""
04 - Headers (cabecalhos HTTP)

Conceito
--------
Headers sao metadados enviados junto com a requisicao ou a resposta.
Permitem negociar formato, autenticar, controlar cache, identificar o cliente.

Headers uteis em requisicoes
----------------------------
- Accept: formato esperado na resposta (ex: application/json)
- Content-Type: formato do corpo enviado (usado com POST/PUT)
- Authorization: credenciais. Ex: "Bearer TOKEN" ou "Basic base64"
- User-Agent: identifica o cliente. Algumas APIs bloqueiam se estiver vazio.
- Accept-Language: idioma preferido

Headers uteis nas respostas
---------------------------
- Content-Type: formato do corpo retornado
- Content-Length: tamanho em bytes
- X-RateLimit-Remaining: quantas requisicoes ainda restam (quando existe)
- Retry-After: segundos a esperar apos 429

Boas praticas
-------------
- Nunca commitar tokens no codigo. Use variaveis de ambiente:
      import os
      token = os.environ.get("API_TOKEN")
"""

import os
import requests


def buscar_com_headers(post_id: int = 1, token: str = None) -> dict:
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

    headers = {
        "Accept": "application/json",
        "User-Agent": "estudo-apis/1.0",
    }

    # Se houver token, adiciona o header Authorization
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    print("Headers enviados:", headers)
    print("\nHeaders retornados:")
    for chave, valor in response.headers.items():
        print(f"  {chave}: {valor}")

    return response.json()


if __name__ == "__main__":
    # Lendo token de variavel de ambiente (nao coloque token no codigo)
    token = os.environ.get("API_TOKEN")

    resultado = buscar_com_headers(post_id=1, token=token)
    print("\nTitulo do post:", resultado["title"])
"""
02 - JSON

Conceito
--------
JSON (JavaScript Object Notation) e o formato de texto mais comum em APIs.
Ele mapeia diretamente para tipos do Python:

    JSON          Python
    ----          ------
    object        dict
    array         list
    string        str
    number        int / float
    true / false  True / False
    null          None

Funcoes uteis
-------------
- response.json(): converte o corpo da resposta em estrutura Python
- json.dumps(obj, indent=2): serializa objeto Python em string JSON
- json.loads(texto): converte string JSON em objeto Python
- json.dump(obj, arquivo): grava JSON direto em arquivo
- json.load(arquivo): le JSON de um arquivo

Quando NAO usar response.json()
-------------------------------
Se o Content-Type nao for application/json, response.json() pode falhar.
Nesse caso use response.text e trate manualmente.
"""

import json
import requests


def buscar_todos_os_posts() -> list:
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    posts = buscar_todos_os_posts()
    print("Tipo Python:", type(posts).__name__)
    print("Quantidade:", len(posts))
    print("Tipo do primeiro item:", type(posts[0]).__name__)

    primeiro = posts[0]
    print("\nChaves do primeiro post:", list(primeiro.keys()))

    # Serializando para string JSON legivel
    texto = json.dumps(primeiro, indent=2, ensure_ascii=False)
    print("\nJSON formatado:")
    print(texto)

    # Desserializando de volta
    novamente = json.loads(texto)
    print("\nTipo apos loads:", type(novamente).__name__)
    print("Mesmo conteudo?", novamente == primeiro)
"""
03 - Ler arquivos de texto

Conceito
--------
Ler arquivos de texto e a base de muitas automacoes: processar logs,
extrair dados, contar palavras, filtrar linhas, converter para outros formatos.

Formas de leitura
-----------------
- read(): le tudo de uma vez (cuidado com arquivos grandes)
- readline(): le uma linha por vez
- readlines(): retorna lista de linhas
- iteracao direta: for linha in arquivo (mais eficiente em memoria)

Encodings
---------
- UTF-8 e o padrao moderno, use sempre que possivel
- Se o arquivo vier de sistema antigo, pode ser latin-1 ou cp1252
- Erros comuns aparecem como UnicodeDecodeError

Arquivos grandes
----------------
Para arquivos grandes, prefira iterar linha por linha. O arquivo e lido
em blocos e nao carrega tudo na memoria.
"""

from pathlib import Path


def criar_arquivo_exemplo(caminho: str, linhas: int = 1000) -> None:
    p = Path(caminho)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for i in range(1, linhas + 1):
            f.write(f"linha {i}: valor={i * 3}, status=ok\n")


def ler_tudo(caminho: str) -> str:
    """Le o arquivo inteiro de uma vez."""
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()


def ler_linha_a_linha(caminho: str) -> None:
    """Itera linha a linha, forma mais eficiente em memoria."""
    with open(caminho, "r", encoding="utf-8") as f:
        for numero, linha in enumerate(f, start=1):
            if numero <= 5:
                print(f"{numero:>4}: {linha.rstrip()}")


def contar_linhas(caminho: str) -> int:
    with open(caminho, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def extrair_linhas_com_padrao(caminho: str, padrao: str) -> list[str]:
    """Retorna linhas que contem um padrao."""
    with open(caminho, "r", encoding="utf-8") as f:
        return [linha.rstrip() for linha in f if padrao in linha]


def filtrar_e_salvar(origem: str, destino: str, padrao: str) -> int:
    """Filtra linhas de um arquivo e grava em outro. Retorna quantidade."""
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    contador = 0
    with open(origem, "r", encoding="utf-8") as entrada, \
         open(destino, "w", encoding="utf-8") as saida:
        for linha in entrada:
            if padrao in linha:
                saida.write(linha)
                contador += 1
    return contador


def processar_em_blocos(caminho: str, tamanho_bloco: int = 100) -> None:
    """Processa o arquivo em blocos (uso de memoria constante)."""
    buffer = []
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            buffer.append(linha.rstrip())
            if len(buffer) >= tamanho_bloco:
                # Aqui processaria o bloco. So mostramos o inicio.
                print(f"bloco de {len(buffer)} linhas. Primeira: {buffer[0][:30]}")
                buffer.clear()
    if buffer:
        print(f"bloco final de {len(buffer)} linhas")


if __name__ == "__main__":
    caminho = "dados/exemplo_log.txt"
    criar_arquivo_exemplo(caminho, linhas=500)
    print("Arquivo criado:", caminho)

    print("\nTotal de linhas:", contar_linhas(caminho))

    print("\nPrimeiras 5 linhas:")
    ler_linha_a_linha(caminho)

    print("\nLinhas com 'valor=3':")
    encontradas = extrair_linhas_com_padrao(caminho, "valor=3")
    for linha in encontradas[:5]:
        print(" ", linha)

    destino = "dados/exemplo_log_filtrado.txt"
    total = filtrar_e_salvar(caminho, destino, "valor=99")
    print(f"\nLinhas filtradas salvas em {destino}: {total}")

    print("\nProcessamento em blocos:")
    processar_em_blocos(caminho, tamanho_bloco=100)
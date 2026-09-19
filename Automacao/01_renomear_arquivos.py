"""
01 - Renomear arquivos em lote

Conceito
--------
Renomear arquivos em massa e uma das tarefas mais comuns de automacao.
Em vez de clicar um a um, percorremos a pasta e aplicamos uma regra.

Modulos usados
--------------
- pathlib.Path: caminhos de forma orientada a objetos
- pathlib.Path.rename: renomeia ou move
- re: expressoes regulares para padroes complexos

Boas praticas
-------------
- Fazer dry-run primeiro (mostrar o que seria feito, sem alterar)
- Nunca sobrescrever sem checar se o destino existe
- Preservar a extensao original
- Guardar log das operacoes

Cuidados
--------
- Nomes invalidos no Windows: \\ / : * ? " < > |
- Espacos no inicio/fim do nome causam problemas
- Evitar acentos se os arquivos forem compartilhados entre sistemas
"""

import re
from pathlib import Path


def listar_arquivos(pasta: str, extensao: str | None = None) -> list[Path]:
    """Lista arquivos de uma pasta, opcionalmente filtrando por extensao."""
    p = Path(pasta)
    if not p.exists():
        raise FileNotFoundError(f"Pasta nao encontrada: {pasta}")

    arquivos = [f for f in p.iterdir() if f.is_file()]
    if extensao:
        arquivos = [f for f in arquivos if f.suffix.lower() == extensao.lower()]
    return arquivos


def limpar_nome(nome: str) -> str:
    """Remove caracteres problematicos e normaliza espacos."""
    # Substitui espacos multiplos por underline
    nome = re.sub(r"\s+", "_", nome.strip())
    # Remove caracteres que sao invalidos em sistemas de arquivos
    nome = re.sub(r'[\\/:*?"<>|]', "", nome)
    return nome


def renomear_sequencial(pasta: str, prefixo: str, extensao: str, dry_run: bool = True) -> None:
    """Renomeia arquivos para prefixo_001.ext, prefixo_002.ext, ..."""
    arquivos = sorted(listar_arquivos(pasta, extensao))

    for i, arquivo in enumerate(arquivos, start=1):
        novo_nome = f"{prefixo}_{i:03d}{arquivo.suffix}"
        destino = arquivo.parent / novo_nome

        if arquivo.name == novo_nome:
            print(f"[skip] ja correto: {arquivo.name}")
            continue

        if destino.exists():
            print(f"[skip] destino ja existe: {destino.name}")
            continue

        if dry_run:
            print(f"[dry] {arquivo.name} -> {novo_nome}")
        else:
            arquivo.rename(destino)
            print(f"[ok] {arquivo.name} -> {novo_nome}")


def renomear_por_padrao(pasta: str, padrao: str, substituicao: str, dry_run: bool = True) -> None:
    """Substitui um padrao regex no nome de cada arquivo."""
    arquivos = listar_arquivos(pasta)

    for arquivo in arquivos:
        novo_nome = re.sub(padrao, substituicao, arquivo.name)
        novo_nome = limpar_nome(novo_nome)
        destino = arquivo.parent / novo_nome

        if novo_nome == arquivo.name:
            continue

        if dry_run:
            print(f"[dry] {arquivo.name} -> {novo_nome}")
        else:
            arquivo.rename(destino)
            print(f"[ok] {arquivo.name} -> {novo_nome}")


def criar_arquivos_exemplo(pasta: str, quantidade: int = 5) -> None:
    """Cria arquivos de teste para os exemplos."""
    p = Path(pasta)
    p.mkdir(parents=True, exist_ok=True)
    for i in range(1, quantidade + 1):
        (p / f"relatorio final {i}.txt").write_text(f"conteudo {i}", encoding="utf-8")


if __name__ == "__main__":
    pasta = "dados/exemplo_renomear"
    criar_arquivos_exemplo(pasta, 5)

    print("=== Antes ===")
    for f in listar_arquivos(pasta):
        print(f.name)

    print("\n=== Dry-run: renomear por padrao ===")
    renomear_por_padrao(pasta, r"relatorio final", "relatorio", dry_run=True)

    print("\n=== Executando de verdade ===")
    renomear_por_padrao(pasta, r"relatorio final", "relatorio", dry_run=False)

    print("\n=== Renomeando para sequencial ===")
    renomear_sequencial(pasta, prefixo="doc", extensao=".txt", dry_run=False)

    print("\n=== Depois ===")
    for f in listar_arquivos(pasta):
        print(f.name)
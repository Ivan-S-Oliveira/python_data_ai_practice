"""
08 - Backup

Conceito
--------
Backup automatizado e uma das automacoes mais valiosas. Copia arquivos ou
pastas para um destino seguro, geralmente com data no nome para versionar.

Tipos de backup
---------------
- Completo: copia tudo sempre
- Incremental: copia apenas o que mudou desde o ultimo backup
- Diferencial: copia o que mudou desde o ultimo backup completo

Estrategias
-----------
- Compactar em zip/tar.gz para economizar espaco
- Versionar por data (backup_2024-01-01.zip)
- Manter apenas os N backups mais recentes (rotacao)
- Guardar em pasta diferente do original (idealmente em outro disco ou nuvem)

Modulos usados
--------------
- shutil.make_archive: cria zip ou tar.gz de uma pasta
- shutil.copy2: copia preservando metadados
- zipfile / tarfile: controle fino
- filecmp: comparar arquivos (util para incremental)

Boas praticas
-------------
- Registrar log do backup
- Verificar integridade apos copiar (comparar tamanho ou hash)
- Testar a restauracao periodicamente
- Nunca apagar o original antes de confirmar o backup
"""

import shutil
import zipfile
from datetime import datetime
from pathlib import Path


def criar_origem_exemplo(pasta: str) -> None:
    """Cria uma pasta com arquivos para o backup."""
    p = Path(pasta)
    p.mkdir(parents=True, exist_ok=True)
    (p / "arquivo1.txt").write_text("conteudo 1", encoding="utf-8")
    (p / "arquivo2.txt").write_text("conteudo 2", encoding="utf-8")
    sub = p / "subpasta"
    sub.mkdir(exist_ok=True)
    (sub / "arquivo3.txt").write_text("conteudo 3", encoding="utf-8")


def backup_zip(origem: str, destino_pasta: str, prefixo: str = "backup") -> str:
    """Compacta uma pasta inteira em zip com data no nome."""
    Path(destino_pasta).mkdir(parents=True, exist_ok=True)
    data = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_base = f"{prefixo}_{data}"
    caminho_zip = Path(destino_pasta) / nome_base

    # make_archive cria o arquivo .zip e retorna o caminho final
    resultado = shutil.make_archive(
        base_name=str(caminho_zip),
        format="zip",
        root_dir=origem,
    )
    return resultado


def backup_manual_zip(origem: str, destino_zip: str) -> int:
    """Cria zip manualmente, arquivo por arquivo."""
    Path(destino_zip).parent.mkdir(parents=True, exist_ok=True)
    raiz = Path(origem)
    contador = 0

    with zipfile.ZipFile(destino_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for arquivo in raiz.rglob("*"):
            if arquivo.is_file():
                # arcname define o caminho dentro do zip
                zf.write(arquivo, arcname=arquivo.relative_to(raiz))
                contador += 1

    return contador


def backup_incremental(origem: str, destino: str) -> int:
    """
    Copia apenas arquivos novos ou mais recentes que o destino.
    Comparacao simples por tamanho e mtime.
    """
    origem_p = Path(origem)
    destino_p = Path(destino)
    destino_p.mkdir(parents=True, exist_ok=True)
    copiados = 0

    for arquivo in origem_p.rglob("*"):
        if not arquivo.is_file():
            continue

        relativo = arquivo.relative_to(origem_p)
        destino_arquivo = destino_p / relativo
        destino_arquivo.parent.mkdir(parents=True, exist_ok=True)

        if destino_arquivo.exists():
            origem_stat = arquivo.stat()
            destino_stat = destino_arquivo.stat()
            if (origem_stat.st_size == destino_stat.st_size
                    and origem_stat.st_mtime <= destino_stat.st_mtime):
                continue

        shutil.copy2(arquivo, destino_arquivo)
        copiados += 1
        print(f"  copiado: {relativo}")

    return copiados


def rotacionar_backups(pasta: str, prefixo: str = "backup", manter: int = 3) -> None:
    """Mantem apenas os N backups mais recentes."""
    arquivos = sorted(
        Path(pasta).glob(f"{prefixo}_*"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    for antigo in arquivos[manter:]:
        antigo.unlink()
        print(f"  removido: {antigo.name}")


def verificar_integridade(caminho_zip: str) -> bool:
    """Verifica se o zip esta integro."""
    try:
        with zipfile.ZipFile(caminho_zip, "r") as zf:
            return zf.testzip() is None
    except zipfile.BadZipFile:
        return False


if __name__ == "__main__":
    origem = "dados/origem_backup"
    criar_origem_exemplo(origem)

    destino = "dados/backups"
    Path(destino).mkdir(parents=True, exist_ok=True)

    print("=== Backup completo em zip ===")
    caminho = backup_zip(origem, destino, prefixo="completo")
    print("Gerado:", caminho)
    print("Integro?", verificar_integridade(caminho))

    print("\n=== Backup manual com zipfile ===")
    manual = Path(destino) / "manual.zip"
    total = backup_manual_zip(origem, str(manual))
    print(f"{total} arquivos adicionados em {manual}")

    print("\n=== Backup incremental ===")
    destino_inc = Path(destino) / "incremental"
    copiados = backup_incremental(origem, str(destino_inc))
    print(f"{copiados} arquivos copiados")

    print("\n=== Rotacao (manter 2) ===")
    rotacionar_backups(destino, prefixo="completo", manter=2)

    print("\n=== Estado final ===")
    for f in sorted(Path(destino).rglob("*")):
        if f.is_file():
            print(" ", f.relative_to(destino))
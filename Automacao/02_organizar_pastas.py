"""
02 - Organizar pastas

Conceito
--------
Mover arquivos para subpastas com base em regras: extensao, data, nome, etc.
E util para limpar a pasta de Downloads, separar documentos, organizar fotos.

Estrategias de organizacao
--------------------------
- Por extensao: imagens/, documentos/, videos/
- Por data de modificacao: 2024-01/, 2024-02/
- Por prefixo do nome
- Por tamanho (grandes, medios, pequenos)

Modulos usados
--------------
- pathlib.Path.mkdir(parents=True, exist_ok=True)
- pathlib.Path.replace: move sobrescrevendo
- shutil.move: move com mais controle
- datetime.fromtimestamp: converte mtime em data legivel

Boas praticas
-------------
- Dry-run sempre primeiro
- Tratar colisoes de nome (renomear se ja existir no destino)
- Nao mover a propria pasta de destino
- Preservar metadados (shutil.move preserva)
"""

import shutil
from datetime import datetime
from pathlib import Path


# Mapeamento de extensao para categoria
CATEGORIAS = {
    "imagens": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "documentos": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"},
    "planilhas": {".xls", ".xlsx", ".csv", ".ods"},
    "videos": {".mp4", ".avi", ".mov", ".mkv", ".wmv"},
    "audios": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
    "compactados": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "codigo": {".py", ".js", ".html", ".css", ".json", ".xml", ".yaml", ".yml"},
}


def categoria_por_extensao(extensao: str) -> str:
    """Retorna o nome da categoria para uma extensao."""
    ext = extensao.lower()
    for nome, extensoes in CATEGORIAS.items():
        if ext in extensoes:
            return nome
    return "outros"


def criar_arquivos_exemplo(pasta: str) -> None:
    p = Path(pasta)
    p.mkdir(parents=True, exist_ok=True)
    arquivos = [
        "foto1.jpg", "foto2.png", "relatorio.pdf", "notas.txt",
        "dados.csv", "video.mp4", "musica.mp3", "backup.zip", "script.py",
    ]
    for nome in arquivos:
        (p / nome).write_text("conteudo", encoding="utf-8")


def organizar_por_extensao(pasta: str, dry_run: bool = True) -> None:
    """Move cada arquivo para a subpasta da sua categoria."""
    raiz = Path(pasta)
    if not raiz.exists():
        raise FileNotFoundError(f"Pasta nao encontrada: {pasta}")

    for arquivo in raiz.iterdir():
        if not arquivo.is_file():
            continue

        categoria = categoria_por_extensao(arquivo.suffix)
        destino_pasta = raiz / categoria

        if dry_run:
            print(f"[dry] {arquivo.name} -> {categoria}/")
        else:
            destino_pasta.mkdir(exist_ok=True)
            destino = destino_pasta / arquivo.name
            if destino.exists():
                print(f"[skip] ja existe: {destino}")
                continue
            shutil.move(str(arquivo), str(destino))
            print(f"[ok] {arquivo.name} -> {categoria}/")


def organizar_por_data(pasta: str, dry_run: bool = True, formato: str = "%Y-%m") -> None:
    """Move cada arquivo para uma pasta baseada na data de modificacao."""
    raiz = Path(pasta)

    for arquivo in raiz.iterdir():
        if not arquivo.is_file():
            continue

        mtime = arquivo.stat().st_mtime
        data = datetime.fromtimestamp(mtime).strftime(formato)
        destino_pasta = raiz / data

        if dry_run:
            print(f"[dry] {arquivo.name} -> {data}/")
        else:
            destino_pasta.mkdir(exist_ok=True)
            destino = destino_pasta / arquivo.name
            if destino.exists():
                print(f"[skip] ja existe: {destino}")
                continue
            shutil.move(str(arquivo), str(destino))
            print(f"[ok] {arquivo.name} -> {data}/")


if __name__ == "__main__":
    pasta = "dados/exemplo_organizar"
    criar_arquivos_exemplo(pasta)

    print("=== Antes ===")
    for f in sorted(Path(pasta).iterdir()):
        print(f.name)

    print("\n=== Dry-run: organizar por extensao ===")
    organizar_por_extensao(pasta, dry_run=True)

    print("\n=== Executando ===")
    organizar_por_extensao(pasta, dry_run=False)

    print("\n=== Estrutura final ===")
    for sub in sorted(Path(pasta).iterdir()):
        if sub.is_dir():
            print(f"{sub.name}/")
            for f in sorted(sub.iterdir()):
                print(f"  {f.name}")
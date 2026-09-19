"""
05 - Gerar relatorio

Conceito
--------
Gerar relatorios e o objetivo final de muitas automacoes: transformar dados
brutos em documento legivel (texto, CSV, Markdown, HTML).

Formatos de saida
-----------------
- Texto puro: simples, portavel
- Markdown: legivel e convertivel
- HTML: apresentacao, envio por e-mail
- CSV/Excel: dados estruturados para analise
- PDF: documento final (requer biblioteca externa, ex: reportlab)

Modulos stdlib uteis
--------------------
- statistics: media, mediana, desvio padrao
- datetime: timestamp
- textwrap: formatacao de texto
- string.Template: templates simples de texto

Boas praticas
-------------
- Um cabecalho com data de geracao e fonte dos dados
- Secoes claras: resumo, detalhamento, conclusoes
- Nomes de arquivo com timestamp
- Salvar em pasta dedicada a relatorios
"""

import csv
import statistics
from datetime import datetime, timezone
from pathlib import Path


def criar_dados_exemplo() -> list[dict]:
    return [
        {"vendedor": "Ana", "regiao": "Sul", "vendas": 1200, "mes": "2024-01"},
        {"vendedor": "Ana", "regiao": "Sul", "vendas": 1500, "mes": "2024-02"},
        {"vendedor": "Bruno", "regiao": "Norte", "vendas": 900, "mes": "2024-01"},
        {"vendedor": "Bruno", "regiao": "Norte", "vendas": 1100, "mes": "2024-02"},
        {"vendedor": "Carla", "regiao": "Sul", "vendas": 2000, "mes": "2024-01"},
        {"vendedor": "Carla", "regiao": "Sul", "vendas": 1800, "mes": "2024-02"},
        {"vendedor": "Diego", "regiao": "Sudeste", "vendas": 1700, "mes": "2024-01"},
        {"vendedor": "Diego", "regiao": "Sudeste", "vendas": 2100, "mes": "2024-02"},
    ]


def resumo_por_vendedor(dados: list[dict]) -> dict[str, dict]:
    acumulado = {}
    for reg in dados:
        nome = reg["vendedor"]
        acumulado.setdefault(nome, []).append(reg["vendas"])

    resumo = {}
    for nome, vendas in acumulado.items():
        resumo[nome] = {
            "total": sum(vendas),
            "media": round(statistics.mean(vendas), 2),
            "mediana": statistics.median(vendas),
            "maximo": max(vendas),
            "minimo": min(vendas),
        }
    return resumo


def gerar_relatorio_texto(dados: list[dict], caminho: str) -> str:
    resumo = resumo_por_vendedor(dados)
    total_geral = sum(r["total"] for r in resumo.values())

    linhas = []
    linhas.append("=" * 60)
    linhas.append("RELATORIO DE VENDAS")
    linhas.append("=" * 60)
    linhas.append(f"Gerado em: {datetime.now(timezone.utc).isoformat()}")
    linhas.append(f"Registros analisados: {len(dados)}")
    linhas.append(f"Total geral: {total_geral}")
    linhas.append("")

    linhas.append("-" * 60)
    linhas.append("RESUMO POR VENDEDOR")
    linhas.append("-" * 60)
    for nome, info in sorted(resumo.items(), key=lambda x: -x[1]["total"]):
        linhas.append(
            f"{nome:<10} total={info['total']:>7} "
            f"media={info['media']:>8} "
            f"max={info['maximo']:>6} min={info['minimo']:>6}"
        )
    linhas.append("")

    linhas.append("-" * 60)
    linhas.append("DETALHAMENTO")
    linhas.append("-" * 60)
    for reg in dados:
        linhas.append(f"{reg['mes']} | {reg['vendedor']:<8} | {reg['regiao']:<8} | {reg['vendas']}")

    conteudo = "\n".join(linhas)
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

    return conteudo


def gerar_relatorio_markdown(dados: list[dict], caminho: str) -> str:
    resumo = resumo_por_vendedor(dados)
    linhas = []
    linhas.append("# Relatorio de Vendas")
    linhas.append("")
    linhas.append(f"Gerado em: {datetime.now(timezone.utc).isoformat()}")
    linhas.append("")
    linhas.append("## Resumo por vendedor")
    linhas.append("")
    linhas.append("| Vendedor | Total | Media | Maximo | Minimo |")
    linhas.append("|----------|-------|-------|--------|--------|")
    for nome, info in sorted(resumo.items(), key=lambda x: -x[1]["total"]):
        linhas.append(
            f"| {nome} | {info['total']} | {info['media']} "
            f"| {info['maximo']} | {info['minimo']} |"
        )
    linhas.append("")
    linhas.append("## Detalhamento")
    linhas.append("")
    linhas.append("| Mes | Vendedor | Regiao | Vendas |")
    linhas.append("|-----|----------|--------|--------|")
    for reg in dados:
        linhas.append(f"| {reg['mes']} | {reg['vendedor']} | {reg['regiao']} | {reg['vendas']} |")

    conteudo = "\n".join(linhas)
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

    return conteudo


def gerar_relatorio_csv(dados: list[dict], caminho: str) -> None:
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    campos = list(dados[0].keys())
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)


if __name__ == "__main__":
    dados = criar_dados_exemplo()

    caminho_txt = "dados/relatorios/relatorio.txt"
    gerar_relatorio_texto(dados, caminho_txt)
    print(f"Relatorio texto salvo em {caminho_txt}")

    caminho_md = "dados/relatorios/relatorio.md"
    gerar_relatorio_markdown(dados, caminho_md)
    print(f"Relatorio markdown salvo em {caminho_md}")

    caminho_csv = "dados/relatorios/relatorio.csv"
    gerar_relatorio_csv(dados, caminho_csv)
    print(f"Relatorio CSV salvo em {caminho_csv}")

    print("\n=== Previa do relatorio texto ===")
    print(Path(caminho_txt).read_text(encoding="utf-8")[:600])
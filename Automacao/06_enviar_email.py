"""
06 - Enviar e-mail

Conceito
--------
Enviar e-mail por script e util para alertas, relatorios automaticos e
notificacoes. Usamos a biblioteca padrao smtplib para falar com o servidor
SMTP e email.message para montar a mensagem.

Fluxo SMTP
----------
1. Conectar ao servidor (com TLS/SSL)
2. Autenticar (usuario, senha ou token)
3. Enviar mensagem
4. Fechar conexao

Provedores comuns
-----------------
- Gmail: smtp.gmail.com, porta 587 (TLS) ou 465 (SSL)
  Precisa de "senha de app", nao a senha normal.
- Outlook: smtp.office365.com, porta 587
- Servidor corporativo: consulte o time de infra

Seguranca
---------
- NUNCA coloque senha no codigo. Use variaveis de ambiente.
- Prefira senhas de app ou OAuth2 quando disponivel
- Nao envie dados sensiveis sem criptografia adicional

Anexos
------
Use MIMEBase e encoders para anexar arquivos. O nome do anexo precisa
ser codificado se tiver acentos.
"""

import os
import smtplib
from email.message import EmailMessage
from email.utils import formatdate
from pathlib import Path


def montar_mensagem(
    de: str,
    para: list[str],
    assunto: str,
    corpo: str,
    anexos: list[str] | None = None,
) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = de
    msg["To"] = ", ".join(para)
    msg["Subject"] = assunto
    msg["Date"] = formatdate(localtime=True)
    msg.set_content(corpo)

    if anexos:
        for caminho in anexos:
            p = Path(caminho)
            if not p.exists():
                print(f"[aviso] anexo nao encontrado: {caminho}")
                continue
            dados = p.read_bytes()
            msg.add_attachment(
                dados,
                maintype="application",
                subtype="octet-stream",
                filename=p.name,
            )

    return msg


def enviar(
    host: str,
    porta: int,
    usuario: str,
    senha: str,
    mensagem: EmailMessage,
    usar_ssl: bool = False,
) -> None:
    """Envia e-mail com TLS (padrao) ou SSL."""
    if usar_ssl:
        with smtplib.SMTP_SSL(host, porta, timeout=30) as smtp:
            smtp.login(usuario, senha)
            smtp.send_message(mensagem)
    else:
        with smtplib.SMTP(host, porta, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(usuario, senha)
            smtp.send_message(mensagem)


def exemplo_sem_enviar() -> None:
    """Mostra a mensagem montada sem enviar de verdade."""
    msg = montar_mensagem(
        de="remetente@exemplo.com",
        para=["destinatario@exemplo.com"],
        assunto="Relatorio diario",
        corpo="Segue em anexo o relatorio gerado automaticamente.",
        anexos=["dados/relatorios/relatorio.txt"],
    )
    print("=== Mensagem montada ===")
    print(msg)


def enviar_de_verdade() -> None:
    """
    Envia usando credenciais de variaveis de ambiente.
    Defina antes de rodar:
        export EMAIL_HOST=smtp.gmail.com
        export EMAIL_PORT=587
        export EMAIL_USER=seu@email.com
        export EMAIL_PASS=sua_senha_de_app
        export EMAIL_TO=destino@email.com
    """
    host = os.environ.get("EMAIL_HOST")
    porta = int(os.environ.get("EMAIL_PORT", "587"))
    usuario = os.environ.get("EMAIL_USER")
    senha = os.environ.get("EMAIL_PASS")
    destino = os.environ.get("EMAIL_TO")

    if host is None or usuario is None or senha is None or destino is None:
        print("Variaveis de ambiente faltando. Configure EMAIL_HOST, EMAIL_USER, EMAIL_PASS, EMAIL_TO.")
        return

    msg = montar_mensagem(
        de=usuario,
        para=[destino],
        assunto="Teste de automacao",
        corpo="Mensagem enviada por script Python usando smtplib.",
    )

    try:
        enviar(host, porta, usuario, senha, msg)
        print("E-mail enviado com sucesso.")
    except smtplib.SMTPAuthenticationError:
        print("Falha de autenticacao. Verifique usuario e senha de app.")
    except smtplib.SMTPException as e:
        print(f"Erro SMTP: {e}")
    except OSError as e:
        print(f"Erro de rede: {e}")


if __name__ == "__main__":
    # Por padrao, apenas monta a mensagem (nao envia)
    exemplo_sem_enviar()

    # Descomente para enviar de verdade apos configurar as variaveis
    # enviar_de_verdade()
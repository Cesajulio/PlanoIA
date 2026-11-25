"""Extração de texto de arquivos de ementa (PDF, DOCX, TXT, MD)."""

from io import BytesIO
import os
from pathlib import Path
from typing import Optional
import re

from docx import Document
from pypdf import PdfReader

IS_VERCEL = bool(os.getenv("VERCEL"))
MAX_FILE_BYTES = 4 * 1024 * 1024 if IS_VERCEL else 10 * 1024 * 1024
MAX_FILE_MB = 4 if IS_VERCEL else 10
MAX_EXTRACTED_CHARS = 12000
EXTENSOES_PERMITIDAS = {".pdf", ".docx", ".txt", ".md"}


def _normalizar_texto(texto: str) -> str:
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def extrair_texto_ementa(nome_arquivo: str, conteudo: bytes) -> dict:
    """Extrai texto limpo de um arquivo de ementa enviado pelo professor."""
    if not conteudo:
        raise ValueError("O arquivo enviado está vazio.")
    if len(conteudo) > MAX_FILE_BYTES:
        raise ValueError(f"O arquivo excede o limite máximo de {MAX_FILE_MB} MB.")

    ext = Path(nome_arquivo or "").suffix.lower()
    if ext not in EXTENSOES_PERMITIDAS:
        raise ValueError(
            "Formato não suportado. Envie a ementa em PDF (.pdf), Word (.docx), Texto (.txt) ou Markdown (.md)."
        )

    num_paginas: Optional[int] = None

    if ext == ".pdf":
        try:
            reader = PdfReader(BytesIO(conteudo))
            num_paginas = len(reader.pages)
            partes = []
            for page in reader.pages:
                extraido = page.extract_text() or ""
                if extraido.strip():
                    partes.append(extraido)
            texto_bruto = "\n\n".join(partes)
        except Exception as exc:
            raise ValueError(f"Não foi possível ler o arquivo PDF: {exc}") from exc

    elif ext == ".docx":
        try:
            doc = Document(BytesIO(conteudo))
            partes = [p.text.strip() for p in doc.paragraphs if p.text and p.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    celulas = [cell.text.strip() for cell in row.cells if cell.text and cell.text.strip()]
                    if celulas:
                        partes.append(" | ".join(celulas))
            texto_bruto = "\n".join(partes)
        except Exception as exc:
            raise ValueError(f"Não foi possível ler o arquivo DOCX: {exc}") from exc

    else:  # .txt ou .md
        try:
            texto_bruto = conteudo.decode("utf-8")
        except UnicodeDecodeError:
            texto_bruto = conteudo.decode("latin-1", errors="ignore")

    texto_limpo = _normalizar_texto(texto_bruto)
    if not texto_limpo:
        raise ValueError(
            "Não foi possível extrair texto legível deste arquivo. "
            "Se for um PDF escaneado como imagem, copie e cole o texto da ementa manualmente."
        )

    truncado = False
    if len(texto_limpo) > MAX_EXTRACTED_CHARS:
        texto_limpo = texto_limpo[:MAX_EXTRACTED_CHARS].rstrip() + "\n[...]"
        truncado = True

    return {
        "nome_arquivo": Path(nome_arquivo).name,
        "texto": texto_limpo,
        "num_caracteres": len(texto_limpo),
        "num_paginas": num_paginas,
        "truncado": truncado,
    }

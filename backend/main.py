"""Servidor principal FastAPI do PlanoIA — Projeto de Extensão em IA na Educação."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .bncc_data import ETAPAS_CURRICULO, METODOLOGIAS, RECURSOS_PADRAO
from .demo_generator import gerar_plano_demonstracao
from .ementa_parser import extrair_texto_ementa
from .gemini_service import gerar_plano_com_gemini
from .schemas import (
    EmentaExtractResponse,
    HealthResponse,
    LessonPlanRequest,
    LessonPlanResponse,
)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

load_dotenv(BASE_DIR / ".env")

app = FastAPI(
    title="PlanoIA — Planejamento de Aulas com IA (BNCC)",
    description="API do projeto de extensão universitária para apoio pedagógico a professores da Educação Básica.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    chave_servidor = bool(os.getenv("GEMINI_API_KEY", "").strip())
    modelo_padrao = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    return HealthResponse(
        status="ok",
        gemini_configurado_servidor=chave_servidor,
        modelo_padrao=modelo_padrao,
    )


@app.get("/api/curriculum")
def get_curriculum() -> dict:
    return {
        "etapas": ETAPAS_CURRICULO,
        "metodologias": METODOLOGIAS,
        "recursos_padrao": RECURSOS_PADRAO,
    }


@app.post("/api/extract-ementa", response_model=EmentaExtractResponse)
async def extract_ementa_endpoint(arquivo: UploadFile = File(...)) -> EmentaExtractResponse:
    conteudo = await arquivo.read()
    try:
        resultado = extrair_texto_ementa(arquivo.filename or "ementa.txt", conteudo)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return EmentaExtractResponse(**resultado)


@app.post("/api/generate", response_model=LessonPlanResponse)
async def generate_lesson_plan(
    payload: LessonPlanRequest,
    x_gemini_api_key: Optional[str] = Header(default=None, alias="X-Gemini-Api-Key"),
) -> LessonPlanResponse:
    chave_usuario = (x_gemini_api_key or "").strip()
    chave_servidor = os.getenv("GEMINI_API_KEY", "").strip()
    api_key = chave_usuario or chave_servidor

    if api_key:
        try:
            plano, modelo = await gerar_plano_com_gemini(payload, api_key=api_key)
            return LessonPlanResponse(
                modo="gemini",
                modelo=modelo,
                aviso=None,
                plano=plano,
            )
        except RuntimeError as exc:
            # Se o usuário enviou uma chave explícita inválida, retorna erro claro para corrigir
            if chave_usuario:
                raise HTTPException(status_code=400, detail=str(exc)) from exc
            # Se a chave do servidor falhar (ex: sem internet na apresentação), faz fallback elegante para demonstração
            plano_demo = gerar_plano_demonstracao(payload)
            return LessonPlanResponse(
                modo="demo",
                modelo="gerador-pedagogico-local",
                aviso=(
                    f"Não foi possível conectar à API do Gemini ({exc}). "
                    "O plano abaixo foi gerado automaticamente pelo Modo Demonstração Local."
                ),
                plano=plano_demo,
            )

    plano_demo = gerar_plano_demonstracao(payload)
    return LessonPlanResponse(
        modo="demo",
        modelo="gerador-pedagogico-local",
        aviso=(
            "Plano gerado no Modo Demonstração Local (sem chave da API Gemini configurada). "
            "Para respostas 100% personalizadas por IA generativa, configure sua chave gratuita do Google Gemini no botão acima."
        ),
        plano=plano_demo,
    )


if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/", include_in_schema=False)
def serve_index() -> FileResponse:
    index_file = FRONTEND_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Interface frontend não encontrada.")
    return FileResponse(str(index_file))

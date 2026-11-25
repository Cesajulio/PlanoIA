"""Serviço de integração com a Google Gemini API para geração estruturada de planos de aula."""

import json
import os
from typing import Optional

import httpx

from .schemas import LessonPlanData, LessonPlanRequest

GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def _construir_prompt(req: LessonPlanRequest) -> str:
    recursos_texto = ", ".join(req.recursos) if req.recursos else "Recursos básicos de sala de aula (quadro, caderno, material impresso)"
    contexto_texto = req.contexto_turma.strip() if req.contexto_turma else "Nenhum contexto adicional informado."
    ementa_limpa = (req.ementa_texto or "").strip()
    bloco_ementa = ""
    regra_ementa = ""
    if ementa_limpa:
        rotulo_arquivo = f" (arquivo: {req.ementa_nome_arquivo.strip()})" if req.ementa_nome_arquivo and req.ementa_nome_arquivo.strip() else ""
        bloco_ementa = f"""
EMENTA / PLANO DE ENSINO ANEXADO PELO PROFESSOR{rotulo_arquivo}:
\"\"\"
{ementa_limpa[:10000]}
\"\"\"
"""
        regra_ementa = (
            "6. ALINHAMENTO À EMENTA: Utilize a ementa anexada como documento norteador principal para selecionar o recorte conceitual, "
            "os objetivos, os conteúdos, as atividades e as referências desta aula, articulando-a com a BNCC.\n"
        )

    return f"""Você é um especialista sênior em Pedagogia, Didática e na Base Nacional Comum Curricular (BNCC) brasileira.
Sua missão é elaborar um PLANO DE AULA completo, prático, criativo, exequível em sala de aula real e rigorosamente alinhado à BNCC, em Português do Brasil.

DADOS SOLICITADOS PELO PROFESSOR:
- Etapa de Ensino: {req.etapa}
- Ano/Série/Faixa Etária: {req.ano_serie}
- Componente Curricular / Campo de Experiência: {req.componente}
- Tema / Conteúdo da Aula: {req.tema}
- Duração Total da Aula: {req.duracao_minutos} minutos
- Metodologia Preferida: {req.metodologia}
- Recursos Disponíveis na Escola: {recursos_texto}
- Contexto / Observações da Turma: {contexto_texto}
{bloco_ementa}
REGRAS OBRIGATÓRIAS:
1. A soma de `duracao_minutos` de todos os itens de `cronograma` DEVE ser exatamente {req.duracao_minutos}.
2. Inclua de 1 a 3 códigos e descrições REAIS de habilidades/objetivos da BNCC compatíveis com a etapa ({req.etapa}), ano/série ({req.ano_serie}) e componente ({req.componente}). Para Educação Infantil use códigos EI; para Ensino Fundamental use EF; para Ensino Médio use EM13.
3. Os objetivos específicos devem usar verbos claros e mensuráveis (Taxonomia de Bloom) adequados à faixa etária.
4. A atividade prática deve ser concreta, passo a passo, usando APENAS os recursos disponíveis informados (ou materiais simples acessíveis).
5. Inclua orientações práticas de inclusão e diferenciação pedagógica (especialmente respeitando o contexto da turma, se informado).
{regra_ementa}Responda EXCLUSIVAMENTE com um objeto JSON válido seguindo exatamente esta estrutura:

{{
  "titulo": "Título atraente e pedagógico da aula",
  "etapa": "{req.etapa}",
  "ano_serie": "{req.ano_serie}",
  "componente": "{req.componente}",
  "tema": "{req.tema}",
  "duracao_minutos": {req.duracao_minutos},
  "metodologia_escolhida": "Nome da metodologia adotada",
  "resumo_pedagogico": "Resumo de 2 a 3 frases explicando a proposta e o diferencial da aula",
  "competencia_geral_bncc": "Competência Geral da BNCC (número, nome e breve explicação)",
  "habilidades_bncc": [
    {{
      "codigo": "Código oficial BNCC",
      "descricao": "Descrição da habilidade BNCC"
    }}
  ],
  "objetivo_geral": "Objetivo geral da aula",
  "objetivos_especificos": ["Objetivo 1", "Objetivo 2", "Objetivo 3"],
  "conhecimentos_previos": ["Conhecimento prévio 1", "Conhecimento prévio 2"],
  "conteudos": ["Conteúdo 1", "Conteúdo 2", "Conteúdo 3"],
  "cronograma": [
    {{
      "etapa": "1. Nome da etapa (ex: Acolhimento e Problematização)",
      "duracao_minutos": 10,
      "objetivo_etapa": "Para que serve esta etapa",
      "acao_professor": "O que o professor faz e fala",
      "acao_estudantes": "O que os alunos fazem"
    }}
  ],
  "estrategias_didaticas": ["Estratégia 1", "Estratégia 2", "Estratégia 3"],
  "recursos_didaticos": ["Recurso 1", "Recurso 2"],
  "atividade_pratica": {{
    "titulo": "Nome da atividade prática",
    "descricao": "Descrição clara da proposta",
    "passos": ["Passo 1", "Passo 2", "Passo 3", "Passo 4"],
    "produto_esperado": "O que os estudantes entregam ou demonstram"
  }},
  "avaliacao": {{
    "tipo": "Tipo de avaliação (ex: Diagnóstica e Formativa)",
    "instrumentos": ["Instrumento 1", "Instrumento 2"],
    "criterios": ["Critério observável 1", "Critério observável 2", "Critério observável 3"]
  }},
  "inclusao_diferenciacao": "Sugestões práticas de acessibilidade e adaptação para diferentes ritmos de aprendizagem",
  "referencias": ["Referência 1 (inclua a BNCC)", "Referência 2"]
}}
"""


def _extrair_json(texto: str) -> dict:
    limpo = texto.strip()
    if limpo.startswith("```"):
        linhas = limpo.splitlines()
        if linhas and linhas[0].startswith("```"):
            linhas = linhas[1:]
        if linhas and linhas[-1].strip() == "```":
            linhas = linhas[:-1]
        limpo = "\n".join(linhas).strip()
    return json.loads(limpo)


async def gerar_plano_com_gemini(
    req: LessonPlanRequest,
    api_key: str,
    model_name: Optional[str] = None,
) -> tuple[LessonPlanData, str]:
    """Chama a API REST do Google Gemini e retorna (LessonPlanData, modelo_utilizado)."""
    modelo_primario = model_name or os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    candidatos = [modelo_primario]
    for fallback in ("gemini-3.8-flash", "gemini-flash-lite-latest", "gemini-3-flash-preview"):
        if fallback not in candidatos:
            candidatos.append(fallback)

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": _construir_prompt(req)}],
            }
        ],
        "generationConfig": {
            "temperature": 0.65,
            "responseMimeType": "application/json",
        },
    }

    ultimo_erro = None
    async with httpx.AsyncClient(timeout=45.0) as client:
        for modelo in candidatos:
            url = f"{GEMINI_API_BASE}/{modelo}:generateContent"
            try:
                resp = await client.post(
                    url,
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "x-goog-api-key": api_key,
                    },
                )
                if resp.status_code in (404, 429, 503):
                    ultimo_erro = f"Modelo {modelo} temporariamente indisponível ({resp.status_code})."
                    continue
                if resp.status_code in (400, 401, 403):
                    raise RuntimeError(
                        f"Erro de autenticação ou permissão na API Gemini (HTTP {resp.status_code}). Verifique sua chave API."
                    )
                if resp.status_code >= 400:
                    ultimo_erro = f"Erro HTTP {resp.status_code} ao consultar {modelo}."
                    continue

                data = resp.json()
                candidates = data.get("candidates") or []
                if not candidates:
                    raise RuntimeError("A API Gemini não retornou candidatos de resposta.")
                parts = candidates[0].get("content", {}).get("parts") or []
                texto = "".join(
                    p.get("text", "") for p in parts if not p.get("thought")
                ).strip()
                if not texto:
                    raise RuntimeError("Resposta vazia recebida da API Gemini.")

                bruto = _extrair_json(texto)
                # Garante consistência dos campos obrigatórios de identificação
                bruto["etapa"] = req.etapa
                bruto["ano_serie"] = req.ano_serie
                bruto["componente"] = req.componente
                bruto["tema"] = req.tema
                bruto["duracao_minutos"] = req.duracao_minutos
                if req.ementa_texto and req.ementa_texto.strip():
                    bruto["ementa_utilizada"] = (
                        req.ementa_nome_arquivo.strip()
                        if req.ementa_nome_arquivo and req.ementa_nome_arquivo.strip()
                        else "Texto de ementa informado"
                    )
                else:
                    bruto["ementa_utilizada"] = None

                plano = LessonPlanData.model_validate(bruto)
                return plano, modelo
            except RuntimeError:
                raise
            except Exception as exc:
                ultimo_erro = f"Falha ao processar resposta de {modelo}: {type(exc).__name__}"

    raise RuntimeError(f"Não foi possível gerar o plano com a API Gemini: {ultimo_erro}")

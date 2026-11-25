from typing import List, Optional
from pydantic import BaseModel, Field


class LessonPlanRequest(BaseModel):
    etapa: str = Field(..., min_length=2, description="Etapa da Educação Básica")
    ano_serie: str = Field(..., min_length=1, description="Ano, série ou faixa etária")
    componente: str = Field(..., min_length=2, description="Componente curricular ou campo de experiência")
    tema: str = Field(..., min_length=3, max_length=200, description="Tema ou conteúdo central da aula")
    duracao_minutos: int = Field(50, ge=20, le=300, description="Duração total em minutos")
    metodologia: str = Field("Sugerida pela IA", description="Metodologia ativa ou tradicional desejada")
    recursos: List[str] = Field(default_factory=list, description="Recursos disponíveis na escola")
    contexto_turma: Optional[str] = Field(
        default="",
        max_length=600,
        description="Observações opcionais sobre perfil da turma, inclusão ou objetivos extras",
    )
    ementa_texto: Optional[str] = Field(
        default="",
        max_length=15000,
        description="Texto extraído ou colado da ementa / plano de ensino da disciplina",
    )
    ementa_nome_arquivo: Optional[str] = Field(
        default="",
        max_length=255,
        description="Nome do arquivo de ementa anexado, quando houver",
    )


class EmentaExtractResponse(BaseModel):
    nome_arquivo: str
    texto: str
    num_caracteres: int
    num_paginas: Optional[int] = None
    truncado: bool = False


class BnccSkill(BaseModel):
    codigo: str
    descricao: str


class TimelineStep(BaseModel):
    etapa: str
    duracao_minutos: int
    objetivo_etapa: str
    acao_professor: str
    acao_estudantes: str


class EvaluationSection(BaseModel):
    tipo: str
    instrumentos: List[str]
    criterios: List[str]


class PracticalActivity(BaseModel):
    titulo: str
    descricao: str
    passos: List[str]
    produto_esperado: str


class LessonPlanData(BaseModel):
    titulo: str
    etapa: str
    ano_serie: str
    componente: str
    tema: str
    duracao_minutos: int
    metodologia_escolhida: str
    resumo_pedagogico: str
    competencia_geral_bncc: str
    habilidades_bncc: List[BnccSkill]
    objetivo_geral: str
    objetivos_especificos: List[str]
    conhecimentos_previos: List[str]
    conteudos: List[str]
    cronograma: List[TimelineStep]
    estrategias_didaticas: List[str]
    recursos_didaticos: List[str]
    atividade_pratica: PracticalActivity
    avaliacao: EvaluationSection
    inclusao_diferenciacao: str
    referencias: List[str]
    ementa_utilizada: Optional[str] = None


class LessonPlanResponse(BaseModel):
    modo: str = Field(..., description="'gemini' ou 'demo'")
    modelo: str = Field(..., description="Nome do modelo utilizado")
    aviso: Optional[str] = Field(default=None, description="Mensagem informativa quando em modo demo ou fallback")
    plano: LessonPlanData


class HealthResponse(BaseModel):
    status: str
    gemini_configurado_servidor: bool
    modelo_padrao: str

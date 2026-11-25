"""Gerador pedagógico local (Modo Demonstração) quando a chave Gemini não estiver configurada."""

from .bncc_data import COMPETENCIAS_GERAIS_BNCC, HABILIDADES_REFERENCIA
from .schemas import (
    BnccSkill,
    EvaluationSection,
    LessonPlanData,
    LessonPlanRequest,
    PracticalActivity,
    TimelineStep,
)


def _distribuir_tempo(duracao_total: int) -> tuple[int, int, int, int]:
    """Divide a duração total da aula em 4 blocos cuja soma é exata."""
    t1 = max(5, round(duracao_total * 0.15))
    t2 = max(10, round(duracao_total * 0.35))
    t3 = max(10, round(duracao_total * 0.35))
    t4 = duracao_total - (t1 + t2 + t3)
    if t4 < 5:
        ajuste = 5 - t4
        t2 = max(5, t2 - ajuste)
        t4 = duracao_total - (t1 + t2 + t3)
    return t1, t2, t3, t4


def _selecionar_habilidades(req: LessonPlanRequest) -> list[BnccSkill]:
    chave = (req.etapa, req.componente)
    if chave in HABILIDADES_REFERENCIA:
        return [BnccSkill(codigo=c, descricao=d) for c, d in HABILIDADES_REFERENCIA[chave]]

    prefixos = {
        "Educação Infantil": ("EI03EO03", "Ampliar as relações interpessoais e explorar vivências ligadas ao tema proposto com ludicidade e cooperação."),
        "Ensino Fundamental – Anos Iniciais": ("EF15LP09", f"Expressar-se e construir sentidos sobre '{req.tema}' integrando leitura, oralidade e vivências cotidianas."),
        "Ensino Fundamental – Anos Finais": ("EF69AR01", f"Investigar, analisar e relacionar conceitos essenciais de '{req.tema}' em situações-problema do cotidiano."),
        "Ensino Médio": ("EM13CHS101", f"Analisar criticamente fontes, dados e contextos relacionados a '{req.tema}', formulando argumentos consistentes."),
    }
    cod, desc = prefixos.get(
        req.etapa,
        ("BNCC-REF", f"Desenvolver competências de investigação, compreensão e aplicação crítica acerca de '{req.tema}'."),
    )
    return [BnccSkill(codigo=cod, descricao=desc)]


def _escolher_metodologia(req: LessonPlanRequest) -> str:
    if req.metodologia and req.metodologia != "Sugerida pela IA":
        return req.metodologia
    if req.etapa == "Educação Infantil":
        return "Roda de Conversa e Ludicidade"
    if req.etapa == "Ensino Médio":
        return "Aprendizagem Baseada em Problemas (ABP)"
    return "Aula Expositiva Dialogada com Prática Colaborativa"


def gerar_plano_demonstracao(req: LessonPlanRequest) -> LessonPlanData:
    """Monta um plano de aula estruturado e coerente com os parâmetros enviados."""
    t1, t2, t3, t4 = _distribuir_tempo(req.duracao_minutos)
    metodologia = _escolher_metodologia(req)
    habilidades = _selecionar_habilidades(req)
    recursos = req.recursos if req.recursos else [
        "Quadro e pincel/giz",
        "Folhas sulfite e lápis/canetas",
        "Material de apoio preparado pelo professor",
    ]
    eh_infantil = req.etapa == "Educação Infantil"

    competencia = (
        COMPETENCIAS_GERAIS_BNCC[2]
        if eh_infantil
        else COMPETENCIAS_GERAIS_BNCC[1]
    )

    nota_contexto = (
        f" Considerando o contexto informado da turma ({req.contexto_turma.strip()}), "
        "o ritmo das intervenções foi planejado com checagens intermediárias e apoio mediado."
        if req.contexto_turma and req.contexto_turma.strip()
        else ""
    )

    ementa_limpa = (req.ementa_texto or "").strip()
    ementa_rotulo = None
    topicos_ementa: list[str] = []
    if ementa_limpa:
        ementa_rotulo = (
            req.ementa_nome_arquivo.strip()
            if req.ementa_nome_arquivo and req.ementa_nome_arquivo.strip()
            else "Texto de ementa informado"
        )
        linhas_uteis = [
            linha.strip(" -•*\t")
            for linha in ementa_limpa.splitlines()
            if len(linha.strip()) >= 8
        ]
        topicos_ementa = [l[:140] for l in linhas_uteis[:3]]
        nota_contexto += f" O planejamento também foi alinhado à ementa anexada ({ementa_rotulo})."

    if eh_infantil:
        titulo = f"Descobrindo e Brincando: {req.tema}"
        atividade = PracticalActivity(
            titulo=f"Estação Lúdica: Explorando {req.tema}",
            descricao=(
                f"Experiência sensorial e expressiva em pequenos grupos onde as crianças exploram "
                f"'{req.tema}' por meio de brincadeira orientada, manipulação de materiais e narrativa coletiva."
            ),
            passos=[
                "Organizar o espaço em roda e apresentar um objeto ou imagem disparadora ligada ao tema.",
                "Convidar as crianças a explorar os materiais disponíveis livremente, observando cores, formas ou ações.",
                "Mediar pequenas descobertas com perguntas abertas ('O que acontece se...?', 'Como você percebeu isso?').",
                "Registrar as produções (desenho, colagem ou relato oral) em um mural coletivo da sala.",
            ],
            produto_esperado="Mural coletivo ou registro expressivo das descobertas das crianças sobre o tema.",
        )
        avaliacao = EvaluationSection(
            tipo="Avaliação Formativa e Processual (Observação e Registro)",
            instrumentos=[
                "Diário de bordo do professor",
                "Registros fotográficos e produções das crianças",
                "Escuta atenta durante a roda final",
            ],
            criterios=[
                "Engajamento e curiosidade durante a exploração proposta",
                "Interação respeitosa e cooperação com os colegas",
                "Expressão de ideias, gestos ou relatos relacionados à vivência",
            ],
        )
    else:
        titulo = f"{req.componente} em Prática: {req.tema}"
        atividade = PracticalActivity(
            titulo=f"Desafio Aplicado sobre {req.tema}",
            descricao=(
                f"Atividade colaborativa em duplas ou trios utilizando {metodologia} para aplicar os conceitos "
                f"de '{req.tema}' a uma situação real próxima da vivência dos estudantes do {req.ano_serie}."
            ),
            passos=[
                f"Dividir a turma em pequenos grupos e apresentar uma situação-problema concreta envolvendo '{req.tema}'.",
                "Orientar a análise das informações principais com apoio dos recursos disponíveis em sala.",
                "Solicitar que cada grupo elabore uma solução, esquema visual ou síntese argumentada.",
                "Promover a socialização rápida de 2 ou 3 grupos com mediação e feedback coletivo.",
            ],
            produto_esperado=(
                f"Síntese visual (mapa conceitual, resolução comentada ou miniprojeto) demonstrando compreensão prática de '{req.tema}'."
            ),
        )
        avaliacao = EvaluationSection(
            tipo="Avaliação Diagnóstica e Formativa",
            instrumentos=[
                "Sondagem inicial oral (levantamento de conhecimentos prévios)",
                "Rubrica simples de acompanhamento da atividade prática",
                "Bilhete de saída (exit ticket) com 1 aprendizado e 1 dúvida",
            ],
            criterios=[
                f"Compreensão dos conceitos fundamentais relacionados a '{req.tema}'",
                "Capacidade de aplicar o conteúdo na atividade prática proposta",
                "Participação ativa, clareza na argumentação e colaboração em grupo",
            ],
        )

    cronograma = [
        TimelineStep(
            etapa="1. Acolhimento e Problematização Inicial",
            duracao_minutos=t1,
            objetivo_etapa="Engajar a turma, ativar conhecimentos prévios e conectar o tema à realidade dos alunos.",
            acao_professor=(
                f"Apresentar uma pergunta disparadora ou situação cotidiana sobre '{req.tema}' e registrar no quadro "
                "as hipóteses levantadas pela turma."
            ),
            acao_estudantes=(
                "Compartilhar experiências anteriores, responder à provocação inicial e levantar dúvidas sobre o assunto."
            ),
        ),
        TimelineStep(
            etapa="2. Desenvolvimento e Construção Conceitual",
            duracao_minutos=t2,
            objetivo_etapa=f"Apresentar e aprofundar os fundamentos de '{req.tema}' por meio de {metodologia}.",
            acao_professor=(
                f"Conduzir a explicação dialogada de '{req.tema}', utilizando exemplos concretos adequados ao {req.ano_serie} "
                "e verificando a compreensão com pausas para perguntas."
            ),
            acao_estudantes=(
                "Observar os exemplos, fazer anotações ou conexões guiadas, formular perguntas e participar da construção coletiva."
            ),
        ),
        TimelineStep(
            etapa="3. Prática Guiada e Mão na Massa",
            duracao_minutos=t3,
            objetivo_etapa="Consolidar a aprendizagem por meio de aplicação ativa e colaborativa.",
            acao_professor=(
                "Propor a atividade prática, circular entre os estudantes oferecendo mediação individualizada "
                "e incentivar diferentes estratégias de resolução."
            ),
            acao_estudantes=(
                "Executar a atividade proposta em grupo ou individualmente, discutir caminhos possíveis e registrar resultados."
            ),
        ),
        TimelineStep(
            etapa="4. Socialização, Sistematização e Fechamento",
            duracao_minutos=t4,
            objetivo_etapa="Revisar os pontos-chave, corrigir concepções equivocadas e avaliar o alcance dos objetivos.",
            acao_professor=(
                "Mediar a apresentação breve das descobertas, sintetizar os conceitos centrais no quadro e aplicar "
                "o fechamento avaliativo (roda de síntese ou bilhete de saída)."
            ),
            acao_estudantes=(
                "Apresentar conclusões, comparar ideias com os colegas e registrar o principal aprendizado da aula."
            ),
        ),
    ]

    return LessonPlanData(
        titulo=titulo,
        etapa=req.etapa,
        ano_serie=req.ano_serie,
        componente=req.componente,
        tema=req.tema,
        duracao_minutos=req.duracao_minutos,
        metodologia_escolhida=metodologia,
        resumo_pedagogico=(
            f"Plano de aula estruturado para {req.ano_serie} ({req.etapa}) no componente {req.componente}, "
            f"dedicado ao tema '{req.tema}' em {req.duracao_minutos} minutos, aplicando {metodologia} "
            f"com foco no protagonismo estudantil e alinhamento à BNCC.{nota_contexto}"
        ),
        competencia_geral_bncc=competencia,
        habilidades_bncc=habilidades,
        objetivo_geral=(
            f"Compreender e aplicar os aspectos fundamentais de '{req.tema}' no contexto de {req.componente}, "
            f"desenvolvendo autonomia, pensamento crítico e participação ativa compatíveis com o {req.ano_serie}."
        ),
        objetivos_especificos=[
            f"Identificar os conceitos e elementos essenciais envolvidos em '{req.tema}'.",
            f"Relacionar '{req.tema}' a situações concretas do cotidiano dos estudantes.",
            "Participar de atividade colaborativa propondo explicações, registros ou soluções fundamentadas.",
        ],
        conhecimentos_previos=[
            f"Noções introdutórias de {req.componente} trabalhadas em aulas anteriores.",
            "Vivências cotidianas dos alunos que se conectam diretamente ao tema.",
            "Habilidades básicas de escuta ativa, leitura/observação e trabalho em grupo.",
        ],
        conteudos=[
            f"Conceitos centrais de {req.tema}",
            f"Aplicações práticas e contextualização em {req.componente}",
            *(
                [f"Tópico da ementa: {t}" for t in topicos_ementa]
                if topicos_ementa
                else ["Síntese, argumentação e registro das aprendizagens"]
            ),
        ],
        cronograma=cronograma,
        estrategias_didaticas=[
            f"Uso de {metodologia} para manter a turma ativa durante todo o percurso da aula.",
            "Perguntas norteadoras graduais (do concreto para o abstrato) para ampliar a participação.",
            "Feedback formativo imediato durante a etapa prática para sanar dúvidas em tempo real.",
        ],
        recursos_didaticos=recursos,
        atividade_pratica=atividade,
        avaliacao=avaliacao,
        inclusao_diferenciacao=(
            "Oferecer instruções curtas e também visuais (no quadro ou cartões), permitir respostas por múltiplas "
            "linguagens (oral, escrita ou desenho/esquema), organizar duplas heterogêneas de apoio mútuo e disponibilizar "
            "tempo flexível ou um desafio extra para estudantes que concluírem antes."
        ),
        referencias=[
            "BRASIL. Ministério da Educação. Base Nacional Comum Curricular (BNCC). Brasília: MEC, 2018.",
            *(
                [f"Ementa / Plano de Ensino da disciplina ({ementa_rotulo})."]
                if ementa_rotulo
                else []
            ),
            f"Livro didático adotado pela escola para {req.componente} — {req.ano_serie}.",
            "BACICH, Lilian; MORAN, José (org.). Metodologias ativas para uma educação inovadora. Porto Alegre: Penso, 2018.",
        ],
        ementa_utilizada=ementa_rotulo,
    )

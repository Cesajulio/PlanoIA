"""Catálogo curricular de referência alinhado à BNCC (Educação Básica)."""

ETAPAS_CURRICULO = {
    "Educação Infantil": {
        "anos": [
            "Bebês (0 a 1 ano e 6 meses)",
            "Crianças bem pequenas (1 ano e 7 meses a 3 anos e 11 meses)",
            "Crianças pequenas (4 anos a 5 anos e 11 meses)",
        ],
        "componentes": [
            "O eu, o outro e o nós",
            "Corpo, gestos e movimentos",
            "Traços, sons, cores e formas",
            "Escuta, fala, pensamento e imaginação",
            "Espaços, tempos, quantidades, relações e transformações",
        ],
    },
    "Ensino Fundamental – Anos Iniciais": {
        "anos": ["1º ano", "2º ano", "3º ano", "4º ano", "5º ano"],
        "componentes": [
            "Língua Portuguesa",
            "Matemática",
            "Ciências",
            "História",
            "Geografia",
            "Arte",
            "Educação Física",
            "Ensino Religioso",
        ],
    },
    "Ensino Fundamental – Anos Finais": {
        "anos": ["6º ano", "7º ano", "8º ano", "9º ano"],
        "componentes": [
            "Língua Portuguesa",
            "Matemática",
            "Ciências",
            "História",
            "Geografia",
            "Língua Inglesa",
            "Arte",
            "Educação Física",
            "Ensino Religioso",
        ],
    },
    "Ensino Médio": {
        "anos": ["1ª série", "2ª série", "3ª série"],
        "componentes": [
            "Língua Portuguesa",
            "Matemática",
            "Física",
            "Química",
            "Biologia",
            "História",
            "Geografia",
            "Filosofia",
            "Sociologia",
            "Língua Inglesa",
            "Arte",
            "Educação Física",
            "Projeto de Vida / Itinerário Formativo",
        ],
    },
}

METODOLOGIAS = [
    "Sugerida pela IA",
    "Aula Expositiva Dialogada",
    "Aprendizagem Baseada em Problemas (ABP)",
    "Gamificação",
    "Sala de Aula Invertida",
    "Rotação por Estações",
    "Aprendizagem Baseada em Projetos (Mão na Massa)",
    "Roda de Conversa e Ludicidade",
]

RECURSOS_PADRAO = [
    "Quadro e pincel/giz",
    "Projetor multimídia ou TV",
    "Material impresso / folhas sulfite",
    "Laboratório de informática",
    "Celulares ou tablets",
    "Materiais concretos / recicláveis",
    "Livros didáticos / biblioteca",
]

COMPETENCIAS_GERAIS_BNCC = [
    "Competência Geral 1 (Conhecimento): Valorizar e utilizar os conhecimentos historicamente construídos sobre o mundo físico, social, cultural e digital.",
    "Competência Geral 2 (Pensamento Científico, Crítico e Criativo): Exercitar a curiosidade intelectual e recorrer à abordagem própria das ciências, incluindo investigação, reflexão, análise crítica, imaginação e criatividade.",
    "Competência Geral 4 (Comunicação): Utilizar diferentes linguagens – verbal, corporal, visual, sonora e digital – para se expressar e partilhar informações, experiências, ideias e sentimentos.",
    "Competência Geral 5 (Cultura Digital): Compreender, utilizar e criar tecnologias digitais de informação e comunicação de forma crítica, significativa, reflexiva e ética.",
    "Competência Geral 7 (Argumentação): Argumentar com base em fatos, dados e informações confiáveis, para formular, negociar e defender ideias, pontos de vista e decisões comuns.",
    "Competência Geral 9 (Empatia e Cooperação): Exercitar a empatia, o diálogo, a resolução de conflitos e a cooperação, fazendo-se respeitar e promovendo o respeito ao outro.",
    "Competência Geral 10 (Responsabilidade e Cidadania): Agir pessoal e coletivamente com autonomia, responsabilidade, flexibilidade, resiliência e determinação.",
]

# Habilidades reais da BNCC utilizadas como referência no Modo Demonstração
HABILIDADES_REFERENCIA = {
    ("Educação Infantil", "O eu, o outro e o nós"): [
        ("EI03EO03", "Ampliar as relações interpessoais, desenvolvendo atitudes de participação e cooperação."),
        ("EI03EO04", "Comunicar suas ideias e sentimentos a pessoas e grupos diversos."),
    ],
    ("Educação Infantil", "Corpo, gestos e movimentos"): [
        ("EI03CG01", "Criar com o corpo formas diversificadas de expressão de sentimentos, sensações e emoções, tanto nas situações do cotidiano quanto em brincadeiras, dança, teatro e música."),
        ("EI03CG02", "Demonstrar controle e adequação do uso de seu corpo em brincadeiras e jogos, escuta e reconto de histórias, atividades artísticas, entre outras possibilidades."),
    ],
    ("Educação Infantil", "Traços, sons, cores e formas"): [
        ("EI03TS02", "Expressar-se livremente por meio de desenho, pintura, colagem, dobradura e escultura, criando produções bidimensionais e tridimensionais."),
        ("EI03TS01", "Utilizar sons produzidos por materiais, objetos e instrumentos musicais durante brincadeiras de faz de conta, encenações, criações musicais e festas."),
    ],
    ("Educação Infantil", "Escuta, fala, pensamento e imaginação"): [
        ("EI03EF01", "Expressar ideias, desejos e sentimentos sobre suas vivências, por meio da linguagem oral e escrita (escrita espontânea), de fotos, desenhos e outras formas de expressão."),
        ("EI03EF04", "Recontar histórias ouvidas e planejar coletivamente roteiros de vídeos e de encenações, definindo os contextos, os personagens e a estrutura da história."),
    ],
    ("Educação Infantil", "Espaços, tempos, quantidades, relações e transformações"): [
        ("EI03ET01", "Estabelecer relações de comparação entre objetos, observando suas propriedades."),
        ("EI03ET03", "Identificar e selecionar fontes de informações, para responder a questões sobre a natureza, seus fenômenos, sua conservação."),
    ],
    ("Ensino Fundamental – Anos Iniciais", "Língua Portuguesa"): [
        ("EF15LP02", "Estabelecer expectativas em relação ao texto que vai ler, apoiando-se em seus conhecimentos prévios sobre as condições de produção e recepção desse texto."),
        ("EF15LP09", "Expressar-se em situações de intercâmbio oral com clareza, preocupando-se em ser compreendido pelo interlocutor."),
    ],
    ("Ensino Fundamental – Anos Iniciais", "Matemática"): [
        ("EF04MA03", "Resolver e elaborar problemas com números naturais envolvendo adição e subtração, utilizando estratégias diversas, como cálculo, cálculo mental e algoritmos."),
        ("EF05MA07", "Resolver e elaborar problemas de adição e subtração com números naturais e com números racionais, cuja representação decimal seja finita."),
    ],
    ("Ensino Fundamental – Anos Iniciais", "Ciências"): [
        ("EF04CI04", "Analisar e construir cadeias alimentares simples, reconhecendo a posição ocupada pelos seres vivos nessas cadeias e o papel do Sol como fonte primária de energia."),
        ("EF05CI02", "Aplicar os conhecimentos sobre as mudanças de estado físico da água para explicar o ciclo hidrológico e analisar suas implicações na agricultura, no clima e na geração de energia."),
    ],
    ("Ensino Fundamental – Anos Iniciais", "História"): [
        ("EF04HI01", "Reconhecer a história como resultado da ação do ser humano no tempo e no espaço, com base na identificação de mudanças e permanências ao longo do tempo."),
        ("EF05HI04", "Associar a noção de cidadania com os princípios de respeito à diversidade, à pluralidade e aos direitos humanos."),
    ],
    ("Ensino Fundamental – Anos Iniciais", "Geografia"): [
        ("EF04GE09", "Utilizar as direções cardeais na localização de componentes físicos e humanos nas paisagens rurais e urbanas."),
        ("EF05GE11", "Identificar e descrever problemas ambientais que ocorrem no entorno da escola e da residência, propondo soluções para esses problemas."),
    ],
    ("Ensino Fundamental – Anos Finais", "Língua Portuguesa"): [
        ("EF69LP03", "Identificar, em notícias, o fato central, suas principais circunstâncias e eventuais decorrências, articulando diferentes fontes e pontos de vista."),
        ("EF69LP07", "Produzir textos em diferentes gêneros, considerando sua adequação ao contexto de produção e circulação."),
    ],
    ("Ensino Fundamental – Anos Finais", "Matemática"): [
        ("EF07MA18", "Resolver e elaborar problemas que possam ser representados por equações polinomiais de 1º grau, redutíveis à forma ax + b = c, fazendo uso das propriedades da igualdade."),
        ("EF08MA04", "Resolver e elaborar problemas envolvendo cálculo de porcentagens, incluindo o uso de tecnologias digitais."),
    ],
    ("Ensino Fundamental – Anos Finais", "Ciências"): [
        ("EF07CI07", "Caracterizar os principais ecossistemas brasileiros quanto à paisagem, à quantidade de água, ao tipo de solo, à disponibilidade de luz solar, à temperatura etc."),
        ("EF08CI01", "Identificar e classificar diferentes fontes (renováveis e não renováveis) e tipos de energia utilizados em residências, comunidades ou cidades."),
    ],
    ("Ensino Fundamental – Anos Finais", "História"): [
        ("EF07HI01", "Explicar o significado de 'modernidade' e suas lógicas de inclusão e exclusão, com base em uma concepção europeia."),
        ("EF08HI19", "Formular questionamentos sobre o legado da escravidão nas Américas, com base na seleção e consulta de fontes de diferentes naturezas."),
    ],
    ("Ensino Fundamental – Anos Finais", "Geografia"): [
        ("EF07GE06", "Discutir em que medida a produção, a circulação e o consumo de mercadorias provocam impactos ambientais, assim como influem na distribuição de riquezas."),
        ("EF08GE05", "Aplicar os conceitos de Estado, nação, território, governo e país para o entendimento de conflitos e tensões na contemporaneidade."),
    ],
    ("Ensino Médio", "Língua Portuguesa"): [
        ("EM13LP01", "Relacionar o texto, tanto na produção como na leitura/escuta, com suas condições de produção e seu contexto sócio-histórico de circulação."),
        ("EM13LP05", "Analisar, em textos argumentativos, os posicionamentos assumidos, os movimentos argumentativos e os argumentos utilizados para sustentá-los."),
    ],
    ("Ensino Médio", "Matemática"): [
        ("EM13MAT302", "Construir modelos empregando as funções polinomiais de 1º ou 2º graus, para resolver problemas em contextos diversos, com ou sem apoio de tecnologias digitais."),
        ("EM13MAT316", "Resolver e elaborar problemas, em diferentes contextos, que envolvem cálculo e interpretação das medidas de tendência central e de dispersão."),
    ],
    ("Ensino Médio", "Física"): [
        ("EM13CNT101", "Analisar e representar, com ou sem o uso de dispositivos e de aplicativos digitais específicos, as transformações e conservações em sistemas que envolvam quantidade de matéria, de energia e de movimento."),
        ("EM13CNT301", "Construir questões, elaborar hipóteses, previsões e estimativas, empregar instrumentos de medição e representar e interpretar modelos explicativos, dados e/ou resultados experimentais."),
    ],
    ("Ensino Médio", "Química"): [
        ("EM13CNT104", "Avaliar os benefícios e os riscos à saúde e ao ambiente, considerando a composição, a toxicidade e a reatividade de diferentes materiais e produtos."),
        ("EM13CNT203", "Avaliar e prever efeitos de intervenções nos ecossistemas, e seus impactos nos seres vivos e no corpo humano, com base nos mecanismos de manutenção da vida."),
    ],
    ("Ensino Médio", "Biologia"): [
        ("EM13CNT202", "Analisar as diversas formas de manifestação da vida em seus diferentes níveis de organização, bem como as condições ambientais favoráveis e os fatores limitantes a elas."),
        ("EM13CNT303", "Interpretar textos de divulgação científica que tratem de temáticas das Ciências da Natureza, disponíveis em diferentes mídias."),
    ],
    ("Ensino Médio", "História"): [
        ("EM13CHS101", "Identificar, analisar e comparar diferentes fontes e narrativas expressas em diversas linguagens, com vistas à compreensão de ideias filosóficas e de processos e eventos históricos."),
        ("EM13CHS102", "Identificar, analisar e discutir as circunstâncias históricas, geográficas, políticas, econômicas, sociais, ambientais e culturais de matrizes conceituais."),
    ],
    ("Ensino Médio", "Geografia"): [
        ("EM13CHS201", "Analisar e caracterizar as dinâmicas das populações, das mercadorias e do capital nos diversos continentes, com destaque para a mobilidade e a fixação de pessoas."),
        ("EM13CHS301", "Problematizar hábitos e práticas individuais e coletivos de produção, reaproveitamento e descarte de resíduos em metrópoles, áreas urbanas e rurais."),
    ],
}

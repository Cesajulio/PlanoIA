# PlanoIA — IA para Planejamento de Aulas (BNCC)

Aplicação web desenvolvida para **Projeto de Extensão Universitária** com o objetivo de apoiar professores da **Educação Básica** (Educação Infantil, Ensino Fundamental e Ensino Médio) na criação de planos de aula completos, práticos e alinhados à **Base Nacional Comum Curricular (BNCC)**.

## Funcionalidades

- **Alinhamento Curricular à BNCC**: seleção dinâmica de etapa, ano/série/faixa etária e componente curricular (ou Campo de Experiência na Educação Infantil), retornando competências gerais e códigos/habilidades da BNCC.
- **Plano de Aula Completo**:
  - Identificação e resumo pedagógico;
  - Competência Geral e Habilidades da BNCC;
  - Objetivo Geral e Objetivos Específicos;
  - Conteúdos e Conhecimentos Prévios;
  - Cronograma passo a passo com distribuição exata dos minutos (Ação do Professor vs. Ação dos Estudantes);
  - Atividade prática sugerida adaptada aos recursos disponíveis na escola;
  - Estratégias didáticas, recursos, avaliação (tipo, instrumentos e critérios);
  - Orientações de inclusão e diferenciação pedagógica;
  - Referências.
- **Integração com Google Gemini API + Modo Demonstração Local**:
  - Funciona imediatamente mesmo sem chave de API (usando o gerador pedagógico local com catálogo real da BNCC).
  - Basta inserir uma chave gratuita da **Google Gemini API** (no arquivo `.env` ou pelo botão **Chave Gemini** na própria interface) para ativar a IA generativa completa.
- **Exportação e Produtividade**:
  - Impressão / Exportação direta em **PDF** com layout limpo (`@media print`);
  - Cópia rápida para Word/Google Docs e download em **Markdown (`.md`)**;
  - **Exemplos rápidos** (1 clique) para demonstrações e oficinas com professores;
  - **Histórico local** automático no navegador (`localStorage`).

## Estrutura do Projeto

```text
Ia_Projeto_extensao/
├── backend/
│   ├── main.py             # Servidor FastAPI e rotas da API
│   ├── schemas.py          # Modelos Pydantic de entrada e saída
│   ├── gemini_service.py   # Integração com a Google Gemini API (JSON estruturado)
│   ├── demo_generator.py   # Gerador local de demonstração (BNCC)
│   └── bncc_data.py        # Catálogo curricular de etapas, componentes e habilidades BNCC
├── frontend/
│   ├── index.html          # Interface web principal
│   ├── styles.css          # Estilo responsivo e layout de impressão PDF
│   └── app.js              # Interatividade, chamadas à API, histórico e exportação
├── .env.example            # Modelo de variáveis de ambiente
├── requirements.txt        # Dependências Python
├── iniciar.bat             # Inicialização rápida no Windows (1 clique)
└── README.md
```

## Como Executar

### Opção 1 — Rápida no Windows
Dê um duplo clique no arquivo **`iniciar.bat`**. Ele criará o ambiente virtual, instalará as dependências e abrirá o navegador automaticamente em `http://localhost:8000`.

### Opção 2 — Manual pelo Terminal (PowerShell)

```powershell
# 1. Criar e ativar ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Instalar dependências
pip install -r requirements.txt

# 3. (Opcional) Configurar sua chave do Google Gemini
copy .env.example .env
# Edite o arquivo .env e preencha GEMINI_API_KEY=sua_chave_aqui

# 4. Iniciar o servidor
uvicorn backend.main:app --reload --port 8000
```

Acesse no navegador:
- **Aplicação Web:** `http://localhost:8000`
- **Documentação interativa da API (Swagger):** `http://localhost:8000/docs`

## Como Obter a Chave Gratuita da Google Gemini API

1. Acesse [Google AI Studio — API Keys](https://aistudio.google.com/apikey) com uma conta Google.
2. Clique em **Create API key** e copie a chave gerada.
3. Você pode usá-la de duas formas:
   - **No servidor (permanente):** salve em `GEMINI_API_KEY=...` dentro do arquivo `.env` e reinicie o servidor;
   - **Na interface (rápido para apresentações):** clique no botão **Chave Gemini** no canto superior direito da tela e cole a chave na sessão atual.

## Como Hospedar na Vercel (Gratuito)

O projeto já está pronto para deploy na **Vercel** por meio de `api/index.py` e `vercel.json`.

1. Crie um repositório no **GitHub** e envie este projeto (o arquivo `.env` já está no `.gitignore`, portanto sua chave não será enviada).
2. Acesse [vercel.com](https://vercel.com), clique em **Add New → Project** e importe o repositório do GitHub.
3. Em **Environment Variables**, adicione:
   - `GEMINI_API_KEY` = sua chave do Google Gemini
   - `GEMINI_MODEL` = `gemini-3.5-flash`
4. Clique em **Deploy**. Ao concluir, a Vercel gerará o link público `https://seu-projeto.vercel.app`.
5. **Observação:** no plano gratuito da Vercel, arquivos de ementa anexados têm limite de até **4 MB** (o sistema já valida esse limite automaticamente quando roda na Vercel).

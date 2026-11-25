const STORAGE_KEY_HISTORY = "planoia_historico_v1";
const SESSION_KEY_GEMINI = "planoia_gemini_api_key";

let curriculumData = null;
let serverHasGeminiKey = false;
let serverDefaultModel = "gemini-3.5-flash";
let currentResult = null;
let attachedEmentaFilename = "";

const QUICK_EXAMPLES = {
  agua: {
    etapa: "Ensino Fundamental – Anos Iniciais",
    ano_serie: "5º ano",
    componente: "Ciências",
    tema: "O ciclo da água e a importância da preservação hídrica",
    duracao_minutos: 50,
    metodologia: "Aprendizagem Baseada em Problemas (ABP)",
    recursos: ["Quadro e pincel/giz", "Material impresso / folhas sulfite", "Projetor multimídia ou TV"],
    contexto_turma: "Turma curiosa com 26 alunos; conectar o tema com a economia de água em casa e na escola.",
  },
  equacoes: {
    etapa: "Ensino Fundamental – Anos Finais",
    ano_serie: "7º ano",
    componente: "Matemática",
    tema: "Equações do 1º grau aplicadas a compras e orçamento cotidiano",
    duracao_minutos: 100,
    metodologia: "Gamificação",
    recursos: ["Quadro e pincel/giz", "Material impresso / folhas sulfite"],
    contexto_turma: "Parte da turma tem dificuldade em traduzir problemas de texto para linguagem algébrica.",
  },
  infantil: {
    etapa: "Educação Infantil",
    ano_serie: "Crianças pequenas (4 anos a 5 anos e 11 meses)",
    componente: "Traços, sons, cores e formas",
    tema: "Cores, texturas e sons encontrados na natureza",
    duracao_minutos: 45,
    metodologia: "Roda de Conversa e Ludicidade",
    recursos: ["Materiais concretos / recicláveis", "Material impresso / folhas sulfite"],
    contexto_turma: "Turma de 18 crianças; aproveitar o pátio externo se possível.",
  },
  fakenews: {
    etapa: "Ensino Médio",
    ano_serie: "2ª série",
    componente: "Língua Portuguesa",
    tema: "Checagem de fatos, desinformação (Fake News) e argumentação crítica",
    duracao_minutos: 100,
    metodologia: "Rotação por Estações",
    recursos: ["Quadro e pincel/giz", "Projetor multimídia ou TV", "Celulares ou tablets"],
    contexto_turma: "Estudantes muito conectados às redes sociais; preparar também para a redação argumentativa.",
  },
};

// Elementos DOM
const elEtapa = document.getElementById("etapa");
const elAno = document.getElementById("ano_serie");
const elComponente = document.getElementById("componente");
const elTema = document.getElementById("tema");
const elDuracao = document.getElementById("duracao_minutos");
const elMetodologia = document.getElementById("metodologia");
const elRecursosContainer = document.getElementById("recursos-container");
const elEmentaDropzone = document.getElementById("ementa-dropzone");
const elEmentaDropzoneTitle = document.getElementById("ementa-dropzone-title");
const elEmentaFileInput = document.getElementById("ementa-file");
const elEmentaFileCard = document.getElementById("ementa-file-card");
const elEmentaFileName = document.getElementById("ementa-file-name");
const elEmentaFileMeta = document.getElementById("ementa-file-meta");
const elBtnToggleEmentaText = document.getElementById("btn-toggle-ementa-text");
const elBtnRemoveEmenta = document.getElementById("btn-remove-ementa");
const elBtnPasteEmenta = document.getElementById("btn-paste-ementa");
const elEmentaTextWrapper = document.getElementById("ementa-text-wrapper");
const elEmentaTexto = document.getElementById("ementa_texto");
const elContexto = document.getElementById("contexto_turma");
const elForm = document.getElementById("lesson-form");
const elFormError = document.getElementById("form-error");
const elBtnGenerate = document.getElementById("btn-generate");
const elBtnGenerateText = document.getElementById("btn-generate-text");

const elEmptyState = document.getElementById("empty-state");
const elLoadingState = document.getElementById("loading-state");
const elPlanOutput = document.getElementById("plan-output");
const elPlanDocument = document.getElementById("plan-document");
const elPlanModeBadge = document.getElementById("plan-mode-badge");
const elPlanNotice = document.getElementById("plan-notice");

const elStatusPill = document.getElementById("ai-status-pill");
const elStatusText = document.getElementById("ai-status-text");
const elHistoryCount = document.getElementById("history-count");
const elHistoryList = document.getElementById("history-list");
const elInputApiKey = document.getElementById("input-api-key");
const elToast = document.getElementById("toast");

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function showToast(message) {
  elToast.textContent = message;
  elToast.classList.remove("hidden");
  clearTimeout(showToast._timer);
  showToast._timer = setTimeout(() => {
    elToast.classList.add("hidden");
  }, 2800);
}

function getUserApiKey() {
  return (sessionStorage.getItem(SESSION_KEY_GEMINI) || "").trim();
}

function updateAiStatusUi() {
  const hasUserKey = Boolean(getUserApiKey());
  if (hasUserKey || serverHasGeminiKey) {
    elStatusPill.classList.remove("status-demo");
    elStatusPill.classList.add("status-gemini");
    elStatusText.textContent = hasUserKey
      ? `Gemini Ativo (Sessão)`
      : `Gemini Ativo (${serverDefaultModel})`;
  } else {
    elStatusPill.classList.remove("status-gemini");
    elStatusPill.classList.add("status-demo");
    elStatusText.textContent = "Modo Demonstração Local";
  }
}

function populateSelect(selectEl, items, selectedValue = null) {
  selectEl.innerHTML = "";
  items.forEach((item) => {
    const opt = document.createElement("option");
    opt.value = item;
    opt.textContent = item;
    if (selectedValue && selectedValue === item) {
      opt.selected = true;
    }
    selectEl.appendChild(opt);
  });
}

function updateStageDependentFields(selectedAno = null, selectedComp = null) {
  if (!curriculumData) return;
  const etapa = elEtapa.value;
  const config = curriculumData.etapas[etapa];
  if (!config) return;
  populateSelect(elAno, config.anos, selectedAno);
  populateSelect(elComponente, config.componentes, selectedComp);
}

function renderResourceChips(recursos, preselected = ["Quadro e pincel/giz", "Material impresso / folhas sulfite"]) {
  elRecursosContainer.innerHTML = "";
  recursos.forEach((recurso) => {
    const label = document.createElement("label");
    label.className = "resource-chip";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = recurso;
    if (preselected.includes(recurso)) {
      checkbox.checked = true;
      label.classList.add("selected");
    }
    checkbox.addEventListener("change", () => {
      label.classList.toggle("selected", checkbox.checked);
    });
    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(recurso));
    elRecursosContainer.appendChild(label);
  });
}

function setSelectedResources(selectedList) {
  const checkboxes = elRecursosContainer.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach((cb) => {
    const isChecked = selectedList.includes(cb.value);
    cb.checked = isChecked;
    cb.closest(".resource-chip").classList.toggle("selected", isChecked);
  });
}

function getSelectedResources() {
  return Array.from(elRecursosContainer.querySelectorAll('input[type="checkbox"]:checked')).map(
    (cb) => cb.value
  );
}

function syncDurationPresetButtons(minutes) {
  document.querySelectorAll(".preset-btn").forEach((btn) => {
    btn.classList.toggle("active", Number(btn.dataset.min) === Number(minutes));
  });
}

function applyExample(key) {
  const ex = QUICK_EXAMPLES[key];
  if (!ex || !curriculumData) return;
  elEtapa.value = ex.etapa;
  updateStageDependentFields(ex.ano_serie, ex.componente);
  elTema.value = ex.tema;
  elDuracao.value = ex.duracao_minutos;
  syncDurationPresetButtons(ex.duracao_minutos);
  elMetodologia.value = ex.metodologia;
  setSelectedResources(ex.recursos);
  elContexto.value = ex.contexto_turma;
  showToast("Exemplo preenchido! Clique em 'Gerar Plano de Aula'.");
}

// Histórico (localStorage)
function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY_HISTORY) || "[]");
  } catch {
    return [];
  }
}

function saveToHistory(responseObj) {
  const history = loadHistory();
  const entry = {
    id: `${Date.now()}`,
    criado_em: new Date().toLocaleString("pt-BR"),
    resultado: responseObj,
  };
  history.unshift(entry);
  const trimmed = history.slice(0, 15);
  localStorage.setItem(STORAGE_KEY_HISTORY, JSON.stringify(trimmed));
  updateHistoryBadge();
}

function updateHistoryBadge() {
  elHistoryCount.textContent = String(loadHistory().length);
}

function scrollToPlan(highlight = false) {
  requestAnimationFrame(() => {
    elPlanOutput.scrollIntoView({ behavior: "smooth", block: "start" });
    if (highlight) {
      elPlanDocument.classList.remove("plan-flash");
      void elPlanDocument.offsetWidth;
      elPlanDocument.classList.add("plan-flash");
    }
  });
}

function openHistoryPlan(item) {
  if (!item || !item.resultado || !item.resultado.plano) {
    showToast("Este registro do histórico está incompleto.");
    return;
  }
  closeModal("modal-history");
  renderLessonPlan(item.resultado);
  scrollToPlan(true);
  showToast("Plano carregado do histórico.");
}

function renderHistoryModal() {
  const history = loadHistory();
  if (!history.length) {
    elHistoryList.innerHTML =
      '<p class="modal-text">Nenhum plano salvo ainda. Os planos que você gerar aparecerão aqui automaticamente.</p>';
    return;
  }

  elHistoryList.innerHTML = "";
  history.forEach((item) => {
    const p = item?.resultado?.plano;
    if (!p) return;
    const row = document.createElement("div");
    row.className = "history-item";
    row.innerHTML = `
      <div class="history-info">
        <strong>${escapeHtml(p.titulo)}</strong>
        <span>${escapeHtml(p.etapa)} • ${escapeHtml(p.ano_serie)} • ${escapeHtml(p.componente)} • ${escapeHtml(p.duracao_minutos)} min • ${escapeHtml(item.criado_em)}</span>
      </div>
      <button type="button" class="btn btn-outline btn-sm">Abrir</button>
    `;
    row.querySelector(".history-info").addEventListener("click", () => openHistoryPlan(item));
    row.querySelector("button").addEventListener("click", (e) => {
      e.stopPropagation();
      openHistoryPlan(item);
    });
    elHistoryList.appendChild(row);
  });
}

// Renderização do Plano de Aula
function renderLessonPlan(result) {
  currentResult = result;
  const p = result.plano;

  elEmptyState.classList.add("hidden");
  elLoadingState.classList.add("hidden");
  elPlanOutput.classList.remove("hidden");

  if (result.modo === "gemini") {
    elPlanModeBadge.className = "mode-badge gemini";
    elPlanModeBadge.textContent = `Gerado com Google Gemini (${result.modelo})`;
  } else {
    elPlanModeBadge.className = "mode-badge demo";
    elPlanModeBadge.textContent = "Modo Demonstração Local (BNCC)";
  }

  if (result.aviso) {
    elPlanNotice.textContent = result.aviso;
    elPlanNotice.classList.remove("hidden");
  } else {
    elPlanNotice.classList.add("hidden");
  }

  const somaMinutos = (p.cronograma || []).reduce((acc, s) => acc + Number(s.duracao_minutos || 0), 0);

  const habilidadesHtml = (p.habilidades_bncc || [])
    .map(
      (h) => `
      <div class="bncc-item">
        <span class="bncc-code">${escapeHtml(h.codigo)}</span>
        <span class="bncc-desc">${escapeHtml(h.descricao)}</span>
      </div>`
    )
    .join("");

  const cronogramaHtml = (p.cronograma || [])
    .map(
      (step) => `
      <div class="timeline-card">
        <div class="timeline-head">
          <h4>${escapeHtml(step.etapa)}</h4>
          <span class="time-pill">${escapeHtml(step.duracao_minutos)} min</span>
        </div>
        <p class="timeline-objective"><strong>Objetivo:</strong> ${escapeHtml(step.objetivo_etapa)}</p>
        <div class="roles-grid">
          <div class="role-box role-prof">
            <strong>Ação do Professor</strong>
            ${escapeHtml(step.acao_professor)}
          </div>
          <div class="role-box role-student">
            <strong>Ação dos Estudantes</strong>
            ${escapeHtml(step.acao_estudantes)}
          </div>
        </div>
      </div>`
    )
    .join("");

  const toList = (items) =>
    (items || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("");

  const atividade = p.atividade_pratica || {
    titulo: "",
    descricao: "",
    passos: [],
    produto_esperado: "",
  };
  const avaliacao = p.avaliacao || {
    tipo: "",
    instrumentos: [],
    criterios: [],
  };
  const ementaTagHtml = p.ementa_utilizada
    ? `<span class="meta-tag meta-tag-ementa"><strong>Ementa:</strong> ${escapeHtml(p.ementa_utilizada)}</span>`
    : "";

  elPlanDocument.innerHTML = `
    <div class="doc-hero">
      <div class="doc-kicker">Plano de Aula • Alinhado à BNCC</div>
      <h2 class="doc-title">${escapeHtml(p.titulo)}</h2>
      <div class="doc-meta-grid">
        <span class="meta-tag"><strong>Etapa:</strong> ${escapeHtml(p.etapa)}</span>
        <span class="meta-tag"><strong>Ano/Série:</strong> ${escapeHtml(p.ano_serie)}</span>
        <span class="meta-tag"><strong>Componente:</strong> ${escapeHtml(p.componente)}</span>
        <span class="meta-tag"><strong>Duração:</strong> ${escapeHtml(p.duracao_minutos)} min</span>
        <span class="meta-tag"><strong>Metodologia:</strong> ${escapeHtml(p.metodologia_escolhida)}</span>
        ${ementaTagHtml}
      </div>
      <p class="doc-summary">${escapeHtml(p.resumo_pedagogico)}</p>
    </div>

    <section class="doc-section">
      <h3 class="section-title">1. Alinhamento à BNCC</h3>
      <div class="bncc-competencia">
        <strong>Competência Geral:</strong> ${escapeHtml(p.competencia_geral_bncc)}
      </div>
      <div class="bncc-list">${habilidadesHtml}</div>
    </section>

    <section class="doc-section">
      <h3 class="section-title">2. Objetivos de Aprendizagem</h3>
      <div class="objetivo-geral-box">
        <p class="sub-label">Objetivo Geral</p>
        ${escapeHtml(p.objetivo_geral)}
      </div>
      <p class="sub-label">Objetivos Específicos</p>
      <ul class="clean-list">${toList(p.objetivos_especificos)}</ul>
    </section>

    <section class="doc-section">
      <h3 class="section-title">3. Conteúdos e Conhecimentos Prévios</h3>
      <div class="two-col-grid">
        <div>
          <p class="sub-label">Conteúdos Abordados</p>
          <ul class="clean-list">${toList(p.conteudos)}</ul>
        </div>
        <div>
          <p class="sub-label">Conhecimentos Prévios</p>
          <ul class="clean-list">${toList(p.conhecimentos_previos)}</ul>
        </div>
      </div>
    </section>

    <section class="doc-section">
      <h3 class="section-title">
        <span>4. Desenvolvimento e Cronograma Passo a Passo</span>
        <span class="meta-tag">Total: ${escapeHtml(somaMinutos)} min</span>
      </h3>
      <div class="timeline">${cronogramaHtml}</div>
    </section>

    <section class="doc-section activity-box">
      <h3 class="section-title">5. Atividade Prática Sugerida</h3>
      <div class="activity-title">${escapeHtml(atividade.titulo)}</div>
      <p style="margin:0 0 0.5rem; font-size:0.92rem;">${escapeHtml(atividade.descricao)}</p>
      <ol class="activity-steps">${toList(atividade.passos)}</ol>
      <div class="product-box">
        <strong>Produto / Evidência Esperada:</strong> ${escapeHtml(atividade.produto_esperado)}
      </div>
    </section>

    <section class="doc-section">
      <h3 class="section-title">6. Estratégias Didáticas e Recursos</h3>
      <div class="two-col-grid">
        <div>
          <p class="sub-label">Estratégias Didáticas</p>
          <ul class="clean-list">${toList(p.estrategias_didaticas)}</ul>
        </div>
        <div>
          <p class="sub-label">Recursos Necessários</p>
          <ul class="clean-list">${toList(p.recursos_didaticos)}</ul>
        </div>
      </div>
    </section>

    <section class="doc-section">
      <h3 class="section-title">7. Avaliação da Aprendizagem</h3>
      <p style="margin:0 0 0.9rem; font-size:0.92rem;"><strong>Tipo:</strong> ${escapeHtml(avaliacao.tipo)}</p>
      <div class="two-col-grid">
        <div>
          <p class="sub-label">Instrumentos</p>
          <ul class="clean-list">${toList(avaliacao.instrumentos)}</ul>
        </div>
        <div>
          <p class="sub-label">Critérios Observáveis</p>
          <ul class="clean-list">${toList(avaliacao.criterios)}</ul>
        </div>
      </div>
    </section>

    <section class="doc-section inclusion-box">
      <h3 class="section-title">8. Inclusão e Diferenciação Pedagógica</h3>
      <p>${escapeHtml(p.inclusao_diferenciacao)}</p>
    </section>

    <section class="doc-section">
      <h3 class="section-title">9. Referências</h3>
      <ul class="clean-list">${toList(p.referencias)}</ul>
    </section>
  `;
}

// Conversão para Markdown / Texto limpo
function planToMarkdown(plan) {
  const lines = [
    `# ${plan.titulo}`,
    "",
    `- **Etapa:** ${plan.etapa}`,
    `- **Ano/Série:** ${plan.ano_serie}`,
    `- **Componente Curricular:** ${plan.componente}`,
    `- **Tema:** ${plan.tema}`,
    `- **Duração:** ${plan.duracao_minutos} minutos`,
    `- **Metodologia:** ${plan.metodologia_escolhida}`,
    ...(plan.ementa_utilizada ? [`- **Ementa Anexada:** ${plan.ementa_utilizada}`] : []),
    "",
    `> ${plan.resumo_pedagogico}`,
    "",
    "## 1. Alinhamento à BNCC",
    `**Competência Geral:** ${plan.competencia_geral_bncc}`,
    "",
    ...plan.habilidades_bncc.map((h) => `- **${h.codigo}:** ${h.descricao}`),
    "",
    "## 2. Objetivos de Aprendizagem",
    `**Objetivo Geral:** ${plan.objetivo_geral}`,
    "",
    "**Objetivos Específicos:**",
    ...plan.objetivos_especificos.map((o) => `- ${o}`),
    "",
    "## 3. Conteúdos e Conhecimentos Prévios",
    "**Conteúdos:**",
    ...plan.conteudos.map((c) => `- ${c}`),
    "",
    "**Conhecimentos Prévios:**",
    ...plan.conhecimentos_previos.map((c) => `- ${c}`),
    "",
    "## 4. Cronograma Passo a Passo",
    ...plan.cronograma.flatMap((s) => [
      `### ${s.etapa} (${s.duracao_minutos} min)`,
      `- **Objetivo:** ${s.objetivo_etapa}`,
      `- **Professor:** ${s.acao_professor}`,
      `- **Estudantes:** ${s.acao_estudantes}`,
      "",
    ]),
    "## 5. Atividade Prática Sugerida",
    `### ${plan.atividade_pratica.titulo}`,
    plan.atividade_pratica.descricao,
    "",
    ...plan.atividade_pratica.passos.map((step, i) => `${i + 1}. ${step}`),
    "",
    `**Produto Esperado:** ${plan.atividade_pratica.produto_esperado}`,
    "",
    "## 6. Estratégias Didáticas e Recursos",
    "**Estratégias:**",
    ...plan.estrategias_didaticas.map((e) => `- ${e}`),
    "",
    "**Recursos:**",
    ...plan.recursos_didaticos.map((r) => `- ${r}`),
    "",
    "## 7. Avaliação da Aprendizagem",
    `**Tipo:** ${plan.avaliacao.tipo}`,
    "",
    "**Instrumentos:**",
    ...plan.avaliacao.instrumentos.map((i) => `- ${i}`),
    "",
    "**Critérios:**",
    ...plan.avaliacao.criterios.map((c) => `- ${c}`),
    "",
    "## 8. Inclusão e Diferenciação Pedagógica",
    plan.inclusao_diferenciacao,
    "",
    "## 9. Referências",
    ...plan.referencias.map((r) => `- ${r}`),
  ];
  return lines.join("\n");
}

// Modais
function openModal(id) {
  document.getElementById(id).classList.remove("hidden");
}

function closeModal(id) {
  document.getElementById(id).classList.add("hidden");
}

// Upload e extração de ementa
async function handleEmentaFile(file) {
  if (!file) return;
  elFormError.classList.add("hidden");
  elEmentaDropzoneTitle.textContent = `Lendo "${file.name}"...`;

  const formData = new FormData();
  formData.append("arquivo", file);

  try {
    const response = await fetch("/api/extract-ementa", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Não foi possível ler o arquivo da ementa.");
    }

    attachedEmentaFilename = data.nome_arquivo;
    elEmentaTexto.value = data.texto;
    elEmentaFileName.textContent = data.nome_arquivo;
    const detalhes = [];
    if (data.num_paginas) {
      detalhes.push(`${data.num_paginas} ${data.num_paginas === 1 ? "página" : "páginas"}`);
    }
    detalhes.push(`${data.num_caracteres.toLocaleString("pt-BR")} caracteres`);
    if (data.truncado) {
      detalhes.push("resumido ao limite");
    }
    elEmentaFileMeta.textContent = detalhes.join(" • ");

    elEmentaDropzone.classList.add("hidden");
    elEmentaFileCard.classList.remove("hidden");
    elBtnPasteEmenta.classList.add("hidden");
    showToast("Ementa anexada e lida com sucesso!");
  } catch (err) {
    elFormError.textContent = err.message || "Erro ao anexar ementa.";
    elFormError.classList.remove("hidden");
  } finally {
    elEmentaDropzoneTitle.textContent = "Clique para anexar a ementa ou arraste o arquivo aqui";
    elEmentaFileInput.value = "";
  }
}

function clearEmenta() {
  attachedEmentaFilename = "";
  elEmentaTexto.value = "";
  elEmentaFileInput.value = "";
  elEmentaFileCard.classList.add("hidden");
  elEmentaTextWrapper.classList.add("hidden");
  elEmentaDropzone.classList.remove("hidden");
  elBtnPasteEmenta.classList.remove("hidden");
  elBtnToggleEmentaText.textContent = "Ver texto";
}

// Submissão do formulário
async function handleGenerate(event) {
  event.preventDefault();
  elFormError.classList.add("hidden");

  const payload = {
    etapa: elEtapa.value,
    ano_serie: elAno.value,
    componente: elComponente.value,
    tema: elTema.value.trim(),
    duracao_minutos: Number(elDuracao.value),
    metodologia: elMetodologia.value,
    recursos: getSelectedResources(),
    contexto_turma: elContexto.value.trim(),
    ementa_texto: elEmentaTexto.value.trim(),
    ementa_nome_arquivo: attachedEmentaFilename,
  };

  if (payload.tema.length < 3) {
    elFormError.textContent = "Informe um tema com pelo menos 3 caracteres.";
    elFormError.classList.remove("hidden");
    return;
  }

  elBtnGenerate.disabled = true;
  elBtnGenerateText.textContent = "Gerando plano...";
  elEmptyState.classList.add("hidden");
  elPlanOutput.classList.add("hidden");
  elLoadingState.classList.remove("hidden");

  try {
    const headers = { "Content-Type": "application/json" };
    const userKey = getUserApiKey();
    if (userKey) {
      headers["X-Gemini-Api-Key"] = userKey;
    }

    const response = await fetch("/api/generate", {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Não foi possível gerar o plano de aula.");
    }

    renderLessonPlan(data);
    saveToHistory(data);
    scrollToPlan(true);
    showToast("Plano de aula gerado com sucesso!");
  } catch (err) {
    elLoadingState.classList.add("hidden");
    if (currentResult) {
      elPlanOutput.classList.remove("hidden");
    } else {
      elEmptyState.classList.remove("hidden");
    }
    elFormError.textContent = err.message || "Erro inesperado ao comunicar com o servidor.";
    elFormError.classList.remove("hidden");
  } finally {
    elBtnGenerate.disabled = false;
    elBtnGenerateText.textContent = "Gerar Plano de Aula";
  }
}

// Inicialização
async function init() {
  try {
    const [healthRes, curriculumRes] = await Promise.all([
      fetch("/api/health"),
      fetch("/api/curriculum"),
    ]);

    if (healthRes.ok) {
      const health = await healthRes.json();
      serverHasGeminiKey = Boolean(health.gemini_configurado_servidor);
      serverDefaultModel = health.modelo_padrao || "gemini-3.5-flash";
    }

    curriculumData = await curriculumRes.json();
    const etapas = Object.keys(curriculumData.etapas);
    populateSelect(elEtapa, etapas, "Ensino Fundamental – Anos Iniciais");
    updateStageDependentFields("5º ano", "Ciências");
    populateSelect(elMetodologia, curriculumData.metodologias);
    renderResourceChips(curriculumData.recursos_padrao);
    updateAiStatusUi();
    updateHistoryBadge();
  } catch (err) {
    elFormError.textContent =
      "Erro ao carregar os dados curriculares do servidor. Verifique se o backend está rodando.";
    elFormError.classList.remove("hidden");
  }
}

// Event Listeners
elEtapa.addEventListener("change", () => updateStageDependentFields());

document.querySelectorAll(".preset-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const mins = Number(btn.dataset.min);
    elDuracao.value = mins;
    syncDurationPresetButtons(mins);
  });
});

elDuracao.addEventListener("input", () => syncDurationPresetButtons(elDuracao.value));

document.querySelectorAll(".chip[data-example]").forEach((btn) => {
  btn.addEventListener("click", () => applyExample(btn.dataset.example));
});

elForm.addEventListener("submit", handleGenerate);

// Ementa Dropzone & Upload Listeners
elEmentaDropzone.addEventListener("click", () => elEmentaFileInput.click());
elEmentaDropzone.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    elEmentaFileInput.click();
  }
});

elEmentaDropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  elEmentaDropzone.classList.add("dragover");
});

elEmentaDropzone.addEventListener("dragleave", () => {
  elEmentaDropzone.classList.remove("dragover");
});

elEmentaDropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  elEmentaDropzone.classList.remove("dragover");
  const file = e.dataTransfer?.files?.[0];
  if (file) handleEmentaFile(file);
});

elEmentaFileInput.addEventListener("change", () => {
  const file = elEmentaFileInput.files?.[0];
  if (file) handleEmentaFile(file);
});

elBtnToggleEmentaText.addEventListener("click", () => {
  const isHidden = elEmentaTextWrapper.classList.toggle("hidden");
  elBtnToggleEmentaText.textContent = isHidden ? "Ver texto" : "Ocultar texto";
});

elBtnRemoveEmenta.addEventListener("click", () => {
  clearEmenta();
  showToast("Ementa removida.");
});

elBtnPasteEmenta.addEventListener("click", () => {
  const isHidden = elEmentaTextWrapper.classList.toggle("hidden");
  elBtnPasteEmenta.textContent = isHidden
    ? "ou colar texto da ementa manualmente"
    : "ocultar campo de texto da ementa";
  if (!isHidden) {
    elEmentaTexto.focus();
  }
});

document.getElementById("btn-print").addEventListener("click", () => {
  window.print();
});

document.getElementById("btn-copy").addEventListener("click", async () => {
  if (!currentResult) return;
  try {
    await navigator.clipboard.writeText(planToMarkdown(currentResult.plano));
    showToast("Plano copiado! Cole no Word ou Google Docs.");
  } catch {
    showToast("Não foi possível copiar automaticamente.");
  }
});

document.getElementById("btn-download-md").addEventListener("click", () => {
  if (!currentResult) return;
  const md = planToMarkdown(currentResult.plano);
  const slug = currentResult.plano.tema
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 40);
  const blob = new Blob([md], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `plano-de-aula-${slug || "bncc"}.md`;
  a.click();
  URL.revokeObjectURL(url);
  showToast("Arquivo Markdown baixado.");
});

// Modal Settings
document.getElementById("btn-open-settings").addEventListener("click", () => {
  elInputApiKey.value = getUserApiKey();
  openModal("modal-settings");
});

document.getElementById("btn-save-key").addEventListener("click", () => {
  const key = elInputApiKey.value.trim();
  if (key) {
    sessionStorage.setItem(SESSION_KEY_GEMINI, key);
    showToast("Chave da API Gemini salva para esta sessão!");
  } else {
    sessionStorage.removeItem(SESSION_KEY_GEMINI);
    showToast("Chave removida. Voltando ao modo padrão.");
  }
  updateAiStatusUi();
  closeModal("modal-settings");
});

document.getElementById("btn-clear-key").addEventListener("click", () => {
  sessionStorage.removeItem(SESSION_KEY_GEMINI);
  elInputApiKey.value = "";
  updateAiStatusUi();
  showToast("Chave da sessão removida.");
  closeModal("modal-settings");
});

// Modal History
document.getElementById("btn-open-history").addEventListener("click", () => {
  renderHistoryModal();
  openModal("modal-history");
});

document.getElementById("btn-clear-history").addEventListener("click", () => {
  localStorage.removeItem(STORAGE_KEY_HISTORY);
  updateHistoryBadge();
  renderHistoryModal();
  showToast("Histórico limpo.");
});

document.querySelectorAll("[data-close-modal]").forEach((el) => {
  el.addEventListener("click", () => closeModal(el.dataset.closeModal));
});

init();

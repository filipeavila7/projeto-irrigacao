// Válvulas
const container = document.getElementById("valvulasContainer");
const exemplo = document.getElementById("valvulasExemplo");
const toggle = document.getElementById("valvulasToggle");
let expanded = false;
if (container && exemplo && toggle) {
  const header = container.querySelector(".rectangle-32");
  header.onclick = function (e) {
    expanded = !expanded;
    if (expanded) {
      exemplo.style.display = "block";
      // Força reflow para garantir transição
      void exemplo.offsetWidth;
      exemplo.classList.add("show");
      toggle.style.transform = "rotate(180deg)";
    } else {
      // Garante que a transição ocorra mesmo se display já for block
      exemplo.classList.remove("show");
      toggle.style.transform = "rotate(0deg)";
      // Aguarda a transição para esconder
      const handler = function (ev) {
        if (ev.propertyName === "max-height") {
          exemplo.style.display = "none";
          exemplo.removeEventListener("transitionend", handler);
        }
      };
      exemplo.addEventListener("transitionend", handler);
      // Cria os elementos das válvulas a partir da lista
      const boxes = valvulas.map((valvula) => {
        const box = document.createElement("div");
        box.className = "valvula-box";
        box.id = "valvula" + valvula.id;
        box.innerHTML = `
              <div class="valvula-label" data-id="\${valvula.id}" style="cursor:pointer;">\${valvula.nome} (\${valvula.serial})</div>
              <div class="status" id="statusValvula\${valvula.id}">\${valvula.ativada ? "Ativada" : "Desativada"}</div>
              <img class="mdi-valve" id="imgValvula\${valvula.id}" src="static/img/\${valvula.ativada ? "mdi--valve-open.svg" : "mdi--valve.svg"}" alt="\${valvula.ativada ? "valvulaAberta" : "valvulaFechada"}"/>
              <button class="toggle-btn \${valvula.ativada ? "ativada" : "desativada"}" id="btnValvula\${valvula.id}">\${valvula.ativada ? "Desativar" : "Ativar"}</button>
            `;
        return box;
      });
    }
  };
}
const estacaoExemplo = document.getElementById("estacaoExemplo");
const estacaoToggle = document.getElementById("estacaoToggle");
let estacaoExpanded = false;
if (estacaoContainer && estacaoExemplo && estacaoToggle) {
  // Mock para últimas 24h (hora a hora)
  const weatherCardsData = {
    "24h": [
      {
        title: "00h",
        temp: 19,
        min: 16,
        max: 27,
        umidade: 80,
        vento: 8,
        chuva: 0,
      },
      {
        title: "03h",
        temp: 18,
        min: 16,
        max: 27,
        umidade: 82,
        vento: 7,
        chuva: 0,
      },
      {
        title: "06h",
        temp: 17,
        min: 16,
        max: 27,
        umidade: 85,
        vento: 6,
        chuva: 0,
      },
      {
        title: "09h",
        temp: 20,
        min: 16,
        max: 27,
        umidade: 70,
        vento: 10,
        chuva: 0,
      },
      {
        title: "12h",
        temp: 24,
        min: 16,
        max: 27,
        umidade: 60,
        vento: 12,
        chuva: 0,
      },
      {
        title: "15h",
        temp: 27,
        min: 16,
        max: 27,
        umidade: 55,
        vento: 14,
        chuva: 0,
      },
      {
        title: "18h",
        temp: 25,
        min: 16,
        max: 27,
        umidade: 65,
        vento: 11,
        chuva: 0,
      },
      {
        title: "21h",
        temp: 22,
        min: 16,
        max: 27,
        umidade: 75,
        vento: 9,
        chuva: 0,
      },
    ],
    semana: [
      {
        title: "Seg",
        temp: 27,
        min: 16,
        max: 27,
        desc: "Ensolarado",
        umidade: 60,
        vento: 10,
        chuva: 0,
      },
      {
        title: "Ter",
        temp: 22,
        min: 16,
        max: 27,
        desc: "Nublado",
        umidade: 65,
        vento: 12,
        chuva: 2,
      },
      {
        title: "Qua",
        temp: 28,
        min: 16,
        max: 27,
        desc: "Sol",
        umidade: 58,
        vento: 11,
        chuva: 0,
      },
      {
        title: "Qui",
        temp: 19,
        min: 16,
        max: 27,
        desc: "Chuva",
        umidade: 80,
        vento: 8,
        chuva: 10,
      },
      {
        title: "Sex",
        temp: 24,
        min: 16,
        max: 27,
        desc: "Nublado",
        umidade: 70,
        vento: 9,
        chuva: 1,
      },
      {
        title: "Sáb",
        temp: 25,
        min: 16,
        max: 27,
        desc: "Sol",
        umidade: 62,
        vento: 10,
        chuva: 0,
      },
      {
        title: "Dom",
        temp: 26,
        min: 16,
        max: 27,
        desc: "Ensolarado",
        umidade: 60,
        vento: 8,
        chuva: 0,
      },
    ],
    mes: [
      {
        title: "01/06",
        temp: 25,
        min: 15,
        max: 28,
        desc: "Sol",
        umidade: 60,
        vento: 10,
        chuva: 0,
      },
      {
        title: "05/06",
        temp: 23,
        min: 14,
        max: 27,
        desc: "Nublado",
        umidade: 65,
        vento: 12,
        chuva: 2,
      },
      {
        title: "10/06",
        temp: 21,
        min: 13,
        max: 26,
        desc: "Chuva",
        umidade: 80,
        vento: 8,
        chuva: 10,
      },
      {
        title: "15/06",
        temp: 27,
        min: 16,
        max: 29,
        desc: "Ensolarado",
        umidade: 58,
        vento: 11,
        chuva: 0,
      },
      {
        title: "20/06",
        temp: 28,
        min: 17,
        max: 30,
        desc: "Sol",
        umidade: 62,
        vento: 10,
        chuva: 0,
      },
      {
        title: "25/06",
        temp: 22,
        min: 15,
        max: 27,
        desc: "Nublado",
        umidade: 70,
        vento: 9,
        chuva: 1,
      },
      {
        title: "30/06",
        temp: 26,
        min: 16,
        max: 28,
        desc: "Sol",
        umidade: 60,
        vento: 8,
        chuva: 0,
      },
    ],
  };

  // Clima atual fixo (mock)
  const climaAtual = {
    temp: 27,
    min: 16,
    max: 27,
    umidade: 74,
    vento: 12,
    chuva: 57,
  };

  function updateWeatherMain() {
    document.getElementById("weatherTemp").textContent = climaAtual.temp;
    document.getElementById("weatherMin").textContent = climaAtual.min;
    document.getElementById("weatherMax").textContent = climaAtual.max;
    document.getElementById("weatherHumidity").textContent =
      climaAtual.umidade + "%";
    document.getElementById("weatherWind").textContent =
      climaAtual.vento + "km/h";
    document.getElementById("weatherRain").textContent = climaAtual.chuva + "%";
  }

  // Remova o helper showWeatherCardsImmediate e ajuste o toggle para não ocultar/mostrar os cards manualmente
  const header = estacaoContainer.querySelector(".rectangle-32");
  header.onclick = function (e) {
    estacaoExpanded = !estacaoExpanded;
    if (estacaoExpanded) {
      estacaoExemplo.style.display = "block";
      void estacaoExemplo.offsetWidth;
      estacaoExemplo.classList.add("show");
      estacaoToggle.style.transform = "rotate(180deg)";
    } else {
      estacaoExemplo.classList.remove("show");
      estacaoToggle.style.transform = "rotate(0deg)";
      estacaoExemplo.addEventListener("transitionend", function handler(ev) {
        if (ev.propertyName === "max-height") {
          estacaoExemplo.style.display = "none";
          estacaoExemplo.removeEventListener("transitionend", handler);
        }
      });
    }
    e.stopPropagation();
  };

  // Função auxiliar para retornar os dados das abas umidade, vento, chuva
  function getCardsByTab(period, tab) {
    const data = weatherCardsData[period] || [];
    if (tab === "umidade") {
      return data.map((d) => {
        let label = "";
        if (d.umidade < 30) {
          label = "Muito baixa";
        } else if (d.umidade < 60) {
          label = "Baixa";
        } else if (d.umidade < 80) {
          label = "Moderada";
        } else {
          label = "Alta";
        }
        return {
          title: d.title,
          value: d.umidade + "%",
          label: label,
        };
      });
    }
    if (tab === "vento") {
      return data.map((d) => {
        let label = "";
        if (d.vento < 5) {
          label = "Calmo";
        } else if (d.vento < 15) {
          label = "Moderado";
        } else {
          label = "Forte";
        }
        return {
          title: d.title,
          value: d.vento + " km/h",
          label: label,
        };
      });
    }
    if (tab === "chuva") {
      return data.map((d) => {
        let label = "";
        if (d.chuva === 0) {
          label = "Sem chuva";
        } else if (d.chuva < 5) {
          label = "Pouca chuva";
        } else if (d.chuva < 20) {
          label = "Chuva moderada";
        } else {
          label = "Chuva intensa";
        }
        return {
          title: d.title,
          value: d.chuva + "mm",
          label: label,
        };
      });
    }
    return [];
  }

  function renderWeatherCards(period, tab) {
    const cards = document.getElementById("weatherCards");
    if (!cards) return;
    cards.innerHTML = "";
    if (tab === "visao") {
      if (period === "24h") {
        // Um card por hora, mostrando temperatura daquele horário
        (weatherCardsData["24h"] || []).forEach((item) => {
          const card = document.createElement("div");
          card.className = "weather-card";
          card.innerHTML = `
            <div class="weather-card-title">${item.title}</div>
            <div class="weather-card-temp">${item.temp}°C</div>
            <div class="weather-card-minmax">min ${item.min}°C<br>max ${item.max}°C</div>
          `;
          cards.appendChild(card);
        });
      } else {
        // Um card por dia, mostrando média, min, max daquele dia
        (weatherCardsData[period] || []).forEach((item) => {
          const card = document.createElement("div");
          card.className = "weather-card";
          card.innerHTML = `
            <div class="weather-card-title">${item.title}</div>
            <div class="weather-card-temp">${item.temp}°C</div>
            <div class="weather-card-minmax">min ${item.min}°C<br>max ${item.max}°C</div>
          `;
          cards.appendChild(card);
        });
      }
    } else {
      // Umidade, Vento, Chuva: mostra cards por hora/dia
      const data = getCardsByTab(period, tab);
      data.forEach((item) => {
        const div = document.createElement("div");
        div.className = "weather-card";
        div.innerHTML = `
          <div class="weather-card-title">${item.title}</div>
          <div class="weather-card-temp">${item.value}</div>
          <div class="weather-card-desc">${item.label}</div>
        `;
        cards.appendChild(div);
      });
    }
    cards.style.display = cards.children.length > 0 ? "flex" : "";
  }

  let currentTab = "visao";
  let currentPeriod = "24h";

  function updateWeatherCards() {
    renderWeatherCards(currentPeriod, currentTab);
    updateWeatherMain();
  }

  // Dropdown de período
  const weatherPeriod = document.getElementById("weatherPeriod");
  if (weatherPeriod) {
    weatherPeriod.addEventListener("change", function (e) {
      currentPeriod = weatherPeriod.value;
      updateWeatherCards();
    });
    currentPeriod = weatherPeriod.value;
  }

  // Abas
  document.querySelectorAll(".weather-tab").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      document
        .querySelectorAll(".weather-tab")
        .forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentTab = btn.getAttribute("data-tab");
      updateWeatherCards();
      e.stopPropagation();
    });
  });

  // Inicializa
  updateWeatherCards();
}

// Controle das válvulas
let valvulaCount = 0;
let valvulas = []; // Lista local de válvulas

function renderValvulas() {
  const assets = document.getElementById("valvulasAssets");
  if (!assets) return;
  // Remove linhas antigas e válvulas antigas, mas NÃO remove o addValvulaBox
  Array.from(assets.querySelectorAll(".valvulas-row")).forEach((r) =>
    r.remove(),
  );
  Array.from(assets.querySelectorAll(".valvula-box")).forEach((b) =>
    b.remove(),
  );

  // Cria os elementos das válvulas a partir da lista
  const boxes = valvulas.map((valvula) => {
    const box = document.createElement("div");
    box.className = "valvula-box";
    box.id = "valvula" + valvula.id;
    box.innerHTML = `
      <div class="valvula-label" data-id="${valvula.id}" style="cursor:pointer;">${valvula.nome} (${valvula.serial})</div>
      <div class="status" id="statusValvula${valvula.id}">${valvula.ativada ? "Ativada" : "Desativada"}</div>
      <img class="mdi-valve" id="imgValvula${valvula.id}" src="static/img/${valvula.ativada ? "mdi--valve-open.svg" : "mdi--valve.svg"}" alt="${valvula.ativada ? "valvulaAberta" : "valvulaFechada"}"/>
      <button class="toggle-btn ${valvula.ativada ? "ativada" : "desativada"}" id="btnValvula${valvula.id}">${valvula.ativada ? "Desativar" : "Ativar"}</button>
              <button class="registros-btn" id="btnRegistros${valvula.id}">Ver registros</button>
              <div class="registros-panel" id="registrosPanel${valvula.id}" style="display:none; margin-top:12px; max-height:200px; overflow:auto; background:#fff; padding:8px; border-radius:6px;"></div>
    `;
    return box;
  });

  // Cálculo dinâmico de válvulas por linha
  const valvulasExemplo = document.getElementById("valvulasExemplo");
  let containerWidth = 1080; // fallback padrão
  if (valvulasExemplo) {
    containerWidth =
      valvulasExemplo.clientWidth || valvulasExemplo.offsetWidth || 1080;
  }
  const boxWidth = 180 + 24; // largura da válvula + gap horizontal
  const perRow = Math.max(1, Math.floor((containerWidth + 24) / boxWidth));

  // Agrupa em linhas dinâmicas
  let rows = [];
  for (let i = 0; i < boxes.length; i += perRow) {
    const row = document.createElement("div");
    row.className = "valvulas-row";
    row.style.display = "flex";
    row.style.flexDirection = "row";
    row.style.gap = "24px";
    row.style.marginBottom = "24px";
    boxes.slice(i, i + perRow).forEach((b) => row.appendChild(b));
    rows.push(row);
  }

  // Insere as linhas (sempre após o addValvulaBox, mantendo a ordem correta)
  const addBox = document.getElementById("addValvulaBox");
  let nextSibling = addBox.nextSibling;
  rows.forEach((r) => {
    assets.insertBefore(r, nextSibling);
    nextSibling = r.nextSibling;
  });

  // Setup eventos
  boxes.forEach((b, idx) => {
    const valvula = valvulas[idx];
    setupValvula(valvula.id);
    setupValvulaLabel(b.querySelector(".valvula-label"));
    // setup registros button
    const regBtn = b.querySelector(`#btnRegistros${valvula.id}`);
    if (regBtn) {
      regBtn.addEventListener("click", async (e) => {
        const panel = document.getElementById(`registrosPanel${valvula.id}`);
        if (!panel) return;
        if (panel.style.display === "none") {
          panel.style.display = "block";
          panel.innerHTML =
            '<div class="loading">Carregando registros...</div>';
          try {
            const resp = await fetch(`/api/registros/valvula/${valvula.id}`, {
              credentials: "same-origin",
            });
            if (!resp.ok) {
              panel.innerHTML =
                '<div class="error">Erro ao buscar registros</div>';
              return;
            }
            const data = await resp.json();
            const items = data.registros || data;
            if (!items || items.length === 0) {
              panel.innerHTML = '<div class="empty">Sem registros</div>';
              return;
            }
            panel.innerHTML = items
              .slice(0, 20)
              .map((r) => {
                const ts = new Date(
                  r.data || r.timestamp || r.created_at,
                ).toLocaleString();
                const status =
                  r.ativado !== undefined
                    ? r.ativado
                      ? "Ativado"
                      : "Desativado"
                    : r.status || "—";
                return `<div class="registro-item" style="padding:6px 0;border-bottom:1px solid #eee">${ts} — ${status}</div>`;
              })
              .join("");
          } catch (err) {
            console.error(err);
            panel.innerHTML =
              '<div class="error">Erro de rede ao buscar registros</div>';
          }
        } else {
          panel.style.display = "none";
        }
      });
    }
  });

  // Ajusta rolagem
  if (valvulasExemplo) {
    valvulasExemplo.style.maxHeight = "600px";
    valvulasExemplo.style.overflowY = "auto";
  }
}

function setupValvula(id) {
  const btn = document.getElementById("btnValvula" + id);
  const img = document.getElementById("imgValvula" + id);
  const status = document.getElementById("statusValvula" + id);
  if (!btn || !img || !status) return;

  btn.onclick = null;

  // Busca a válvula na lista local
  const valvula = valvulas.find((v) => v.id === Number(id));
  if (!valvula) return;

  function updateUI() {
    if (valvula.ativada) {
      img.src = "static/img/mdi--valve-open.svg";
      status.textContent = "Ativada";
      status.classList.add("ativada");
      status.classList.remove("desativada");
      btn.textContent = "Desativar";
      btn.classList.add("ativada");
      btn.classList.remove("desativada");
    } else {
      img.src = "static/img/mdi--valve.svg";
      status.textContent = "Desativada";
      status.classList.remove("ativada");
      status.classList.add("desativada");
      btn.textContent = "Ativar";
      btn.classList.remove("ativada");
      btn.classList.add("desativada");
    }
  }

  updateUI();

  btn.onclick = function () {
    img.classList.remove(
      "valve-rotate-in",
      "valve-rotate-out",
      "valve-rotate-in-reverse",
      "valve-rotate-out-reverse",
    );
    if (!valvula.ativada) {
      img.classList.add("valve-rotate-in");
      setTimeout(() => {
        valvula.ativada = true;
        updateUI();
        img.classList.remove("valve-rotate-in");
        img.classList.add("valve-rotate-out");
        setTimeout(() => img.classList.remove("valve-rotate-out"), 300);
      }, 150);
    } else {
      img.classList.add("valve-rotate-in-reverse");
      setTimeout(() => {
        valvula.ativada = false;
        updateUI();
        img.classList.remove("valve-rotate-in-reverse");
        img.classList.add("valve-rotate-out-reverse");
        setTimeout(() => img.classList.remove("valve-rotate-out-reverse"), 300);
      }, 150);
    }
  };
}

function setupValvulaLabel(label) {
  if (!label) return;
  label.onclick = function (e) {
    showValvulaActions(label);
    e.stopPropagation();
  };
}

// Adicionar válvula dinamicamente
const adicionarValvula = document.getElementById("adicionarValvula");
const valvulasAssets = document.getElementById("valvulasAssets");
if (adicionarValvula && valvulasAssets) {
  adicionarValvula.onclick = function () {
    showAddValvulaModal((nome, serial) => {
      valvulaCount++;
      valvulas.push({
        id: valvulaCount,
        nome,
        serial,
        ativada: false,
      });
      renderValvulas();
    });
  };
}

// Modal de confirmação customizada
function showConfirmModal(msg, onConfirm) {
  let modal = document.getElementById("confirmModal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "confirmModal";
    modal.innerHTML = `
      <div class="custom-modal-bg">
        <div class="custom-modal-content">
          <div class="custom-modal-title">Confirmação</div>
          <div class="custom-modal-msg"></div>
          <div class="custom-modal-actions">
            <button class="custom-modal-btn custom-modal-btn-yes">Sim</button>
            <button class="custom-modal-btn custom-modal-btn-no">Não</button>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }
  modal.querySelector(".custom-modal-msg").textContent = msg;
  modal.style.display = "block";
  modal.querySelector(".custom-modal-btn-yes").onclick = () => {
    modal.style.display = "none";
    onConfirm();
  };
  modal.querySelector(".custom-modal-btn-no").onclick = () => {
    modal.style.display = "none";
  };
}

// Modal para adicionar válvula
function showAddValvulaModal(onAdd) {
  let modal = document.getElementById("addValvulaModal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "addValvulaModal";
    modal.innerHTML = `
      <div class="custom-modal-bg">
        <div class="custom-modal-content">
          <div class="custom-modal-title">Adicionar Válvula</div>
          <div style="width:100%;margin-bottom:16px;">
            <label style="font-family:'Nexa-Heavy',sans-serif;font-size:16px;display:block;margin-bottom:6px;">Nome</label>
            <input id="addValvulaNome" type="text" style="width:100%;padding:8px 12px;font-size:16px;border-radius:6px;border:1px solid #bbb;margin-bottom:12px;">
            <label style="font-family:'Nexa-Heavy',sans-serif;font-size:16px;display:block;margin-bottom:6px;">Número Serial</label>
            <input id="addValvulaSerial" type="text" style="width:100%;padding:8px 12px;font-size:16px;border-radius:6px;border:1px solid #bbb;">
          </div>
          <div class="custom-modal-actions">
            <button class="custom-modal-btn custom-modal-btn-yes" id="addValvulaConfirm">Adicionar</button>
            <button class="custom-modal-btn custom-modal-btn-no" id="addValvulaCancel">Cancelar</button>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }
  modal.style.display = "block";
  const nomeInput = modal.querySelector("#addValvulaNome");
  const serialInput = modal.querySelector("#addValvulaSerial");
  nomeInput.value = "";
  serialInput.value = "";
  nomeInput.focus();

  modal.querySelector("#addValvulaConfirm").onclick = () => {
    const nome = nomeInput.value.trim();
    const serial = serialInput.value.trim();
    if (!nome || !serial) {
      nomeInput.focus();
      return;
    }
    modal.style.display = "none";
    onAdd(nome, serial);
  };
  modal.querySelector("#addValvulaCancel").onclick = () => {
    modal.style.display = "none";
  };
}

// Modal para editar válvula
function showEditValvulaModal(box, label) {
  let modal = document.getElementById("editValvulaModal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "editValvulaModal";
    modal.innerHTML = `
      <div class="custom-modal-bg">
        <div class="custom-modal-content">
          <div class="custom-modal-title">Editar Válvula</div>
          <div style="width:100%;margin-bottom:16px;">
            <label style="font-family:'Nexa-Heavy',sans-serif;font-size:16px;display:block;margin-bottom:6px;">Nome</label>
            <input id="editValvulaNome" type="text" style="width:100%;padding:8px 12px;font-size:16px;border-radius:6px;border:1px solid #bbb;margin-bottom:12px;">
            <label style="font-family:'Nexa-Heavy',sans-serif;font-size:16px;display:block;margin-bottom:6px;">Número Serial</label>
            <input id="editValvulaSerial" type="text" style="width:100%;padding:8px 12px;font-size:16px;border-radius:6px;border:1px solid #bbb;">
          </div>
          <div class="custom-modal-actions">
            <button class="custom-modal-btn custom-modal-btn-yes" id="editValvulaConfirm">Salvar</button>
            <button class="custom-modal-btn custom-modal-btn-no" id="editValvulaCancel">Cancelar</button>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }
  // Busca id da válvula
  const boxId = box.id.replace("valvula", "");
  const valvula = valvulas.find((v) => v.id === Number(boxId));
  if (!valvula) return;

  modal.style.display = "block";
  const nomeInput = modal.querySelector("#editValvulaNome");
  const serialInput = modal.querySelector("#editValvulaSerial");
  nomeInput.value = valvula.nome;
  serialInput.value = valvula.serial;
  nomeInput.focus();

  modal.querySelector("#editValvulaConfirm").onclick = () => {
    const nome = nomeInput.value.trim();
    const serial = serialInput.value.trim();
    if (!nome || !serial) {
      nomeInput.focus();
      return;
    }
    valvula.nome = nome;
    valvula.serial = serial;
    modal.style.display = "none";
    renderValvulas();
  };
  modal.querySelector("#editValvulaCancel").onclick = () => {
    modal.style.display = "none";
  };
}

// Modal para editar válvula (versão simplificada)
function showValvulaEdit(box, label) {
  // Oculta todas as outras válvulas
  document.querySelectorAll(".valvula-box").forEach((b) => {
    if (b !== box) b.style.display = "none";
    else b.style.display = "";
  });

  // Cria container para label + botões
  const nomeAtual = label.textContent;
  const editContainer = document.createElement("div");
  editContainer.className = "valvula-edit-label";
  editContainer.style.display = "flex";
  editContainer.style.alignItems = "center";
  editContainer.style.width = "100%";

  // Input menor
  const input = document.createElement("input");
  input.type = "text";
  input.value = nomeAtual;
  input.className = "valvula-edit-input";
  input.style.fontSize = "22px"; // Reduzido
  input.style.fontFamily = "Nexa-Heavy,sans-serif";
  input.style.fontWeight = "700";
  input.style.marginBottom = "8px"; // Reduzido
  input.style.width = "100%";
  input.style.textAlign = "center";
  input.style.background = "none";
  input.style.border = "none";
  input.style.outline = "none";

  // Botão salvar (ícone)
  const saveBtn = document.createElement("button");
  saveBtn.className = "icon-btn save-btn";
  saveBtn.title = "Salvar";
  saveBtn.style.marginLeft = "8px";
  saveBtn.innerHTML = `<img src="static/img/edit-outline.svg" alt="Salvar" style="width:22px;height:22px;">`;

  // Botão cancelar (ícone)
  const cancelBtn = document.createElement("button");
  cancelBtn.className = "icon-btn cancel-btn";
  cancelBtn.title = "Cancelar";
  cancelBtn.style.marginLeft = "4px";
  cancelBtn.innerHTML = `<img src="static/img/close.svg" alt="Cancelar" style="width:22px;height:22px;">`;

  // Substitui label
  label.style.display = "none";
  editContainer.appendChild(input);
  editContainer.appendChild(saveBtn);
  editContainer.appendChild(cancelBtn);
  label.parentNode.insertBefore(editContainer, label);

  // Foco no input
  input.focus();
  input.select();

  saveBtn.onclick = function () {
    const novoNome = input.value.trim();
    if (novoNome === "") {
      showConfirmModal("Deseja realmente excluir esta válvula?", () => {
        box.remove();
        updateValvulasLayout();
        // Após excluir, restaura visualização das válvulas
        document
          .querySelectorAll(".valvula-box")
          .forEach((b) => (b.style.display = ""));
      });
      return;
    }
    label.textContent = novoNome;
    cleanup();
    updateValvulasLayout();
    // Após editar, restaura visualização das válvulas
    document
      .querySelectorAll(".valvula-box")
      .forEach((b) => (b.style.display = ""));
  };
  cancelBtn.onclick = function () {
    cleanup();
    // Após cancelar, restaura visualização das válvulas
    document
      .querySelectorAll(".valvula-box")
      .forEach((b) => (b.style.display = ""));
  };
  function cleanup() {
    editContainer.remove();
    label.style.display = "";
  }
}

// Inicializar labels existentes
function setupValvulaLabel(label) {
  if (!label) return;
  label.onclick = function (e) {
    showValvulaActions(label);
    e.stopPropagation();
  };
}
document.querySelectorAll(".valvula-label").forEach(setupValvulaLabel);

// Atualiza layout das válvulas (rolagem e linhas de 5)
function updateValvulasLayout() {
  const assets = document.getElementById("valvulasAssets");
  if (!assets) return;
  // Remove agrupamentos antigos
  Array.from(assets.querySelectorAll(".valvulas-row")).forEach((r) =>
    r.remove(),
  );
  // Seleciona todas as válvulas (exclui o botão de adicionar)
  const boxes = Array.from(assets.querySelectorAll(".valvula-box"));
  // Remove todas do assets
  boxes.forEach((b) => assets.removeChild(b));
  // Agrupa em linhas de 5
  let rows = [];
  for (let i = 0; i < boxes.length; i += 5) {
    const row = document.createElement("div");
    row.className = "valvulas-row";
    row.style.display = "flex";
    row.style.flexDirection = "row";
    row.style.gap = "48px";
    row.style.marginBottom = "24px";
    boxes.slice(i, i + 5).forEach((b) => row.appendChild(b));
    rows.push(row);
  }
  // Insere as linhas antes do botão de adicionar
  const addBox = document.getElementById("addValvulaBox");
  rows.forEach((r) => assets.insertBefore(r, addBox));
  // Reatribui eventos para cada válvula
  boxes.forEach((b) => {
    const id = b.id.replace("valvula", "");
    setupValvula(id);
    setupValvulaLabel(b.querySelector(".valvula-label"));
  });
  // Se <=5, remove rolagem
  const valvulasExemplo = document.getElementById("valvulasExemplo");
  if (boxes.length > 5) {
    valvulasExemplo.style.maxHeight = "600px";
    valvulasExemplo.style.overflowY = "auto";
  } else {
    valvulasExemplo.style.maxHeight = "";
    valvulasExemplo.style.overflowY = "";
  }
}
updateValvulasLayout();

// Funções de editar/excluir válvula
function showValvulaActions(label) {
  // Remove qualquer menu de ação anterior
  document.querySelectorAll(".valvula-actions-menu").forEach((e) => e.remove());
  const box = label.closest(".valvula-box");
  if (!box) return;
  document
    .querySelectorAll(".valvula-box")
    .forEach((b) => (b.style.display = ""));

  // Cria menu de ações alinhado nas extremidades
  const menu = document.createElement("div");
  menu.className = "valvula-actions-menu";
  menu.innerHTML = `
    <div class="edit rectangle-36" style="cursor:pointer; left:0;">
      <div class="mingcute-edit-line">
        <img class="group" src="static/img/edit-outline.svg" alt="editar"/>
      </div>
    </div>
    <div class="delete rectangle-37" style="cursor:pointer; right:0;">
      <img class="material-symbols-delete-outline" src="static/img/delete-outline.svg" alt="excluir"/>
    </div>
  `;
  box.appendChild(menu);

  menu.querySelector(".edit").onclick = function (e) {
    menu.remove();
    showEditValvulaModal(box, label);
    e.stopPropagation();
  };
  menu.querySelector(".delete").onclick = function (e) {
    showConfirmModal("Deseja realmente excluir esta válvula?", () => {
      // Remove da lista local
      const boxId = box.id.replace("valvula", "");
      valvulas = valvulas.filter((v) => v.id !== Number(boxId));
      renderValvulas();
      document
        .querySelectorAll(".valvula-box")
        .forEach((b) => (b.style.display = ""));
    });
    menu.remove();
    e.stopPropagation();
  };

  setTimeout(() => {
    document.addEventListener("mousedown", function handler(ev) {
      if (!menu.contains(ev.target)) {
        menu.remove();
        document.removeEventListener("mousedown", handler);
      }
    });
  }, 10);
}

// Inicialização: se houver válvulas no HTML, adiciona à lista local
document.querySelectorAll(".valvula-box").forEach((box) => {
  const label = box.querySelector(".valvula-label");
  if (label) {
    const text = label.textContent || "";
    const match = text.match(/^(.*)\s+\((.*)\)$/);
    let nome = "",
      serial = "";
    if (match) {
      nome = match[1];
      serial = match[2];
    } else {
      nome = text;
      serial = "";
    }
    valvulaCount++;
    valvulas.push({
      id: valvulaCount,
      nome,
      serial,
      ativada: false,
    });
  }
});
renderValvulas();

const API_URL = "/api/reter/prever";

let ultimaPrevisao = null;
let previsaoComSucesso = false;

const btnPrever = document.getElementById("btn-form");
const btnRetry = document.getElementById("btn-retry");
const modal = document.getElementById("modal-response");
const labelPrevisao = document.getElementById("response-prediction");
const labelProbabilidade = document.getElementById("response-probability");
const form = document.getElementById("form");
const btnFecharModal = document.getElementById("btn-modal-close");

btnPrever.addEventListener("click", verificarFormulario);

document.querySelectorAll("input, select").forEach((campo) => {
  campo.addEventListener("input", () => {
    campo.classList.remove("invalid");
  });
});

// FLUXO PRINCIPAL

async function verificarFormulario() {
  if (!formularioValido()) return;
  await preverCancelamento();
}

async function preverCancelamento() {
  const payload = montarPayloadPrevisao();

  abrirModal("Processando previsão...", "");

  try {
    const response = await axios.post(API_URL, payload);
    ultimaPrevisao = response.data;
    mostrarResultado();
  } catch (error) {
    mostrarErro(error);
  }
}

// MODAL

function abrirModal(texto, probabilidade) {
  labelPrevisao.textContent = texto;
  labelProbabilidade.textContent = probabilidade;
  modal.showModal();
}

function mostrarResultado() {
  previsaoComSucesso = true;

  labelPrevisao.innerHTML = `<strong>Previsão:</strong> ${ultimaPrevisao.previsao}`;
  labelProbabilidade.innerHTML = `<strong>Probabilidade:</strong> ${ultimaPrevisao.probabilidade}`;
}

function mostrarErro(error) {
  previsaoComSucesso = false;
  mostrarBotaoRetry(true);

  labelPrevisao.textContent = "Serviço indisponível no momento";
  labelProbabilidade.textContent = "Tente novamente em instantes";

  if (error.response) {
    console.error("Erro HTTP:", error.response.status);
  } else {
    console.error("Erro de conexão");
  }
}

function mostrarBotaoRetry(mostrar) {
  btnRetry.hidden = !mostrar;
}

btnFecharModal.addEventListener("click", () => {
  if (previsaoComSucesso) {
    form.reset();
  }

  mostrarBotaoRetry(false);
  previsaoComSucesso = false;
  window.scrollTo({ top: 0, behavior: "smooth" });
  modal.close();
});

btnRetry.addEventListener("click", async () => {
  mostrarBotaoRetry(false);
  abrirModal("Tentando novamente...", "");
  await preverCancelamento();
});

// FORMULÁRIO

function formularioValido() {
  let valido = true;
  const campos = document.querySelectorAll("input, select");
  let primeiroErro = null;

  campos.forEach((campo) => {
    if (!campo.value) {
      campo.classList.add("invalid");
      valido = false;

      if (!primeiroErro) {
        primeiroErro = campo;
      }
    } else {
      campo.classList.remove("invalid");
    }
  });

  if (primeiroErro) {
    primeiroErro.scrollIntoView({
      behavior: "smooth",
      block: "center",
    });
    primeiroErro.focus();
  }

  return valido;
}

function montarPayloadPrevisao() {
  return {
    genero: genero.value,
    idoso: Number(idoso.value),
    parceiro: Number(parceiro.value),
    dependentes: Number(dependentes.value),

    tempo_contrato_meses: Number(tempo_contrato_meses.value),
    servico_telefone: Number(servico_telefone.value),
    linhas_multiplas: linhas_multiplas.value,
    tipo_internet: tipo_internet.value,

    seguranca_online: seguranca_online.value,
    backup_online: backup_online.value,
    protecao_dispositivo: protecao_dispositivo.value,
    suporte_tecnico: suporte_tecnico.value,
    streaming_tv: streaming_tv.value,
    streaming_filmes: streaming_filmes.value,

    tipo_contrato: tipo_contrato.value,
    cobranca_digital: Number(cobranca_digital.value),
    metodo_pagamento: metodo_pagamento.value,
    cobranca_mensal: Number(cobranca_mensal.value),
    cobranca_total: Number(cobranca_total.value),
  };
}

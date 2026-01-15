const API_URL = "http://localhost:8080/reter/prever";
import {navegar} from "./util.js"

let ultimaPrevisao;

async function preverCancelamento() {
    let payload = montarPayloadPrevisao()
    const modalDeCarregamento = apresentarModalDeCarregamento();
    const modalResposta = criarModalDeResposta();
    // payload.idoso = null;

    try {
        const response = await axios.post(API_URL, payload);
        ultimaPrevisao = response.data;
        setTimeout(()=>{
            modalDeCarregamento.hide();
            criarTelaResposta(modalResposta);
        }, 500)
    } catch (error) {
        setTimeout(()=>{
        modalDeCarregamento.hide();
        apresentarModalDeErro(modalResposta)
        }, 500)
        console.log("Erro na requisição:" + error);
        if (error.response) {
            console.log("Erro no servidor: " + error.response.status);
        } else {
            console.log("Erro de conexão. Verifique se o servidor está rodando.");
        }
    }
    //todo retornar ao
    // front um modal, ou alert, avisando da situação.
    // Esses ifs tem que usar o codigo http

}

function montarTelaResposta() {
    let lablePrevisao = document.getElementById('resposta-previsao');
    let lableProbabilidade = document.getElementById('resposta-probabilidade');
    lablePrevisao.textContent = "Previsão: " + ultimaPrevisao.previsao;
    lableProbabilidade.textContent = "Probabilidade: " + ultimaPrevisao.probabilidade;
}

function criarTelaResposta(modalResposta) {
    navegar('tela-resposta'); // tira a class collapse do elemento pai modalResposta
    montarTelaResposta();
    // const modalResposta = criarModalDeResposta();
    modalResposta.show();
}

function reiniciarApp() {
    limparVariavelUltimaPrevisao();
    limparFormulario();
    navegar('tela-home')
}

function limparVariavelUltimaPrevisao() {
    ultimaPrevisao = null;
}

function limparFormulario() {
    document.querySelector('form').reset();
}

function montarPayloadPrevisao() {
    //todo o front end precisa de validão do tipo dos
    // dados e validação para não enviar campo em branco. Como em IDOSO
    const payload = {
        genero: document.getElementById('genero').value,
        idoso: parseInt(document.getElementById('idoso').value),
        parceiro: parseInt(document.getElementById('parceiro').value),
        dependentes: parseInt(document.getElementById('dependentes').value),

        tempo_contrato_meses: parseInt(document.getElementById('tempo_contrato_meses').value),
        servico_telefone: parseInt(document.getElementById('servico_telefone').value),
        linhas_multiplas: document.getElementById('linhas_multiplas').value,
        tipo_internet: document.getElementById('tipo_internet').value,
        seguranca_online: document.getElementById('seguranca_online').value,
        backup_online: document.getElementById('backup_online').value,
        protecao_dispositivo: document.getElementById('protecao_dispositivo').value,
        suporte_tecnico: document.getElementById('suporte_tecnico').value,
        streaming_tv: document.getElementById('streaming_tv').value,
        streaming_filmes: document.getElementById('streaming_filmes').value,
        tipo_contrato: document.getElementById('tipo_contrato').value,
        cobranca_digital: parseInt(document.getElementById('cobranca_digital').value),
        metodo_pagamento: document.getElementById('metodo_pagamento').value,
        cobranca_mensal: parseFloat(document.getElementById('cobranca_mensal').value),
        cobranca_total: parseFloat(document.getElementById('cobranca_total').value)
    };
    return payload;
}


async function verificaCampoVazioNoFormulario() {
    let formularioValido = true;
    const form = document.querySelector('form');
    const campos = form.querySelectorAll('input, select');

    campos.forEach(function (campo) {
        if (!campo.value || campo.value.trim() === "") {
            formularioValido = false;
            campo.classList.add("is-invalid");
        } else {
            campo.classList.remove("is-invalid");
        }

    })
    if (formularioValido) {
        //atencao a esse await
        await preverCancelamento();
    }
}

function apresentarModalDeCarregamento() {
    const modalElement = document.getElementById('modalCarregamento');
    const modalLoading = new bootstrap.Modal(modalElement);
    modalLoading.show();
    return modalLoading;
}

function criarModalDeResposta(){
    const modalElement = document.getElementById('centeredModal');
    const modalResposta = new bootstrap.Modal(modalElement);
    // modalResposta.show();
    return modalResposta;
}

function apresentarModalDeErro(modalResposta){
    navegar('tela-resposta');
    let lablePrevisao = document.getElementById('resposta-previsao');
    let lableProbabilidade = document.getElementById('resposta-probabilidade');
    lablePrevisao.textContent = "Previsão: Erro ";
    lableProbabilidade.textContent = "Probabilidade: Erro ";
    modalResposta.show();
}


window.preverCancelamento = preverCancelamento;
window.navegar = navegar;
window.reiniciarApp = reiniciarApp;


window.verificaCampoVazioNoFormulario = verificaCampoVazioNoFormulario;

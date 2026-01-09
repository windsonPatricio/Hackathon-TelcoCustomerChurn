const API_URL = "http://localhost:8080/reter/test";


async function preverCancelamento() {

    let payload = montarPayloadPrevisao()

    try {
        const response = await axios.post(API_URL, payload);
    } catch (error) {
        console.log("Erro na requisição:" + error);
        if (error.response) {
            console.log("Erro no servidor: " + error.response.status);
        } else {
            console.log("Erro de conexão. Verifique se o servidor está rodando.");
        }
    }
}

function montarPayloadPrevisao() {

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
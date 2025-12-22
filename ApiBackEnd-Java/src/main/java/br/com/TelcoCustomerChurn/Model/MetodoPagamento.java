package br.com.TelcoCustomerChurn.Model;

import com.fasterxml.jackson.annotation.JsonValue;

public enum MetodoPagamento {
    CARTAO_CREDITO_AUTOMATICA("cartao_credito_automatica"),
    CHEQUE_ELETRONICO("cheque_eletronico"),
    CHEQUE_ENVIADO("cheque_enviado"),
    TRANSFERENCIA_BANCARIA_AUTOMATICA("transferencia_bancaria_automatica");

    private final String descricao;

    MetodoPagamento(String descricao) {
        this.descricao = descricao;
    }

    @JsonValue
    public String getDescricao() {
        return descricao;
    }
}

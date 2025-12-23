package br.com.ReterMais.model;

import com.fasterxml.jackson.annotation.JsonValue;

public enum TipoContrato {
    DOIS_ANOS("dois_anos"),
    MENSAL("mensal"),
    UM_ANO("um_ano");

    private final String descricao;

    TipoContrato(String descricao) {
        this.descricao = descricao;
    }

    @JsonValue
    public String getDescricao() {
        return descricao;
    }
}

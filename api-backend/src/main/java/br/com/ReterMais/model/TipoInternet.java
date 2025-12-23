package br.com.ReterMais.model;

import com.fasterxml.jackson.annotation.JsonValue;

public enum TipoInternet {
    DSL("dsl"), FIBRA("fibra"), SEM_INTERNET("sem_internet");

    private final String descricao;

    TipoInternet(String descricao) {
        this.descricao = descricao;
    }

    @JsonValue
    public String getDescricao() {
        return descricao;
    }
}

package br.com.ReterMais.model;

import com.fasterxml.jackson.annotation.JsonValue;

public enum LinhasMultiplas {
    NAO("nao"),
    SEM_TELEFONE( "sem_telefone"),
    SIM("sim");

    private final String descricao;

    LinhasMultiplas(String descricao) {
        this.descricao = descricao;
    }

    @JsonValue
    public String getDescricao() {
        return descricao;
    }
}

package br.com.ReterMais.model;

import com.fasterxml.jackson.annotation.JsonValue;

public enum SegurancaOnline {
    NAO("nao"), SEM_INTERNET("sem_internet"), SIM("sim");

    private final String descricao;

    SegurancaOnline(String descricao) {
        this.descricao = descricao;
    }

    @JsonValue
    public String getDescricao() {
        return descricao;
    }
}

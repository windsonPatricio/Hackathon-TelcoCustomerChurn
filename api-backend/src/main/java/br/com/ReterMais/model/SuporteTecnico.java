package br.com.ReterMais.model;

import com.fasterxml.jackson.annotation.JsonValue;

public enum SuporteTecnico {
    NAO("nao"), SEM_INTERNET("sem_internet"), SIM("sim");

    private final String descricao;

    SuporteTecnico(String descricao) {
        this.descricao = descricao;
    }

    @JsonValue
    public String getDescricao() {
        return descricao;
    }
}

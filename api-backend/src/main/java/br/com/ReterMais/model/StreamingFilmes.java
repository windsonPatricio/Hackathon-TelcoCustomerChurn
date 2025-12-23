package br.com.ReterMais.model;

import com.fasterxml.jackson.annotation.JsonValue;

public enum StreamingFilmes {
    NAO("nao"), SEM_INTERNET("sem_internet"), SIM("sim");

    private final String descricao;

    StreamingFilmes(String descricao) {
        this.descricao = descricao;
    }

    @JsonValue
    public String getDescricao() {
        return descricao;
    }
}

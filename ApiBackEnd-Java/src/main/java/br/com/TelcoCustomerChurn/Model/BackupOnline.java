package br.com.TelcoCustomerChurn.Model;

import com.fasterxml.jackson.annotation.JsonValue;

public enum BackupOnline {
    NAO("nao"), SEM_INTERNET("sem_internet"), SIM("sim");

    private final String descricao;

    BackupOnline (String descricao){
        this.descricao = descricao;
    }

    @JsonValue
    public String getDescricao() {
        return descricao;
    }
}

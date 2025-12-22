package br.com.TelcoCustomerChurn.Model;

import com.fasterxml.jackson.annotation.JsonValue;

public enum Genero {
    HOMEM("homem"), MULHER("mulher");

    private final String descricao;

    Genero(String descricao){
        this.descricao = descricao;
    }

    @JsonValue
    public String getDescricao(){
        return descricao;
    }
}

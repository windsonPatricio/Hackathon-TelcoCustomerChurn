package br.com.retermais.dtos;

import org.springframework.validation.FieldError;

public record ErroValidacaoDTO(
        String campo,
        String mensagem
) {
    public ErroValidacaoDTO(FieldError error) {
        this(toSnakeCase(error.getField()), error.getDefaultMessage());
    }

    private static String toSnakeCase(String camelCase) {
        return camelCase.replaceAll("([a-z])([A-Z])", "$1_$2").toLowerCase();
    }
}

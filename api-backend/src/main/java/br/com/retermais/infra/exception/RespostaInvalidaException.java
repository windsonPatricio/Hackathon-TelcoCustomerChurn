package br.com.retermais.infra.exception;

public class RespostaInvalidaException extends RuntimeException {

    public RespostaInvalidaException(String message) {
        super(message);
    }
}

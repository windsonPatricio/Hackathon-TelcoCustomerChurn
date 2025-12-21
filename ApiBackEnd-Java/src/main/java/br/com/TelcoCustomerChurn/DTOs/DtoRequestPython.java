package br.com.TelcoCustomerChurn.DTOs;

public record DtoRequestPython(
        Integer tempoDeContrato,
        Integer atrasoDePagamento,
        double usoMensal,
        String plano,
        double mensalidade,
        String tipoDeContrato,
        String metodoPagamento) {
}

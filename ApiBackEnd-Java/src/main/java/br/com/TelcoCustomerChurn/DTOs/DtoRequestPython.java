package br.com.TelcoCustomerChurn.DTOs;

import br.com.TelcoCustomerChurn.Model.*;

import java.math.BigDecimal;

/**
 * Sobre algumas escolhas:
 * Nome das variaveis =
 * Booleanos = escolhido visando a praticidade de uso na API
 * BigDecimal = escolha padrão para lidar com valores monetários.
 * Comentei algumas variaveis que não vi no contrato
 *
 * todo: Suponho que vamos precisar alterar esses campos que representam booleanos
 * , para verdadeiros booleanos. Visando uma api escalavel
 *
 *         Boolean idoso,
 *         Boolean parceiro,
 *         Boolean dependentes,
 *         Boolean servicoTelefone
 *         Boolean cobrancaDigital
 *
 * Trazer booleanos, implica em criar um méthodo em service que converta de
 * true/false para 1/0.
 */


public record DtoRequestPython(
        Genero genero,
        Integer idoso,
        Integer parceiro,
        Integer dependentes,
        Integer tempoContratoMeses,
        Integer servicoTelefone,
        LinhasMultiplas linhasMultiplas,
        TipoInternet tipoInternet,
        SegurancaOnline segurancaOnline,
        BackupOnline backupOnline,
        ProtecaoDispositivo protecaoDispositivo,
        SuporteTecnico suporteTecnico,
        StreamingTv streamingTv,
        StreamingFilmes streamingFilmes,
        TipoContrato tipoContrato,
        Integer cobrancaDigital,
        MetodoPagamento metodoPagamento,
        BigDecimal cobrancaMensal,
        BigDecimal cobrancaTotal
//        Integer atrasoDePagamento, Não vi isso na tabela de campos
//        double usoMensal,
//        String plano,
//        double mensalidade,
        ) {
}

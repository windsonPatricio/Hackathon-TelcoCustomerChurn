package br.com.retermais.dtos;

import br.com.retermais.model.*;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;

import java.math.BigDecimal;

public record RequestDTO(
        @NotNull(message = "{genero.notnull}")
        @JsonProperty("genero")
        Genero genero,

        @NotNull(message = "{idoso.notnull}")
        @Min(value = 0, message = "{boolean.01}")
        @Max(value = 1, message = "{boolean.01}")
        @JsonProperty("idoso")
        Integer idoso,

        @NotNull(message = "{parceiro.notnull}")
        @Min(value = 0, message = "{boolean.01}")
        @Max(value = 1, message = "{boolean.01}")
        @JsonProperty("parceiro")
        Integer parceiro,

        @NotNull(message = "{dependentes.notnull}")
        @Min(value = 0, message = "{boolean.01}")
        @Max(value = 1, message = "{boolean.01}")
        @JsonProperty("dependentes")
        Integer dependentes,

        @NotNull(message = "{tempo_contrato_meses.notnull}")
        @PositiveOrZero(message = "{positivo.zero}")
        @JsonProperty("tempo_contrato_meses")
        Integer tempoContratoMeses,

        @NotNull(message = "{servico_telefone.notnull}")
        @Min(value = 0, message = "{boolean.01}")
        @Max(value = 1, message = "{boolean.01}")
        @JsonProperty("servico_telefone")
        Integer servicoTelefone,

        @NotNull(message = "{linhas_multiplas.notnull}")
        @JsonProperty("linhas_multiplas")
        LinhasMultiplas linhasMultiplas,

        @NotNull(message = "{tipo_internet.notnull}")
        @JsonProperty("tipo_internet")
        TipoInternet tipoInternet,

        @NotNull(message = "{seguranca_online.notnull}")
        @JsonProperty("seguranca_online")
        SegurancaOnline segurancaOnline,

        @NotNull(message = "{backup_online.notnull}")
        @JsonProperty("backup_online")
        BackupOnline backupOnline,

        @NotNull(message = "{protecao_dispositivo.notnull}")
        @JsonProperty("protecao_dispositivo")
        ProtecaoDispositivo protecaoDispositivo,

        @NotNull(message = "{suporte_tecnico.notnull}")
        @JsonProperty("suporte_tecnico")
        SuporteTecnico suporteTecnico,

        @NotNull(message = "{streaming_tv.notnull}")
        @JsonProperty("streaming_tv")
        StreamingTv streamingTv,

        @NotNull(message = "{streaming_filmes.notnull}")
        @JsonProperty("streaming_filmes")
        StreamingFilmes streamingFilmes,

        @NotNull(message = "{tipo_contrato.notnull}")
        @JsonProperty("tipo_contrato")
        TipoContrato tipoContrato,

        @NotNull(message = "{cobranca_digital.notnull}")
        @Min(value = 0, message = "{boolean.01}")
        @Max(value = 1, message = "{boolean.01}")
        @JsonProperty("cobranca_digital")
        Integer cobrancaDigital,

        @NotNull(message = "{metodo_pagamento.notnull}")
        @JsonProperty("metodo_pagamento")
        MetodoPagamento metodoPagamento,

        @NotNull(message = "{cobranca_mensal.notnull}")
        @DecimalMin(value = "0.0", message = "{nao.negativo}")
        @JsonProperty("cobranca_mensal")
        BigDecimal cobrancaMensal,

        @NotNull(message = "{cobranca_total.notnull}")
        @DecimalMin(value = "0.0", message = "{nao.negativo}")
        @JsonProperty("cobranca_total")
        BigDecimal cobrancaTotal) {
}

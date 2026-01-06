package br.com.retermais.dtos;

import br.com.retermais.model.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;

import java.math.BigDecimal;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record RequestDTO(
        @NotBlank
        @Pattern(regexp = "\\d{11}")
        String idCliente,
        @NotNull
        Genero genero,
        @NotNull
        Integer idoso,
        @NotNull
        Integer parceiro,
        @NotNull
        Integer dependentes,
        @NotNull
        Integer tempoContratoMeses,
        @NotNull
        Integer servicoTelefone,
        @NotNull
        LinhasMultiplas linhasMultiplas,
        @NotNull
        TipoInternet tipoInternet,
        @NotNull
        SegurancaOnline segurancaOnline,
        @NotNull
        BackupOnline backupOnline,
        @NotNull
        ProtecaoDispositivo protecaoDispositivo,
        @NotNull
        SuporteTecnico suporteTecnico,
        @NotNull
        StreamingTv streamingTv,
        @NotNull
        StreamingFilmes streamingFilmes,
        @NotNull
        TipoContrato tipoContrato,
        @NotNull
        Integer cobrancaDigital,
        @NotNull
        MetodoPagamento metodoPagamento,
        @NotNull
        BigDecimal cobrancaMensal,
        @NotNull
        BigDecimal cobrancaTotal) {
}

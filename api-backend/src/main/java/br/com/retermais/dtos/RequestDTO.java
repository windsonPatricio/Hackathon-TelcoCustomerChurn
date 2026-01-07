package br.com.retermais.dtos;

import br.com.retermais.model.*;
import jakarta.validation.constraints.*;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;

import java.math.BigDecimal;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record RequestDTO(

        @NotNull(message = "Gênero é obrigatório")
        Genero genero,
        @NotNull(message = "O campo idoso é obrigatório (0 ou 1)")
        @Min(0) @Max(1)
        Integer idoso,
        @NotNull(message = "O campo parceiro é obrigatório (0 ou 1)")
        @Min(0) @Max(1)
        Integer parceiro,
        @NotNull(message = "O campo dependentes é obrigatório (0 ou 1)")
        @Min(0) @Max(1)
        Integer dependentes,
        @NotNull(message = "O tempo de contrato em meses é obrigatório")
        @PositiveOrZero(message = "O tempo de contrato deve ser zero ou positivo")
        Integer tempoContratoMeses,
        @NotNull(message = "Serviço de telefone é obrigatório (0 ou 1)")
        @Min(0) @Max(1)
        Integer servicoTelefone,
        @NotNull(message = "Linhas múltiplas é obrigatório")
        LinhasMultiplas linhasMultiplas,
        @NotNull(message = "Tipo de internet é obrigatório")
        TipoInternet tipoInternet,
        @NotNull(message = "Segurança online é obrigatório")
        SegurancaOnline segurancaOnline,
        @NotNull(message = "Backup online é obrigatório")
        BackupOnline backupOnline,
        @NotNull(message = "Proteção de dispositivo é obrigatório")
        ProtecaoDispositivo protecaoDispositivo,
        @NotNull(message = "Suporte técnico é obrigatório")
        SuporteTecnico suporteTecnico,
        @NotNull(message = "Streaming de TV é obrigatório")
        StreamingTv streamingTv,
        @NotNull(message = "Streaming de filmes é obrigatório")
        StreamingFilmes streamingFilmes,
        @NotNull(message = "Tipo de contrato é obrigatório")
        TipoContrato tipoContrato,
        @NotNull(message = "Cobrança digital é obrigatório (0 ou 1)")
        @Min(0) @Max(1)
        Integer cobrancaDigital,
        @NotNull(message = "Método de pagamento é obrigatório")
        MetodoPagamento metodoPagamento,
        @NotNull(message = "Cobrança mensal é obrigatória")
        @DecimalMin(value = "0.0", message = "Cobrança mensal não pode ser negativa")
        BigDecimal cobrancaMensal,
        @NotNull(message = "Cobrança total é obrigatória")
        @DecimalMin(value = "0.0", message = "Cobrança total não pode ser negativa")
        BigDecimal cobrancaTotal) {
}

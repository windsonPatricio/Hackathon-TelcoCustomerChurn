package br.com.retermais.dtos;

import br.com.retermais.model.*;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;

import java.math.BigDecimal;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record RequestPythonDTO(
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
        BigDecimal cobrancaTotal) {
}

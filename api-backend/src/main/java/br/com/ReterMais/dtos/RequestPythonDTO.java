package br.com.ReterMais.dtos;

import br.com.ReterMais.model.*;

import java.math.BigDecimal;

public record RequestPythonDTO(Genero genero,
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

package br.com.retermais.mapper;

import br.com.retermais.dtos.RequestDTO;
import br.com.retermais.dtos.RequestPythonDTO;
import org.springframework.stereotype.Component;

@Component
public class RequestPythonMapper {

    public RequestPythonMapper() {
    }

    public static RequestPythonDTO toPythonDTO(RequestDTO request) {

        return new RequestPythonDTO(
                request.genero(),
                request.idoso(),
                request.parceiro(),
                request.dependentes(),
                request.tempoContratoMeses(),
                request.servicoTelefone(),
                request.linhasMultiplas(),
                request.tipoInternet(),
                request.segurancaOnline(),
                request.backupOnline(),
                request.protecaoDispositivo(),
                request.suporteTecnico(),
                request.streamingTv(),
                request.streamingFilmes(),
                request.tipoContrato(),
                request.cobrancaDigital(),
                request.metodoPagamento(),
                request.cobrancaMensal(),
                request.cobrancaTotal()

        );
    }
}

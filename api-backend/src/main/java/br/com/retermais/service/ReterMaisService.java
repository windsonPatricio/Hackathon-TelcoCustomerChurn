package br.com.retermais.service;

import br.com.retermais.client.fastapi.FastApiClient;
import br.com.retermais.dtos.RequestDTO;
import br.com.retermais.dtos.ResponsePythonDTO;
import br.com.retermais.infra.exception.RespostaInvalidaException;
import br.com.retermais.mapper.RequestPythonMapper;
import org.springframework.stereotype.Service;

@Service
public class ReterMaisService {

    private final FastApiClient fastApiClient;

    public ReterMaisService(FastApiClient fastApiClient) {
        this.fastApiClient = fastApiClient;
    }

    public ResponsePythonDTO preverCancelamento(RequestDTO requestDTO) throws RespostaInvalidaException {
        var resposta = fastApiClient.predict(
                RequestPythonMapper.toPythonDTO(requestDTO)
        );

        if (resposta == null || resposta.previsao() == null || resposta.probabilidade() == null) {
            throw new RespostaInvalidaException("Resposta inválida retornada pela API externa");
        }

        return resposta;
    }
}

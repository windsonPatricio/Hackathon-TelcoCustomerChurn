package br.com.retermais.service;

import br.com.retermais.client.fastapi.FastApiClient;
import br.com.retermais.dtos.RequestDTO;
import br.com.retermais.dtos.RequestPythonDTO;
import br.com.retermais.dtos.ResponsePythonDTO;
import br.com.retermais.mapper.RequestPythonMapper;
import org.springframework.stereotype.Service;

@Service
public class ReterMaisService {

    private final FastApiClient fastApiClient;

    public ReterMaisService(FastApiClient fastApiClient) {
        this.fastApiClient = fastApiClient;
    }

    public ResponsePythonDTO preverCancelamento(RequestDTO requestDTO) {
        RequestPythonDTO request = RequestPythonMapper.toPythonDTO(requestDTO);
        return fastApiClient.predict(request);
    }
}

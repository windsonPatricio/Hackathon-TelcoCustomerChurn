package br.com.retermais.client.fastapi;

import br.com.retermais.dtos.RequestPythonDTO;
import br.com.retermais.dtos.ResponsePythonDTO;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.PostExchange;

@HttpExchange
public interface FastApiClient {

    @PostExchange("/predict")
    ResponsePythonDTO predict(@Valid @RequestBody RequestPythonDTO requestPythonDTO);
}

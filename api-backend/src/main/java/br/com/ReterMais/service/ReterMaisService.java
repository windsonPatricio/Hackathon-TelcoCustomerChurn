package br.com.ReterMais.service;


import br.com.ReterMais.dtos.ResponsePythonDTO;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class ReterMaisService {

    private final WebClient webClient;

    //Conexao com o modelo
    public ReterMaisService(WebClient.Builder builder){
        this.webClient = builder
                .baseUrl("enderecoModelo")
                .build();
    }

    public ResponsePythonDTO preverCancelamento (ResponsePythonDTO request){

        //consulta o modelo atraves da requisicao, e retorna os valores de resposta do modelo.
        return webClient.post()
                .uri("/prever")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(ResponsePythonDTO.class)
                .block();
    }

}

package br.com.TelcoCustomerChurn.Service;


import br.com.TelcoCustomerChurn.DTOs.DtoReponsePython;
import br.com.TelcoCustomerChurn.DTOs.DtoRequestPython;
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

    public DtoReponsePython preverCancelamento (DtoRequestPython request){

        //consulta o modelo atraves da requisicao, e retorna os valores de resposta do modelo.
        return webClient.post()
                .uri("/prever")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(DtoReponsePython.class)
                .block();
    }

}

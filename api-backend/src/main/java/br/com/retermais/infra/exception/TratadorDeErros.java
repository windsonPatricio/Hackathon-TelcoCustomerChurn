package br.com.retermais.infra.exception;

import br.com.retermais.dtos.ErroDTO;
import br.com.retermais.dtos.ErroValidacaoDTO;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClientException;

import java.net.ConnectException;
import java.util.List;

@RestControllerAdvice
public class TratadorDeErros {

    // 400 - Erro de validação
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<List<ErroValidacaoDTO>> tratarErroValidacao(MethodArgumentNotValidException ex) {

        var erros = ex.getFieldErrors()
                .stream()
                .map(ErroValidacaoDTO::new)
                .toList();

        return ResponseEntity.badRequest().body(erros);
    }

    // 400 - JSON inválido / contrato quebrado
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErroDTO> tratarJsonInvalido() {

        return ResponseEntity.badRequest()
                .body(new ErroDTO("JSON inválido ou incompatível com o contrato da API."));
    }

    // 503 - FastAPI indisponível
    @ExceptionHandler({ResourceAccessException.class, ConnectException.class})
    public ResponseEntity<ErroDTO> tratarErroConexao() {

        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                .body(new ErroDTO("O serviço FastAPI está indisponível no momento."));
    }

    // 502 - Erro de integração / contrato externo
    @ExceptionHandler(RestClientException.class)
    public ResponseEntity<ErroDTO> tratarErroIntegracao() {

        return ResponseEntity.status(HttpStatus.BAD_GATEWAY)
                .body(new ErroDTO("Falha na comunicação ou contrato inválido com a API externa."));
    }

    // 502 - Trata resposta inválida da FastAPI
    @ExceptionHandler(RespostaInvalidaException.class)
    public ResponseEntity<ErroDTO> tratarRespostaInvalida(RespostaInvalidaException ex) {

        return ResponseEntity.status(HttpStatus.BAD_GATEWAY)
                .body(new ErroDTO(ex.getMessage()));
    }

    // 500 - Erro inesperado
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErroDTO> tratarErroInesperado() {

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(new ErroDTO("Erro interno inesperado."));
    }
}

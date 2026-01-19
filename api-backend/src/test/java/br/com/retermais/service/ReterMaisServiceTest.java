package br.com.retermais.service;

import br.com.retermais.client.fastapi.FastApiClient;
import br.com.retermais.dtos.RequestDTO;
import br.com.retermais.dtos.ResponsePythonDTO;
import br.com.retermais.infra.exception.RespostaInvalidaException;
import br.com.retermais.model.*;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class ReterMaisServiceTest {

    @Mock
    private FastApiClient fastApiClient;

    @InjectMocks
    private ReterMaisService service;

    private RequestDTO requestValido() {
        return new RequestDTO(
                Genero.HOMEM,
                0,
                1,
                0,
                12,
                1,
                LinhasMultiplas.NAO,
                TipoInternet.FIBRA,
                SegurancaOnline.SIM,
                BackupOnline.SIM,
                ProtecaoDispositivo.SIM,
                SuporteTecnico.SIM,
                StreamingTv.NAO,
                StreamingFilmes.SIM,
                TipoContrato.UM_ANO,
                1,
                MetodoPagamento.CARTAO_CREDITO_AUTOMATICA,
                BigDecimal.valueOf(99.90),
                BigDecimal.valueOf(1199.00)
        );
    }

    @Test
    @DisplayName("Deve retornar a previsão corretamente quando a API externa responde com sucesso")
    void deveRetornarPrevisaoComSucesso() {
        var mockResponse = new ResponsePythonDTO("Vai cancelar", 0.85);
        when(fastApiClient.predict(any())).thenReturn(mockResponse);

        var resultado = service.preverCancelamento(requestValido());

        assertNotNull(resultado);
        assertEquals("Vai cancelar", resultado.previsao());
        assertEquals(0.85, resultado.probabilidade());
    }

    @Test
    @DisplayName("Deve lançar RespostaInvalidaException quando a API externa retornar null")
    void deveLancarExcecaoQuandoRespostaForNula() {
        when(fastApiClient.predict(any())).thenReturn(null);

        assertThrows(RespostaInvalidaException.class,
                () -> service.preverCancelamento(requestValido()));
    }

    @Test
    @DisplayName("Deve lançar RespostaInvalidaException quando a previsão da API externa vier nula")
    void deveLancarExcecaoQuandoCampoObrigatorioForNull() {
        when(fastApiClient.predict(any()))
                .thenReturn(new ResponsePythonDTO(null, 0.75));

        assertThrows(RespostaInvalidaException.class,
                () -> service.preverCancelamento(requestValido()));
    }

    @Test
    @DisplayName("Deve lançar RespostaInvalidaException quando todos os campos da resposta forem nulos")
    void deveLancarErroQuandoRespostaForInvalida() {
        when(fastApiClient.predict(any()))
                .thenReturn(new ResponsePythonDTO(null, null));

        assertThrows(RespostaInvalidaException.class,
                () -> service.preverCancelamento(requestValido()));
    }

    @Test
    @DisplayName("Deve lançar RespostaInvalidaException quando a probabilidade da API externa vier nula")
    void deveLancarExcecaoQuandoProbabilidadeForNull() {
        when(fastApiClient.predict(any()))
                .thenReturn(new ResponsePythonDTO("Vai cancelar", null));

        assertThrows(RespostaInvalidaException.class,
                () -> service.preverCancelamento(requestValido()));
    }

    @Test
    @DisplayName("Deve lançar RespostaInvalidaException quando o objeto de resposta for retornado nulo pela API")
    void deveLancarExcecaoQuandoRetornoTotalForNull() {
        when(fastApiClient.predict(any())).thenReturn(null);

        assertThrows(RespostaInvalidaException.class,
                () -> service.preverCancelamento(requestValido()));
    }
}

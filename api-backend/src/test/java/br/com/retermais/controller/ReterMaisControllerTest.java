package br.com.retermais.controller;

import br.com.retermais.dtos.ResponsePythonDTO;
import br.com.retermais.service.ReterMaisService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest
public class ReterMaisControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private ReterMaisService service;

    private static final String JSON_VALIDO = """
            {
                "genero": "homem",
                "idoso": 0,
                "parceiro": 1,
                "dependentes": 0,
                "tempo_contrato_meses": 12,
                "servico_telefone": 1,
                "linhas_multiplas": "nao",
                "tipo_internet": "fibra",
                "seguranca_online": "sim",
                "backup_online": "nao",
                "protecao_dispositivo": "nao",
                "suporte_tecnico": "nao",
                "streaming_tv": "sim",
                "streaming_filmes": "sim",
                "tipo_contrato": "mensal",
                "cobranca_digital": 1,
                "metodo_pagamento": "cheque_eletronico",
                "cobranca_mensal": 79.85,
                "cobranca_total": 1200.50
            }
            """;

    @Test
    @DisplayName("Deve retornar 200 e a previsão quando o payload for válido")
    void deveRetornar200ComPayloadValido() throws Exception {
        var mockResponse = new ResponsePythonDTO("Não vai cancelar", 0.15);

        when(service.preverCancelamento(any())).thenReturn(mockResponse);

        mockMvc.perform(post("/reter/prever")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(JSON_VALIDO))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.previsao").value("Não vai cancelar"))
                .andExpect(jsonPath("$.probabilidade").value(0.15));
    }

    @Test
    @DisplayName("Deve retornar 400 quando o payload estiver vazio")
    void deveRetornar400ComPayloadInvalido() throws Exception {
        mockMvc.perform(post("/reter/prever")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isBadRequest());
    }

    @Test
    @DisplayName("Deve retornar 400 Bad Request quando campos obrigatórios não forem enviados")
    void deveRetornar400QuandoJSONEstiverIncompleto() throws Exception {
        String jsonInvalido = "{\"genero\": \"homem\"}";

        mockMvc.perform(post("/reter/prever")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(jsonInvalido))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$").isArray())
                .andExpect(jsonPath("$[0].campo").exists())
                .andExpect(jsonPath("$[0].mensagem").exists());
    }

    @Test
    @DisplayName("Deve retornar 400 quando campos numéricos estiverem fora do limite (0 ou 1)")
    void deveRetornar400QuandoValoresForaDoLimite() throws Exception {
        String jsonLimiteInvalido = JSON_VALIDO.replace("\"idoso\": 0", "\"idoso\": 2");

        mockMvc.perform(post("/reter/prever")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(jsonLimiteInvalido))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$[0].mensagem").value("O campo deve ser 0 ou 1"));
    }

    @Test
    @DisplayName("Deve retornar 400 quando o JSON for sintaticamente inválido (erro de vírgula ou chaves)")
    void deveRetornar400QuandoJsonMalformado() throws Exception {
        String jsonComErroSintaxe = "{ genero: homem, \"idoso\" 0 }";

        mockMvc.perform(post("/reter/prever")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(jsonComErroSintaxe))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.erro").value("JSON inválido ou incompatível com o contrato da API."));
    }

    @Test
    @DisplayName("Deve retornar 502 Bad Gateway quando o Service lançar RespostaInvalidaException")
    void deveRetornar502QuandoServiceFalhar() throws Exception {
        when(service.preverCancelamento(any()))
                .thenThrow(new br.com.retermais.infra.exception.RespostaInvalidaException("Falha na API externa"));

        mockMvc.perform(post("/reter/prever")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(JSON_VALIDO))
                .andExpect(status().isBadGateway())
                .andExpect(jsonPath("$.erro").value("Falha na API externa"));
    }

    @Test
    @DisplayName("Deve retornar 503 Service Unavailable quando o FastAPI estiver fora do ar")
    void deveRetornar503QuandoFastApiIndisponivel() throws Exception {
        when(service.preverCancelamento(any()))
                .thenThrow(new org.springframework.web.client.ResourceAccessException("Connection refused"));

        mockMvc.perform(post("/reter/prever")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(JSON_VALIDO))
                .andExpect(status().isServiceUnavailable())
                .andExpect(jsonPath("$.erro").value("O serviço FastAPI está indisponível no momento."));
    }

    @DisplayName("Deve retornar 503 quando houver falha de conexão física com o servidor Python")
    void deveRetornar503QuandoHouverFalhaDeConexao() throws Exception {
        when(service.preverCancelamento(any()))
                .thenThrow(new org.springframework.web.client.ResourceAccessException("I/O error on POST request"));

        mockMvc.perform(post("/reter/prever")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(JSON_VALIDO))
                .andExpect(status().isServiceUnavailable())
                .andExpect(jsonPath("$.erro").value("O serviço FastAPI está indisponível no momento."));
    }
}

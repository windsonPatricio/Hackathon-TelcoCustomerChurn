package br.com.retermais.controller;

import br.com.retermais.dtos.RequestDTO;
import br.com.retermais.dtos.ResponsePythonDTO;
import br.com.retermais.service.ReterMaisService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/reter")
@Tag(name = "Retenção", description = "Endpoints para previsão de churn de clientes")
public class ReterMaisController {

    private final ReterMaisService service;

    public ReterMaisController(ReterMaisService service) {
        this.service = service;
    }

    @Operation(summary = "Prever cancelamento")
    @ApiResponse(responseCode = "400", description = "Erro de validação ou JSON inválido")
    @ApiResponse(responseCode = "502", description = "Erro de integração com a FastAPI")
    @ApiResponse(responseCode = "503", description = "FastAPI indisponível")
    @ApiResponse(responseCode = "500", description = "Erro interno")
    @PostMapping("/prever")
    public ResponseEntity<ResponsePythonDTO> prever(@Valid @RequestBody RequestDTO request) {
        ResponsePythonDTO response = service.preverCancelamento(request);
        return ResponseEntity.ok(response);
    }
}

package br.com.ReterMais.controller;

import br.com.ReterMais.dtos.RequestDTO;
import br.com.ReterMais.dtos.ResponsePythonDTO;
import br.com.ReterMais.service.ReterMaisService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/reter")
public class ReterMaisController {

    private final ReterMaisService reterMaisService;

    public ReterMaisController(ReterMaisService reterMaisService) {
        this.reterMaisService = reterMaisService;
    }

    @PostMapping("/prever")
    public ResponseEntity<ResponsePythonDTO> prever(@Valid @RequestBody RequestDTO request) {
        ResponsePythonDTO response = reterMaisService.preverCancelamento(request);
        return ResponseEntity.ok(response);
    }
}

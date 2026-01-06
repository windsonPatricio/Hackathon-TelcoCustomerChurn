package br.com.retermais.controller;

import br.com.retermais.dtos.RequestDTO;
import br.com.retermais.dtos.RequestPythonDTO;
import br.com.retermais.dtos.ResponsePythonDTO;
import br.com.retermais.service.ReterMaisService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/reter")
public class ReterMaisController {

    private final ReterMaisService service;

    public ReterMaisController(ReterMaisService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<ResponsePythonDTO> prever(@Valid @RequestBody RequestDTO request) {
        ResponsePythonDTO response = service.preverCancelamento(request);
        return ResponseEntity.ok(response);
    }
}

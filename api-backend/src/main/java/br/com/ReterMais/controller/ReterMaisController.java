package br.com.ReterMais.controller;

import br.com.ReterMais.dtos.RequestPythonDTO;
import br.com.ReterMais.dtos.ResponsePythonDTO;
import br.com.ReterMais.dtos.ResponsePythonDTO;
import br.com.ReterMais.service.ReterMaisService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/reter")
public class ReterMaisController {

        private final ReterMaisService reterMaisService;

        public ReterMaisController (ReterMaisService reterMaisService){
            this.reterMaisService = reterMaisService;
        }

        //requisicao atraves do envio do dados, para o modelo, atraves do service
        @PostMapping("/prever")
        public ResponseEntity<ResponsePythonDTO> prever(@RequestBody RequestPythonDTO requestPython){
            ResponsePythonDTO response = reterMaisService.preverCancelamento(requestPython);
            return ResponseEntity.ok(response);
        }


}

package br.com.TelcoCustomerChurn.Controller;


import br.com.TelcoCustomerChurn.DTOs.DtoReponsePython;
import br.com.TelcoCustomerChurn.DTOs.DtoRequestPython;
import br.com.TelcoCustomerChurn.Service.ReterMaisService;
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
        public ResponseEntity<DtoReponsePython> prever(@RequestBody DtoRequestPython requestPython){
            DtoReponsePython response = reterMaisService.preverCancelamento(requestPython);
            return ResponseEntity.ok(response);
        }


}

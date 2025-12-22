package br.com.TelcoCustomerChurn;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class TelcoCustomerChurnApplication {

	public static void main(String[] args) {
		SpringApplication.run(TelcoCustomerChurnApplication.class, args);
	}

}

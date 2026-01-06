package br.com.retermais.config;

import br.com.retermais.client.fastapi.FastApiClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.support.RestClientAdapter;
import org.springframework.web.service.invoker.HttpServiceProxyFactory;

@Configuration
public class FastApiClientConfig {

    @Bean
    RestClient fastApiRestClient(@Value("${api.url}") String baseUrl) {
        return RestClient.builder()
                .baseUrl(baseUrl)
                .build();
    }

    @Bean
    HttpServiceProxyFactory fastApiProxyFactory(RestClient restClient) {
        return HttpServiceProxyFactory.builder()
                .exchangeAdapter(RestClientAdapter.create(restClient))
                .build();
    }

    @Bean
    FastApiClient fastApiClient(HttpServiceProxyFactory factory) {
        return factory.createClient(FastApiClient.class);
    }
}

package dev.cdevents.visualiser;

import io.cloudevents.spring.mvc.CloudEventHttpMessageConverter;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class VisualisationApplication {

	public static void main(String[] args) {
		SpringApplication.run(VisualisationApplication.class, args);
	}

	@Bean
	public RestTemplate restTemplate() {
		RestTemplate restTemplate = new RestTemplate();
		restTemplate.getMessageConverters().add(0, new CloudEventHttpMessageConverter());
		return restTemplate;
	}
}

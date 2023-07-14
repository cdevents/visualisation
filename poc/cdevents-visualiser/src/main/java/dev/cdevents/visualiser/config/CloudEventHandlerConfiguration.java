package dev.cdevents.visualiser.config;

import io.cloudevents.spring.mvc.CloudEventHttpMessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.util.List;

@Configuration
public class CloudEventHandlerConfiguration implements WebMvcConfigurer {

    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
        converters.add(0, cloudEventHttpMessageConverter());
    }

    @Bean
    public CloudEventHttpMessageConverter cloudEventHttpMessageConverter() {
        return new CloudEventHttpMessageConverter();
    }
}

package dev.cdevents.visualiser.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import io.cloudevents.CloudEvent;
import io.cloudevents.spring.mvc.CloudEventHttpMessageConverter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.net.URI;

@ConditionalOnProperty("visualisation.cdeventsvisi.enabled")
@Service
public class CDEventsVisiService implements MonitorCDEvents {

    @Autowired
    RestTemplate restTemplate;
    @Value("${visualisation.cdeventsvisi.endpoint}")
    private String cdEventsVisiEndPoint;

    @Override
    public void processCDEvent(CloudEvent cdEvent) {
        System.out.println("IN CDEventsVisiService received CDEvent and posted to " + cdEventsVisiEndPoint);
        HttpHeaders headers = new HttpHeaders();
        headers.set("Ce-Id", cdEvent.getId());
        headers.set("Ce-Specversion", cdEvent.getSpecVersion().name());
        headers.set("Ce-Source", cdEvent.getSource().toString());
        headers.set("Ce-Type", cdEvent.getType());
        headers.setContentType(MediaType.APPLICATION_JSON);

        ResponseEntity<String> response = restTemplate.postForEntity(cdEventsVisiEndPoint, cdEvent, String.class, headers);

        System.out.println("Response Status Code from CDEvents Visi endpoint: " + response.getStatusCode());
    }

}

package dev.cdevents.visualiser.service;

import io.cloudevents.CloudEvent;
import io.cloudevents.spring.mvc.CloudEventHttpMessageConverter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@ConditionalOnProperty("visualisation.dbstore.enabled")
@Service
public class CDEventsDBService implements MonitorCDEvents {

    @Autowired
    RestTemplate restTemplate;

    @Value("${visualisation.grafanavisi.arangodb.endpoint}")
    private String arangoDBEndPoint;

    @Override
    public void processCDEvent(CloudEvent cdEvent) {
        System.out.println("IN CDEventsDBService received CDEvent");

        HttpHeaders headers = new HttpHeaders();
        headers.set("Ce-Id", cdEvent.getId());
        headers.set("Ce-Specversion", cdEvent.getSpecVersion().name());
        headers.set("Ce-Source", cdEvent.getSource().toString());
        headers.set("Ce-Type", cdEvent.getType());
        headers.setContentType(MediaType.APPLICATION_JSON);

        ResponseEntity<String> response = restTemplate.postForEntity(arangoDBEndPoint, cdEvent, String.class, headers);
        System.out.println("Response Status Code from Arango DB endpoint: " + response.getStatusCode());
    }

}

package dev.cdevents.visualiser.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import dev.cdevents.visualiser.service.MonitorCDEvents;
import io.cloudevents.CloudEvent;
import io.cloudevents.core.provider.EventFormatProvider;
import io.cloudevents.jackson.JsonFormat;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

import static com.fasterxml.jackson.databind.SerializationFeature.FAIL_ON_EMPTY_BEANS;

@RestController
@RequestMapping(value = "/cdevents")
public class MonitorCDEventsController {

    private List<MonitorCDEvents> monitorImplementations;

    @Autowired
    public MonitorCDEventsController(List<MonitorCDEvents> monitorImplementations) {
        this.monitorImplementations = monitorImplementations;
    }


    @RequestMapping(value = "/visualiser", method = RequestMethod.POST)
    public ResponseEntity<Void> receiveCDEvent(@RequestBody CloudEvent cdEvent){
        ObjectMapper objectMapper = new ObjectMapper();
        EventFormatProvider.getInstance().registerFormat(new JsonFormat());
        objectMapper.registerModule(JsonFormat.getCloudEventJacksonModule());
        objectMapper.disable(FAIL_ON_EMPTY_BEANS);

        try {
            System.out.println("Received CDEvent " + objectMapper.writeValueAsString(cdEvent));
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
        for (MonitorCDEvents monitorCDEvents : monitorImplementations) {
            monitorCDEvents.processCDEvent(cdEvent);
        }
        return ResponseEntity.ok().build();
    }
}

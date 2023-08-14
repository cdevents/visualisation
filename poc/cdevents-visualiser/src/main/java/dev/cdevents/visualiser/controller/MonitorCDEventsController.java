package dev.cdevents.visualiser.controller;

import dev.cdevents.visualiser.service.MonitorCDEvents;
import io.cloudevents.CloudEvent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RequestMapping(value = "/cdevents")
@RestController
public class MonitorCDEventsController {

    private List<MonitorCDEvents> monitorImplementations;

    @Autowired
    public MonitorCDEventsController(List<MonitorCDEvents> monitorImplementations) {
        this.monitorImplementations = monitorImplementations;
    }


    @RequestMapping(value = "/visualiser", method = RequestMethod.POST)
    public ResponseEntity<Void> receiveCDEvent(@RequestBody CloudEvent cdEvent){
	    System.out.println("Received CDEvent " + cdEvent.getType());
        for (MonitorCDEvents monitorCDEvents : monitorImplementations) {
            monitorCDEvents.processCDEvent(cdEvent);
        }
        return ResponseEntity.ok().build();
    }
}

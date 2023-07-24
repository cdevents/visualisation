package dev.cdevents.visualiser.controller;

import dev.cdevents.visualiser.service.MonitorCDEvents;
import io.cloudevents.CloudEvent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/cdevents")
@RestController
public class MonitorCDEventsController {

    private List<MonitorCDEvents> monitorImplementations;

    @Autowired
    public MonitorCDEventsController(List<MonitorCDEvents> monitorImplementations) {
        this.monitorImplementations = monitorImplementations;
    }


    @PostMapping("/visualiser")
    public ResponseEntity<Void> receiveCDEvent(@RequestBody CloudEvent cdEvent){
        for (MonitorCDEvents monitorCDEvents : monitorImplementations) {
            monitorCDEvents.processCDEvent(cdEvent);
        }
        return ResponseEntity.ok().build();
    }
}

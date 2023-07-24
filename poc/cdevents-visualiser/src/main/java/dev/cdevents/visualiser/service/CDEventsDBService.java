package dev.cdevents.visualiser.service;

import io.cloudevents.CloudEvent;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

@ConditionalOnProperty("visualisation.dbstore.enabled")
@Service
public class CDEventsDBService implements MonitorCDEvents {
    @Override
    public void processCDEvent(CloudEvent cdEvent) {
        System.out.println("IN CDEventsDBService received CDEvent");
    }

}

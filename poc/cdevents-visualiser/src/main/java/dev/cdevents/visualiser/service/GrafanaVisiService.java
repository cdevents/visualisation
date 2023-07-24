package dev.cdevents.visualiser.service;

import io.cloudevents.CloudEvent;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

@ConditionalOnProperty("visualisation.grafanavisi.enabled")
@Service
public class GrafanaVisiService implements MonitorCDEvents {
    @Override
    public void processCDEvent(CloudEvent cdEvent) {
        System.out.println("IN GrafanaVisiService received CDEvent");
        //Python API to be invoked
    }
}

package dev.cdevents.visualiser.service;

import io.cloudevents.CloudEvent;

public interface MonitorCDEvents {

    public void processCDEvent(CloudEvent cdEvent);

}

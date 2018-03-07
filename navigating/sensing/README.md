# SensorData
Listens for sensor events from sensing RPi over HTTP, and exposes a buffer
of events to caller.

## Quickstart
First start the SensorListener:
```
sl = SensorListener([port=8080])
sl.start()
```
The port argument is optional and defaults to 8080.

To get sensor data:
```
sl.get_camera_events([n=1])
```
This will return the `n` latest camera events. The method is not blocking and
will return an empty array if no events have been heard.
To get gps events:
```
sl.get_gps_events([n=1])
```

All the events will have a property called `timestamp` that corresponds to the
time the event was received. They will also have a property `payload` that
contains everything the sensor sent as a json body.

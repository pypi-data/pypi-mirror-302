# Otel-Metric-Base

**OtelMetricBase** is a simple base class for integrating with OpenTelemetry metrics. It provides an easy way to create and manage synchronous and asynchronous metrics such as counters, up-down counters, histograms, and observable gauges, while also supporting the ability to add tags (attributes) to the metrics.

## Features
- Create counters, up-down counters, histograms, and observable metrics.
- Easily attach tags (attributes) to the metrics for enriched observability.
- Supports OpenTelemetry OTLP protocol for exporting metrics.

## Usage

```python
from otel_metric_base.otel_metrics import OtelMetricBase

# Initialize OtelMetrics with OTLP endpoint
otel_metrics = OtelMetricBase(otlp_endpoint="http://localhost:4317")
```

### Create Synchronous Metrics

You can create counters, up-down counters, and histograms using the create_metric method. Optionally, you can pass tags (attributes) to the metrics.

**Example: Create a Counter with Tags**

```python
tags = {"environment": "production", "region": "us-east"}
```
### Create a counter with tags
```python
counter = otel_metrics.create_metric(
    metric_type="counter", 
    name="dynamic_counter", 
    description="A dynamic counter", 
    tags=tags
)
```

### Add to the counter and attach the tags
```python
counter.add(5, attributes=tags)
```
Create Observable Metrics
Observable metrics (like gauges, counters, and up-down counters) require a callback function that returns the current value of the metric.


### Create a callback function that returns the gauge value
```python
def get_gauge_value() -> float:
    return 42.0  # Replace with actual logic
```
### Create an observable gauge with a callback and tags
```python
observable_gauge_callback = otel_metrics.create_observable_callback(get_gauge_value)
otel_metrics.create_metric(
    metric_type="observable_gauge", 
    name="dynamic_gauge", 
    callback=observable_gauge_callback, 
    tags=tags
)
```
Create Observable Counters and UpDownCounters
The same structure applies for creating observable counters and up-down counters:


### Create an observable counter
```python
def get_counter_value() -> float:
    return 1.0

observable_counter_callback = otel_metrics.create_observable_callback(get_counter_value)
otel_metrics.create_metric(
    metric_type="observable_counter", 
    name="observable_counter", 
    callback=observable_counter_callback, 
    tags=tags
)
```
### Create an observable up-down counter

```python
def get_updown_counter_value() -> float:
    return -10.0

observable_updown_callback = otel_metrics.create_observable_callback(get_updown_counter_value)
otel_metrics.create_metric(
    metric_type="observable_up_down_counter", 
    name="observable_updown_counter", 
    callback=observable_updown_callback, 
    tags=tags
)
```

### Exporting Metrics
The OtelMetricBase class automatically sets up an OTLP exporter to export the metrics to the specified endpoint. Ensure you have an OpenTelemetry Collector or similar service running at the specified OTLP endpoint (http://localhost:4317 by default).

```python
class OtelMetricBase:
    def __init__(
        self, otlp_endpoint="http://localhost:4317", service_name="otel-metrics-service"
    ):
        # Initialize the Meter Provider with a dynamic service name
        resource = Resource(attributes={"service.name": service_name})

        # Set up the OTLP Exporter
        otlp_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
```



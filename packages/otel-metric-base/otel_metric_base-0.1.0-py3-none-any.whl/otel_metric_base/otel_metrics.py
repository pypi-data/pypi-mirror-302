from typing import Iterable, Callable, Dict
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import (
    CallbackOptions,
    Observation,
    get_meter_provider,
    set_meter_provider,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource


class OtelMetricBase:
    def __init__(
        self, otlp_endpoint="http://localhost:4317", service_name="otel-metrics-service"
    ):
        # Initialize the Meter Provider with a dynamic service name
        resource = Resource(attributes={"service.name": service_name})

        # Set up the OTLP Exporter
        otlp_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)

        # Use the OTLP Exporter with a PeriodicExportingMetricReader
        metric_reader = PeriodicExportingMetricReader(otlp_exporter)

        # Initialize the MeterProvider with the OTLP exporter
        self.meter_provider = MeterProvider(
            resource=resource, metric_readers=[metric_reader]
        )
        set_meter_provider(self.meter_provider)

        # Set up a meter instance that can be reused
        self.meter = get_meter_provider().get_meter("otel-metrics", "0.1.0")

    def create_metric(
        self,
        metric_type: str,
        name: str,
        description: str = "",
        unit: str = "1",
        callback: Callable = None,
        tags: Dict[str, str] = None  # Add tags argument
    ):
        """
        General method to create synchronous and asynchronous metrics.

        :param metric_type: 'counter', 'up_down_counter', 'histogram', 'observable_counter', 'observable_up_down_counter', or 'observable_gauge'.
        :param name: The name of the metric.
        :param description: Optional description of the metric.
        :param unit: Optional unit of measurement.
        :param callback: Optional callback for async metrics (required for observable metrics).
        :param tags: Optional tags (attributes) to attach to the metric.
        :return: The created metric.
        """
        tags = tags or {}  # Ensure tags is an empty dict if not provided

        if metric_type == "counter":
            return self.meter.create_counter(
                name=name, description=description, unit=unit
            )
        elif metric_type == "up_down_counter":
            return self.meter.create_up_down_counter(
                name=name, description=description, unit=unit
            )
        elif metric_type == "histogram":
            return self.meter.create_histogram(
                name=name, description=description, unit=unit
            )
        elif metric_type == "observable_counter":
            return self.meter.create_observable_counter(
                name=name, callbacks=[lambda options: callback(options, tags)], description=description, unit=unit
            )
        elif metric_type == "observable_up_down_counter":
            return self.meter.create_observable_up_down_counter(
                name=name, callbacks=[lambda options: callback(options, tags)], description=description, unit=unit
            )
        elif metric_type == "observable_gauge":
            return self.meter.create_observable_gauge(
                name=name, callbacks=[lambda options: callback(options, tags)], description=description, unit=unit
            )
        else:
            raise ValueError(f"Unsupported metric type: {metric_type}")

    # Example callback generator for observable metrics with tags
    def create_observable_callback(
        self, value_func: Callable[[], float]
    ) -> Callable[[CallbackOptions, Dict[str, str]], Iterable[Observation]]:
        def callback(options: CallbackOptions, tags: Dict[str, str]) -> Iterable[Observation]:
            yield Observation(value_func(), tags)  # Use tags here
        return callback

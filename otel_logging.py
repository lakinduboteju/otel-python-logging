import logging

from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource


def setup_otel_logging(otel_collector_host: str, otel_collector_port: int, insecure: bool):
    """
    Set up OpenTelemetry logging with a logger provider and OTLP exporter.
    This function configures app with the OpenTelemetry SDK to export logs
    to an OpenTelemetry Collector running on Docker.
    It creates a logger provider, sets it as the global logger provider,
    and configures an OTLP log exporter to send logs to the collector.
    The logger provider is configured with a resource that includes
    service name and instance ID.
    The function also creates a logging handler that uses the OpenTelemetry
    logger provider and attaches it to the root logger.
    The logging handler allows you to use the standard Python logging library
    to log messages, which are then sent to the OpenTelemetry logger provider.
    The logging handler is set to log all messages (level=logging.NOTSET).
    """

    # Set up OpenTelemetry logging
    # Create a logger provider and set it as the global logger provider
    # This is where you would set up your OpenTelemetry SDK
    # and configure it to export logs to your desired backend
    # For example, you might use the OTLP exporter to send logs to an OpenTelemetry Collector
    logger_provider = LoggerProvider(
        resource=Resource.create(
            {
                "service.name": "otel-example",
                "service.instance.id": "otel-example-instance",
            }
        ),
    )
    set_logger_provider(logger_provider)
    # Create an OTLP log exporter and add it to the logger provider
    # This exporter sends logs to an OpenTelemetry Collector
    # running on Docker (otel-collector:4317)
    exporter = OTLPLogExporter(
        endpoint=f"{otel_collector_host}:{otel_collector_port}",
        insecure=insecure
    )
    # Set up the log exporter and batch processor
    # The batch processor batches log records before sending them to the exporter
    # This can help reduce the number of requests sent to the backend
    # and improve performance
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    # Create a logging handler that uses the OpenTelemetry logger provider
    # This handler sends log records to the OpenTelemetry logger provider
    # and allows you to use the standard Python logging library
    # to log messages
    # The LoggingHandler is a standard Python logging handler
    # that sends log records to the OpenTelemetry logger provider
    # The level parameter specifies the minimum log level
    # for records to be sent to the logger provider
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    # Attach OTLP handler to root logger
    logging.getLogger().addHandler(handler)

import logging

from otel_logging import setup_otel_logging


# Set up OpenTelemetry logging
# This function configures app with the OpenTelemetry SDK to export logs
setup_otel_logging("otel-collector", 4317, True)

logger = logging.getLogger("otel-example")
logger.setLevel(logging.DEBUG)

# Log some messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
# Log a message with attributes
logger.info(
    "This is an info message with attributes",
    extra={
        "key1": "value1",
        "key2": "value2",
    },
)

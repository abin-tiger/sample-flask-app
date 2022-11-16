from flask import request
from prometheus_flask_exporter.multiprocess import (
    GunicornPrometheusMetrics,
    PrometheusMetrics,
)
import os

# Add default static labels for the flask prometheus metrics. For eg. DEFAULT_STATIC_LABELS = {"xyz": "xyz"}
DEFAULT_STATIC_LABELS = {}

# Labels can be added dynamically using value from flask request or response objects
# For eg. DEFAULT_DYNAMIC_LABELS = {"request_path": lambda: request.path}
DEFAULT_DYNAMIC_LABELS = {}

COMBINED_LABELS = {**DEFAULT_STATIC_LABELS, **DEFAULT_DYNAMIC_LABELS}

# This is added a prefix to custom metrics created. Update the value accordingly.
NAMESPACE = "flask_app"

if os.environ.get("SERVER_SOFTWARE", "").startswith("gunicorn"):
    # Creating the multi threaded version for flask prometheus exporter.
    metrics = GunicornPrometheusMetrics.for_app_factory(
        path="/metrics",
        default_labels=COMBINED_LABELS,
    )
else:
    metrics = PrometheusMetrics(
        app=None,
        path="/metrics",
        default_labels=COMBINED_LABELS,
    )

registry = metrics.registry

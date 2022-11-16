
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
import os

# Based on https://github.com/rycus86/prometheus_flask_exporter#multiprocess-applications
def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(int(os.getenv('METRICS_PORT')))


def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)

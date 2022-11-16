from flask import Blueprint, request, Response
from my_api.metrics import registry, NAMESPACE, metrics
from prometheus_client import Counter, Histogram
from prometheus_client.utils import INF
from flask import current_app as app

simple_api = Blueprint("simple_api", __name__)

@simple_api.route("/")  # requests tracked by default
def info():
    """
    Returns some info about the app.
    """
    return (
        "Hello! This is a example app for demonstrating prometheus metrics collection"
    )


@simple_api.route("/healthz")
@metrics.do_not_track()  # skipping default metrics collection for this path
def health():
    """
    Health check.
    """
    return (
        "Success"
    )


total_auths = Counter(
    name="total_auths",
    documentation="Total API authentications",
    labelnames=["user"],  # default label keys for the metric.
    registry=registry,  # Using the flask prometheus exporter registry
    namespace=NAMESPACE,  # This is added as a prefix to the metric name.
)

@simple_api.before_request # This function is invoked for all API calls.
def authenticate():
    """
    A placeholder function which authenticates all API calls.
    """

    # Getting user info from header is just an example. Get it by parsing JWT token when performing SSO integration.
    total_auths.labels(user=request.headers.get("user", "anonymous")).inc()

    return


@simple_api.route("/square", methods=["GET"])
def square():
    """
    An API that that takes a integer and returns the square.
    """

    if not request.args.get("num"):
        return Response("Missing request parameter 'num'!", status=400)

    num = float(request.args.get("num"))

    app.logger.info(f"Finding square for {num}")
    result = num ** 2

    return str(result)


# Histogram metric to record the distribution of input values.
input_distribution = Histogram(
    name="even_numbers",
    documentation="Metrics to track distribution even numbers",
    buckets=(1, 10, 100, 1000, 10000, 100000, 100000, INF),
    labelnames=(),  # default label keys for the metric
    registry=registry,  # Using the flask prometheus exporter registry
    namespace=NAMESPACE,  # This is added as a prefix to the metric name.
)


@simple_api.route("/even", methods=["GET"])  # requests tracked by default
def even():
    """
    An API that that takes a integer and says whether it's even or not.
    """

    if not request.args.get("num"):
        return Response("Missing request parameter 'num'!", status=400)

    num = float(request.args.get("num"))

    # Recording the number as an observation in the metric
    input_distribution.observe(
        num
    )

    app.logger.info(f"Checking whether {num} is even")
    is_even = (num % 2) == 0

    return "true" if is_even else "false"

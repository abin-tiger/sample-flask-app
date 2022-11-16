# Prometheus Example

An example REST API with prometheus metrics integration. The REST API is built using flask.

The prometheus metrics integration is done using [prometheus-flask-exporter](https://pypi.org/project/prometheus-flask-exporter/) built on [prometheus-client](https://github.com/prometheus/client_python) for python.
This example application tries to cover the basic metrics collections features using these libraries. Refer the respective documentation for advanced use cases.

Refer the [About the Integration](#about-the-integration) section to learn how the integration is done in the code.

Similar libaries are available for other languages and frameworks:

* [express-prometheus-middleware](https://www.npmjs.com/package/express-prometheus-middleware)
* [django-promethues](https://pypi.org/project/django-prometheus/)
* Promethues Client libraries: https://prometheus.io/docs/instrumenting/clientlibs/

## Architecture

![Architecture](architecture/architecture.jpeg)

## Prerequisites

If you're new to Prometheus refer the confluence guide: [Getting Started with Prometheus](https://sbd-ddbot.atlassian.net/wiki/spaces/MLOP/pages/2180251699/Getting+Started+with+Prometheus).

The entire applicatio can be run and tested locally. Prometheus should be installed already in the machine. Follow [confluence guide](https://sbd-ddbot.atlassian.net/wiki/spaces/MLOP/pages/2179399681/How-To+Install+Prometheus) for installation steps.


## Installation

- Create virtual environment: `python -m venv venv`
- Activate environment: `source .\venv\Scripts\activate`
- Install dependencies: `pip install -r env/pip/requirements.txt`

## Run

- Copy the `prometheus.yml` configuraton to prometheus installation path.
  Windows:
  ```shell
  cp prometheus.yml ~/bin/prometheus-2.32.1.windows-amd64/
  ```
  Linux:
  ```bash
  cp prometheus.yml ~/bin/prometheus-2.32.1.linux-amd64/
  ```
- Start prometheus server. Refer the [confluence guide](https://sbd-ddbot.atlassian.net/wiki/spaces/MLOP/pages/2179399681/How-To+Install+Prometheus) for running prometheus.

- Run the application.
  ```bash
  python -u run.py
  ```

  The app also included configurations for gunicorn. To run with gunicorn execute the command.

  ```bash
  ./run.sh
  ```

## Test the APIs

Hit the APIs:
```bash
curl -s http://localhost:5000/ --header "user: john"

curl -s http://localhost:5000/square?num=20 --header "user: john"

curl -s http://localhost:5000/even?num=20 --header "user: john"
```

The app is currently deployed in SBD Caspian cluster. Endpoint: https://sbd-prometheus-flask-app.sandbox.sbd-caspian.com/

Open the `/metrics` endpoint to see the prometheus metrics in plain text format: http://localhost:5000/metrics

If running with gunicorn open: http://localhost:9200/metrics
![image](https://user-images.githubusercontent.com/72504807/146925347-00771127-4958-48c8-a8db-fba99e9b0328.png)


Open prometheus UI and query the metrics.

Example metrics:

```promql
flask_http_request_duration_seconds_count
```

```promql
flask_app_even_numbers_bucket
```

```
sum(flask_http_request_duration_seconds_count{app="sbd-prometheus-flask-app"})
```
![image](https://user-images.githubusercontent.com/72504807/146738274-94132fb5-e954-4d57-8742-c9bbc7248a45.png)


## Grafana Dashboards

* [Flask App Dashboard](https://caspian-grafana.sandbox.sbd-caspian.com/d/weX4mpl3/flask-app-dashboard?orgId=1)

* [Prometheus Flask Example Dashboard](https://caspian-grafana.sandbox.sbd-caspian.com/d/cphhAAT7z/prometheus-flask-example-dashboard?orgId=1)


## Notebooks

Jupyterhub notebook with examples on querying prometheus with Python: [notebook](notebooks/notebook.ipynb)


## About the Integration

The Prometheus integration is primarily done through [prometheus-flask-exporter](https://pypi.org/project/prometheus-flask-exporter/). It exposes HTTP metrics by default for all flask routes. It has the necessary helper classes to integrate with Gunicorn.

### Initialization

An object of `prometheus-flask-exporter` class `PrometheusMetrics` is initialized in [metrics.py](my_api/metrics.py). It creates a Flask app factory object which is then imported and registered in the Flask app in [app.py](my_api/app.py). This is the only step required for exposing the default HTTP metrics for the Flask app.

When run with Gunicorn the `GunicornPrometheusMetrics` is used instead of `PrometheusMetrics`. Gunicorn should be run with [config.py](config.py).

### Adding custom metrics for Flask routes

We can add custom metrics for all flask routes. The register_metrics function in the [app.py](my_api/app.py) adds a custom metric `flask_request_in_progress` for all flask routes. It's uses to track the number of active requests for each request path.

### Custom metrics for specific Flask routes

Custom metrics can be added for specific flask routes. Refer the [github example](https://github.com/rycus86/prometheus_flask_exporter#:~:text=%40metrics.gauge(%27in_progress%27%2C%20%27Long%20running%20requests%20in%20progress%27))

Default metrics can be excluded for certain routes by using `do_not_track` decorator as seen for the function health in [routes.py](my_api/routes.py).

### Other Custom metrics

For creating metrics which aren't related to Flask routes the [prometheus-client](https://github.com/prometheus/client_python) for python can be used. `total_auths` is a counter metrics added in [routes.py](my_api/routes.py) in the authenticate function using the prometheus-client library. Remember to use the `registry` imported by [metrics.py](my_api/metrics.py) when new metrics are created. This ensures the metrics are added along with ones from prometheus-flask-exporter.


For more examples on usage of the library refer [prometheus-flask-exporter](https://pypi.org/project/prometheus-flask-exporter/) and [prometheus-client](https://github.com/prometheus/client_python).


## Caveats

Debug mode on Flask breask the prometheus-flask-exporter module. Turn off debug mode to see the metrics.

```python
if __name__ == "__main__":
    app.run(debug=False)
```

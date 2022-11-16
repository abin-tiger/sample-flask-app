# The shell script creates a folder to be used by prometheus client
# for storing data from multiple python processes. Data should be cleared b/w restarts.
METRICS_FOLDER="metrics_data"

rm -rf $METRICS_FOLDER
mkdir $METRICS_FOLDER

# Library expects the following environment variables.
export METRICS_PORT="9200"
export PROMETHEUS_MULTIPROC_DIR=./$METRICS_FOLDER
export prometheus_multiproc_dir=./$METRICS_FOLDER
gunicorn -c config.py --timeout 10 -w 2 -b 0.0.0.0:5000 run:app

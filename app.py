from flask import Flask, render_template
from prometheus_client import Counter, generate_latest
import logging
import logging_loki

app = Flask(__name__)

# --- Prometheus Metric ---
VISIT_COUNTER = Counter("webapp_visits_total", "Total homepage visits")

# --- Loki Logging Handler ---
handler = logging_loki.LokiHandler(
    url="http://loki:3100/loki/api/v1/push",
    tags={"app": "python-web"},
    version="1",
)
logger = logging.getLogger("python-logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.route("/")
def home():
    VISIT_COUNTER.inc()
    logger.info("Homepage visited")
    return render_template("index.html")


@app.route("/metrics")
def metrics():
    return generate_latest(), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


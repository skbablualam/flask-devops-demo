from flask import Flask
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

app = Flask(__name__)

# Prometheus metrics
flask_http_requests_total = Counter(
    'flask_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

flask_http_request_duration_seconds = Histogram(
    'flask_http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

flask_active_requests = Gauge(
    'flask_active_requests',
    'Number of active requests'
)

@app.before_request
def before_request():
    flask_active_requests.inc()

@app.after_request
def after_request(response):
    flask_active_requests.dec()
    return response

@app.route('/')
def home():
    return "DevOps Demo App Running Successfully!"

@app.route('/health')
def health():
    return {"status": "UP"}

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
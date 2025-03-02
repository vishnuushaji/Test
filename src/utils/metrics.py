# src/utils/metrics.py
from prometheus_client import Counter, Histogram
import time

# Request Metrics
REQUEST_COUNT = Counter(
    'app_requests_total', 
    'Total Request Count',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds', 
    'Request Latency',
    ['method', 'endpoint']
)

def track_request_metrics(func):
    def wrapper(*args, **kwargs):
        method = func.__name__
        start_time = time.time()
        
        try:
            response = func(*args, **kwargs)
            REQUEST_COUNT.labels(method=method, endpoint=func.__name__, http_status=200).inc()
            return response
        except Exception as e:
            REQUEST_COUNT.labels(method=method, endpoint=func.__name__, http_status=500).inc()
            raise
        finally:
            REQUEST_LATENCY.labels(method=method, endpoint=func.__name__).observe(time.time() - start_time)
    
    return wrapper
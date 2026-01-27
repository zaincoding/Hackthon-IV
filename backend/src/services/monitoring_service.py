"""
Monitoring service for the AI-Powered Todo Chatbot.
Tracks performance metrics, error rates, and system health.
"""

import time
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from ..utils.logging import detailed_logger
from ..services.storage import storage


class MonitoringService:
    """Service for monitoring system performance and health."""

    def __init__(self):
        self.request_times = deque(maxlen=1000)  # Keep last 1000 request times
        self.error_count = 0
        self.request_count = 0
        self.start_time = datetime.now()

        # Performance thresholds
        self.max_response_time = 3.0  # seconds
        self.max_error_rate = 0.05  # 5%

        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self._periodic_cleanup, daemon=True)
        self.monitoring_thread.start()

    def record_request_time(self, elapsed_time: float):
        """Record the time taken for a request."""
        self.request_times.append(elapsed_time)
        self.request_count += 1

    def record_error(self):
        """Increment the error counter."""
        self.error_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        now = datetime.now()
        uptime = now - self.start_time

        # Calculate response time metrics
        if self.request_times:
            avg_response_time = sum(self.request_times) / len(self.request_times)
            p95_response_time = self._calculate_percentile(95)
            max_response_time = max(self.request_times)
        else:
            avg_response_time = 0
            p95_response_time = 0
            max_response_time = 0

        # Calculate error rate
        error_rate = self.error_count / self.request_count if self.request_count > 0 else 0

        # Get memory usage
        memory_usage = storage.get_memory_usage()

        return {
            "uptime_seconds": uptime.total_seconds(),
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": error_rate,
            "avg_response_time": avg_response_time,
            "p95_response_time": p95_response_time,
            "max_response_time": max_response_time,
            "memory_usage": memory_usage,
            "health_status": self._evaluate_health(avg_response_time, error_rate)
        }

    def _calculate_percentile(self, percentile: int) -> float:
        """Calculate the given percentile of response times."""
        if not self.request_times:
            return 0

        sorted_times = sorted(self.request_times)
        index = int(len(sorted_times) * percentile / 100)
        return sorted_times[min(index, len(sorted_times) - 1)]

    def _evaluate_health(self, avg_response_time: float, error_rate: float) -> str:
        """Evaluate system health based on metrics."""
        if avg_response_time > self.max_response_time or error_rate > self.max_error_rate:
            return "degraded"
        return "healthy"

    def _periodic_cleanup(self):
        """Periodic cleanup tasks."""
        while True:
            time.sleep(300)  # Run every 5 minutes
            try:
                # Log current metrics periodically
                metrics = self.get_metrics()
                detailed_logger.info("Periodic system metrics", extra=metrics)

                # Cleanup expired sessions
                removed_count = storage.cleanup_expired_sessions()
                if removed_count > 0:
                    detailed_logger.info(f"Cleaned up {removed_count} expired sessions")

            except Exception as e:
                detailed_logger.error(f"Error in periodic cleanup: {str(e)}")


# Global monitoring service instance
monitoring_service = MonitoringService()
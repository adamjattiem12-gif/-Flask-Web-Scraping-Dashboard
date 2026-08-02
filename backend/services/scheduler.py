"""
Background scraping scheduler.

Runs the same scrape logic as POST /api/scrape on a fixed interval using
APScheduler, so data refreshes automatically without a user clicking the
"Scrape Now" button. Controlled via two environment variables:

- SCRAPE_SCHEDULER_ENABLED: "1"/"true" to turn it on (default: off, so
  running tests or `flask run` locally doesn't unexpectedly hit external
  sites on a timer).
- SCRAPE_INTERVAL_MINUTES: how often to run (default: 15).
"""
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)

_scheduler = None


def _run_scheduled_scrape(app):
    """Executed on the schedule. Uses the app's own test client to call
    POST /api/scrape internally — this gives the view function a real
    request context (it reads request.args/JSON body) without needing a
    second process or an HTTP round-trip to itself."""
    try:
        logger.info("[scheduler] Running scheduled scrape...")
        with app.test_client() as client:
            response = client.post("/api/scrape")
            logger.info(f"[scheduler] Scheduled scrape finished with status {response.status_code}")
    except Exception as e:
        logger.error(f"[scheduler] Scheduled scrape failed: {e}", exc_info=True)


def init_scheduler(app):
    """Start the background scheduler if enabled via environment variable.
    Safe to call once at app startup; does nothing if already running or
    if disabled."""
    global _scheduler

    enabled = os.environ.get("SCRAPE_SCHEDULER_ENABLED", "0").lower() in ("1", "true", "yes")
    if not enabled:
        logger.info("[scheduler] Disabled (set SCRAPE_SCHEDULER_ENABLED=1 to enable)")
        return None

    if _scheduler is not None:
        return _scheduler

    interval_minutes = int(os.environ.get("SCRAPE_INTERVAL_MINUTES", "15"))

    _scheduler = BackgroundScheduler(daemon=True)
    _scheduler.add_job(
        func=lambda: _run_scheduled_scrape(app),
        trigger="interval",
        minutes=interval_minutes,
        id="periodic_scrape",
        replace_existing=True,
        next_run_time=None,  # first run happens after the first interval, not immediately
    )
    _scheduler.start()
    logger.info(f"[scheduler] Started — scraping every {interval_minutes} minute(s)")
    return _scheduler


def shutdown_scheduler():
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None

"""Background Poller for GasPot HMI

Polls GasPot at regular intervals and stores readings to historian database.
Runs in a background thread to avoid blocking Flask request handling.
"""

import threading
import time
import logging
from datetime import datetime
from typing import Optional

from app import get_db_session, GASPOT_HOST, GASPOT_PORT
from app.models import TankReading
from app.atg_client import ATGClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Polling configuration
POLL_INTERVAL = 10  # seconds between polls
MAX_RETRIES = 3     # max consecutive failures before backoff
BACKOFF_TIME = 30   # seconds to wait after max failures


class GasPotPoller:
    """Background poller that fetches data from GasPot and stores to historian."""

    def __init__(self, host: str, port: int, poll_interval: int = POLL_INTERVAL):
        """Initialize poller.

        Args:
            host: GasPot hostname
            port: GasPot port
            poll_interval: Seconds between polls
        """
        self.host = host
        self.port = port
        self.poll_interval = poll_interval
        self.client = ATGClient(host, port)
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._consecutive_failures = 0
        self._last_poll_time: Optional[datetime] = None
        self._last_poll_success = False

    def start(self):
        """Start the background polling thread."""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("Poller already running")
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()
        logger.info(f"Started GasPot poller: {self.host}:{self.port} every {self.poll_interval}s")

    def stop(self):
        """Stop the background polling thread."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None
        logger.info("Stopped GasPot poller")

    def is_running(self) -> bool:
        """Check if poller is running."""
        return self._thread is not None and self._thread.is_alive()

    @property
    def status(self) -> dict:
        """Get current poller status."""
        return {
            'running': self.is_running(),
            'last_poll_time': self._last_poll_time.isoformat() if self._last_poll_time else None,
            'last_poll_success': self._last_poll_success,
            'consecutive_failures': self._consecutive_failures,
            'host': self.host,
            'port': self.port,
            'interval': self.poll_interval
        }

    def _poll_loop(self):
        """Main polling loop - runs in background thread."""
        logger.info("Poller loop started")

        while not self._stop_event.is_set():
            try:
                self._poll_once()
                self._consecutive_failures = 0
                self._last_poll_success = True
            except Exception as e:
                self._consecutive_failures += 1
                self._last_poll_success = False
                logger.error(f"Poll failed ({self._consecutive_failures}): {e}")

                # Backoff if too many consecutive failures
                if self._consecutive_failures >= MAX_RETRIES:
                    logger.warning(f"Too many failures, backing off for {BACKOFF_TIME}s")
                    self._stop_event.wait(BACKOFF_TIME)
                    self._consecutive_failures = 0
                    continue

            self._last_poll_time = datetime.now()

            # Wait for next poll interval
            self._stop_event.wait(self.poll_interval)

        logger.info("Poller loop stopped")

    def _poll_once(self):
        """Execute a single poll cycle."""
        # Get readings from GasPot
        readings = self.client.poll_all()

        if not readings:
            logger.warning("No readings returned from GasPot")
            return

        # Store readings to database
        session = get_db_session()
        try:
            timestamp = datetime.now()

            for reading in readings:
                tank_reading = TankReading(
                    tank_id=reading.tank_id,
                    timestamp=timestamp,
                    volume=reading.volume,
                    tc_volume=reading.tc_volume,
                    ullage=reading.ullage,
                    height=reading.height,
                    water_content=reading.water_content,
                    temperature=reading.temperature,
                    pressure=reading.pressure
                )
                session.add(tank_reading)

            session.commit()
            logger.debug(f"Stored {len(readings)} readings at {timestamp}")

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


# Global poller instance
_poller: Optional[GasPotPoller] = None


def get_poller() -> Optional[GasPotPoller]:
    """Get the global poller instance."""
    return _poller


def start_poller():
    """Start the global poller."""
    global _poller

    if _poller is None:
        _poller = GasPotPoller(GASPOT_HOST, GASPOT_PORT)

    _poller.start()
    return _poller


def stop_poller():
    """Stop the global poller."""
    global _poller

    if _poller is not None:
        _poller.stop()

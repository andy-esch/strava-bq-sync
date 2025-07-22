"""Retry logic for external API calls."""

import logging
import time
from functools import wraps
from typing import Any, Callable, TypeVar

import requests

from stravabqsync.exceptions import StravaRateLimitError

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def retry_on_failure(
    max_attempts: int = 3,
    backoff_seconds: float = 1.0,
    exponential_backoff: bool = True,
    retry_on_status: tuple[int, ...] = (429, 500, 502, 503, 504),
) -> Callable[[F], F]:
    """Retry decorator for API calls with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        backoff_seconds: Initial delay between retries
        exponential_backoff: Whether to use exponential backoff
        retry_on_status: HTTP status codes to retry on
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)

                except requests.exceptions.HTTPError as e:
                    if hasattr(e, "response") and e.response is not None:
                        status_code = e.response.status_code

                        # Handle rate limiting specially
                        if status_code == 429:
                            retry_after = int(e.response.headers.get("Retry-After", 60))
                            if attempt == max_attempts - 1:
                                raise StravaRateLimitError(
                                    f"Rate limit exceeded after {
                                        max_attempts
                                    } attempts",
                                    retry_after=retry_after,
                                )
                            logger.warning(
                                "Rate limited, waiting %s seconds (attempt %d/%d)",
                                retry_after,
                                attempt + 1,
                                max_attempts,
                            )
                            time.sleep(retry_after)
                            continue

                        # Don't retry on client errors (except rate limiting)
                        if status_code < 500 and status_code != 429:
                            raise

                        # Retry on server errors
                        if status_code in retry_on_status:
                            last_exception = e
                        else:
                            raise
                    else:
                        # Network error without response
                        last_exception = e

                except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                ) as e:
                    last_exception = e

                # Don't sleep on the last attempt
                if attempt < max_attempts - 1:
                    delay = backoff_seconds
                    if exponential_backoff:
                        delay *= 2**attempt

                    logger.warning(
                        "Request failed (attempt %d/%d), retrying in %.1f seconds: %s",
                        attempt + 1,
                        max_attempts,
                        delay,
                        str(last_exception),
                    )
                    time.sleep(delay)

            # All attempts failed
            logger.error("All %d retry attempts failed", max_attempts)
            if last_exception:
                raise last_exception

        return wrapper

    return decorator

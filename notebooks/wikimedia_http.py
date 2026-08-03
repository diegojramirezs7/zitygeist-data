"""Shared HTTP layer for all Wikimedia API calls in this exploration.

Centralizes two things every request in this project must get right, per
https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy
and https://wikitech.wikimedia.org/wiki/Robot_policy:

- A compliant User-Agent (client/version + real contact info). A vague or
  missing one is explicitly called out as blockable, and what looked like
  "unstable/missing data" earlier in this exploration was very likely this —
  confirmed by testing the same URLs with a browser UA, which worked fine.
- A conservative shared rate limit (policy caps unauthenticated REST/Action
  API traffic at <5 req/s; we throttle to 2 req/s across every call site,
  regardless of which Wikimedia domain it's going to, for a comfortable
  margin without needing a per-domain quota system at this scale).
"""

import threading
import time

import requests

USER_AGENT = f"zitygeist-exploration/0.1 (diegojramirezs7@gmail.com) python-requests/{requests.__version__}"

_MIN_INTERVAL = 0.5  # seconds between requests -> max 2 req/s, well under the 5 req/s policy cap
_last_request_time = 0.0
_lock = threading.Lock()


def get(url: str, **kwargs) -> requests.Response:
    """requests.get, but rate-limited and always carrying a policy-compliant User-Agent."""
    global _last_request_time
    with _lock:
        wait = _MIN_INTERVAL - (time.monotonic() - _last_request_time)
        if wait > 0:
            time.sleep(wait)
        headers = {"User-Agent": USER_AGENT, **kwargs.pop("headers", {})}
        resp = requests.get(url, headers=headers, **kwargs)
        _last_request_time = time.monotonic()
    return resp

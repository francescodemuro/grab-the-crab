"""Bounded, isolated in-memory evaluation sessions for a single web worker."""
from __future__ import annotations

import secrets
import time
from dataclasses import dataclass, field
from threading import RLock
from typing import Callable

from .mission_control import MissionControlSession


class SessionExpired(RuntimeError):
    pass


class SessionCapacity(RuntimeError):
    pass


@dataclass
class _Entry:
    session: MissionControlSession
    touched: float
    lock: RLock = field(default_factory=RLock)
    active: int = 0


class SessionStore:
    """Serialize each operator's operations without sharing their incident.

    Sessions expire after an idle hour. Active requests cannot be expired or
    evicted; a full store rejects new sessions instead of discarding work.
    This is intentionally not a persistence or multi-worker service.
    """

    def __init__(self, *, capacity: int = 16, ttl: float = 3600,
                 clock: Callable[[], float] = time.monotonic,
                 factory: Callable[[], MissionControlSession] = MissionControlSession):
        if capacity < 1 or ttl <= 0:
            raise ValueError("Session capacity and lifetime must be positive.")
        self.capacity = capacity
        self.ttl = ttl
        self._clock = clock
        self._factory = factory
        self._entries: dict[str, _Entry] = {}
        self._lock = RLock()

    def run(self, token: str | None, operation: Callable, *, create: bool = False):
        with self._lock:
            now = self._clock()
            expired = [key for key, entry in self._entries.items()
                       if entry.active == 0 and now - entry.touched >= self.ttl]
            for key in expired:
                del self._entries[key]
            entry = self._entries.get(token) if token else None
            if entry is None:
                if not create:
                    raise SessionExpired("Evaluation session expired. Reload the page to start again.")
                if len(self._entries) >= self.capacity:
                    raise SessionCapacity("Evaluation capacity reached. Try again after a session expires.")
                token = secrets.token_urlsafe(32)
                entry = _Entry(self._factory(), now)
                self._entries[token] = entry
            entry.active += 1
        try:
            with entry.lock:
                result = operation(entry.session)
            return token, result
        finally:
            with self._lock:
                entry.active -= 1
                entry.touched = self._clock()

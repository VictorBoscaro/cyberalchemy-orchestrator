"""Explicitly in-memory adapter test doubles for the RWO prototype.

These classes model the communication boundary without claiming durable journal
acceptance, crash recovery, a network protocol, or external delivery.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .canonical import canonical_payload_bytes


@dataclass(frozen=True)
class EventIngressObservation:
    status: str
    logical_event_key: tuple[str, str]
    canonical_bytes: bytes


@dataclass(frozen=True)
class DeliveryObservation:
    status: str
    logical_message_id: str
    transport_delivery_attempt_id: str
    canonical_bytes: bytes


class InMemoryEventIngressPort:
    """A process-local candidate-event deduplicator.

    It is intentionally *not* a journal implementation.  A caller can use its
    bounded statuses to demonstrate the RWO handoff shape before binding a real
    journal-acceptance owner.
    """

    def __init__(self) -> None:
        self._events: dict[tuple[str, str], bytes] = {}

    def offer(self, event: Mapping[str, Any]) -> EventIngressObservation:
        key = (str(event.get("stream_id", "")), str(event.get("event_id", "")))
        payload = canonical_payload_bytes(dict(event))
        known = self._events.get(key)
        if known is None:
            self._events[key] = payload
            status = "accepted_in_memory"
        elif known == payload:
            status = "identical_duplicate"
        else:
            status = "conflict"
        return EventIngressObservation(status, key, payload)


class InMemoryCommandDeliveryPort:
    """A process-local command delivery port with explicit redelivery identity."""

    def __init__(self) -> None:
        self._messages: dict[str, bytes] = {}
        self._attempts = 0

    def deliver(
        self, command: Mapping[str, Any], *, logical_message_id: str
    ) -> DeliveryObservation:
        payload = canonical_payload_bytes(dict(command))
        known = self._messages.get(logical_message_id)
        self._attempts += 1
        attempt_id = f"memory-delivery-{self._attempts}"
        if known is None:
            self._messages[logical_message_id] = payload
            status = "accepted_by_transport"
        elif known == payload:
            status = "redelivered"
        else:
            status = "rejected_known"
        return DeliveryObservation(status, logical_message_id, attempt_id, payload)

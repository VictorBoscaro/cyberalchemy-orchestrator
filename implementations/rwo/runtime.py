"""Small in-memory composition shell around the pure RWO kernel.

This is an executable prototype seam, not a journal, worker, queue, or service.
Only an event already presented as an AcceptedEventView is eligible for the
kernel.  The in-memory ingress and delivery ports are observable test doubles.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .adapters import (
    DeliveryObservation,
    EventIngressObservation,
    InMemoryCommandDeliveryPort,
    InMemoryEventIngressPort,
)
from .kernel import (
    CompileOutcome,
    CompiledGraph,
    ReduceOutcome,
    compile_work_graph,
    reduce_event,
)


@dataclass(frozen=True)
class PrototypeStep:
    ingress: EventIngressObservation
    reduction: ReduceOutcome | None
    delivery: DeliveryObservation | None


class InMemoryRwoPrototype:
    """Connect a compiled graph to local event/delivery test doubles."""

    def __init__(self, compiled: CompiledGraph, initial_cursor: Mapping[str, Any]) -> None:
        self.compiled = compiled
        self.cursor: Mapping[str, Any] = copy.deepcopy(dict(initial_cursor))
        self.ingress = InMemoryEventIngressPort()
        self.delivery = InMemoryCommandDeliveryPort()

    @classmethod
    def from_composition(
        cls, composition: Mapping[str, Any], initial_cursor: Mapping[str, Any]
    ) -> "InMemoryRwoPrototype":
        outcome: CompileOutcome = compile_work_graph(composition)
        if outcome.kind != "Compiled" or outcome.compiled is None:
            codes = ", ".join(defect.code for defect in outcome.defects)
            raise ValueError(f"composition did not compile: {codes}")
        return cls(outcome.compiled, initial_cursor)

    def offer_accepted_event(self, event: Mapping[str, Any]) -> PrototypeStep:
        """Offer an already-accepted event to the local prototype boundary.

        A real integration must replace the local ingress with the selected
        journal-acceptance owner.  An identical ingress duplicate is purposely
        not reduced again.
        """

        ingress = self.ingress.offer(event)
        if ingress.status != "accepted_in_memory":
            return PrototypeStep(ingress, None, None)
        reduction = reduce_event(self.compiled, self.cursor, event)
        if reduction.kind == "Applied":
            self.cursor = reduction.cursor
        delivery = None
        if reduction.command is not None and reduction.command_intent_identity is not None:
            delivery = self.delivery.deliver(
                reduction.command,
                logical_message_id=reduction.command_intent_identity,
            )
        return PrototypeStep(ingress, reduction, delivery)

    def replay(self, events: Sequence[Mapping[str, Any]]) -> tuple[ReduceOutcome, ...]:
        """Purely rebuild a cursor from events without calling ingress or delivery."""

        cursor = copy.deepcopy(dict(self.cursor))
        outcomes: list[ReduceOutcome] = []
        for event in events:
            outcome = reduce_event(self.compiled, cursor, event)
            outcomes.append(outcome)
            if outcome.kind == "Applied":
                cursor = outcome.cursor
        return tuple(outcomes)

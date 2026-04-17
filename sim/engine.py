import heapq
from dataclasses import dataclass, field
from typing import Any, List, Optional, Callable

@dataclass(order=True)
class Event:
    time: float
    type: str = field(compare=False)
    data: Any = field(default=None, compare=False)

class SimulationEngine:
    def __init__(self):
        self.clock = 0.0
        self.event_queue: List[Event] = []
        self.history: List[dict] = []

    def schedule(self, time: float, event_type: str, data: Any = None):
        """Schedule a new event at clock + time."""
        event = Event(self.clock + time, event_type, data)
        heapq.heappush(self.event_queue, event)

    def next_event(self) -> Optional[Event]:
        if not self.event_queue:
            return None
        return heapq.heappop(self.event_queue)

    def run(self, steps: int = 10):
        # Specific problem implementations will define this.
        pass

    def record_state(self, state: dict):
        """Record the state at current clock."""
        state["clock"] = self.clock
        
        # Snapshot of the next event for each type in the FEL
        fel_snapshot = {}
        for event in sorted(self.event_queue):
            if event.type not in fel_snapshot:
                fel_snapshot[event.type] = event.time
        
        state["fel"] = fel_snapshot
        self.history.append(state)

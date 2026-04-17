from sim.engine import SimulationEngine, Event
from typing import Dict, Any, List

class BaseProblem(SimulationEngine):
    def __init__(self, **kwargs):
        super().__init__()
        self.state = self.initial_state()
        self.generators = self.setup_generators(kwargs)

    def initial_state(self) -> Dict[str, Any]:
        """Define initial state variables."""
        raise NotImplementedError

    def setup_generators(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Setup time generators from parameters."""
        raise NotImplementedError

    def handle_event(self, event: Event):
        """Logic to process each event type."""
        raise NotImplementedError

    def run_simulation(self, max_events: int = 50):
        """Run the simulation for a given number of events."""
        # Initial events (usually an arrival)
        self.schedule_initial_events()
        
        # Record initial state
        self.record_state(self.state.copy())

        events_processed = 0
        while events_processed < max_events:
            event = self.next_event()
            if not event:
                break
            
            # Update clock
            self.clock = event.time
            
            # Handle event and potentially update state and schedule new events
            self.handle_event(event)
            
            # Record state
            self.record_state(self.state.copy())
            
            events_processed += 1

    def schedule_initial_events(self):
        """Schedule the first event(s)."""
        raise NotImplementedError

    def get_mermaid_diagram(self, _t) -> str:
        """Return a Mermaid string representing the logical event flow."""
        raise NotImplementedError

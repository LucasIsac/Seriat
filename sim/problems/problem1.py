from sim.problems.base import BaseProblem, Event
from utils.generators import ConstantGenerator, ListGenerator, Generator
from typing import Dict, Any

class Problem1(BaseProblem):
    def initial_state(self) -> Dict[str, Any]:
        return {
            "server_busy": 0,  # 0: Idle, 1: Busy
            "queue": 0,
            "last_event": "START"
        }

    def setup_generators(self, kwargs: Dict[str, Any]) -> Dict[str, Generator]:
        return {
            "arrival": kwargs.get("arrival_gen", ConstantGenerator(45)),
            "service": kwargs.get("service_gen", ConstantGenerator(40))
        }

    def schedule_initial_events(self):
        # First arrival at t=0 or from generator
        self.schedule(next(self.generators["arrival"]), "ARRIVAL")

    def handle_event(self, event: Event):
        self.state["last_event"] = event.type
        
        if event.type == "ARRIVAL":
            # Schedule next arrival
            self.schedule(next(self.generators["arrival"]), "ARRIVAL")
            
            if self.state["server_busy"] == 0:
                # Start service immediately
                self.state["server_busy"] = 1
                self.schedule(next(self.generators["service"]), "END_SERVICE")
            else:
                # Join queue
                self.state["queue"] += 1
                
        elif event.type == "END_SERVICE":
            if self.state["queue"] > 0:
                # Start service for next in queue
                self.state["queue"] -= 1
                self.schedule(next(self.generators["service"]), "END_SERVICE")
            else:
                # Idle
                self.state["server_busy"] = 0

    def get_mermaid_diagram(self, _t) -> str:
        s_start = _t("event_start")
        s_arrival = _t("event_arrival")
        s_end = _t("event_service_end") or "FIN_SERVICIO"
        d_arr = self.generators["arrival"].get_desc(_t)
        d_ser = self.generators["service"].get_desc(_t)
        
        return f"""graph TD
    Start(("{s_start}")) --> Arr["{s_arrival} {d_arr}"]
    Arr --> Arr
    Arr --> Busy{{"{_t('diag_busy_q', default='?')}"}}
    Busy -- {_t('diag_free')} --> End["{s_end} {d_ser}"]
    Busy -- {_t('diag_busy')} --> Queue["{_t('diag_plus_queue')}"]
    End --> QEmpty{{"{_t('diag_q_gt_0')}"}}
    QEmpty -- {_t('diag_yes')} --> End
    QEmpty -- {_t('diag_no')} --> Idle["{_t('diag_idle')}"]"""

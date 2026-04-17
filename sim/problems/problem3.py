from sim.problems.base import BaseProblem, Event
from utils.generators import ConstantGenerator, ListGenerator, Generator
from typing import Dict, Any, List

class Problem3(BaseProblem):
    def initial_state(self) -> Dict[str, Any]:
        return {
            "server_busy": 0,
            "queue": 0,
            "abandoned_count": 0,
            "last_event": "START",
            "queue_customers": []  # List of event_ids (or just times) for abandonment
        }

    def setup_generators(self, kwargs: Dict[str, Any]) -> Dict[str, Generator]:
        return {
            "arrival": kwargs.get("arrival_gen", ConstantGenerator(45)),
            "service": kwargs.get("service_gen", ConstantGenerator(40)),
            "abandonment": kwargs.get("abandon_gen", ConstantGenerator(120))  # 2 minutes default
        }

    def schedule_initial_events(self):
        self.schedule(next(self.generators["arrival"]), "ARRIVAL")

    def handle_event(self, event: Event):
        self.state["last_event"] = event.type
        
        if event.type == "ARRIVAL":
            self.schedule(next(self.generators["arrival"]), "ARRIVAL")
            if self.state["server_busy"] == 0:
                self.state["server_busy"] = 1
                self.schedule(next(self.generators["service"]), "END_SERVICE")
            else:
                self.state["queue"] += 1
                # Schedule abandonment
                wait_time = next(self.generators["abandonment"])
                abandon_time = self.clock + wait_time
                # Store abandonment time to identify which customer abandons
                self.state["queue_customers"].append(abandon_time)
                self.schedule(wait_time, "RENEGING", data=abandon_time)
                
        elif event.type == "END_SERVICE":
            if self.state["queue"] > 0:
                self.state["queue"] -= 1
                # Pop the first customer from queue (FCFS)
                # They no longer abandon
                if self.state["queue_customers"]:
                    self.state["queue_customers"].pop(0)
                self.schedule(next(self.generators["service"]), "END_SERVICE")
            else:
                self.state["server_busy"] = 0
                
        elif event.type == "RENEGING":
            abandon_time = event.data
            if abandon_time in self.state["queue_customers"]:
                # Customer is still in queue
                self.state["queue_customers"].remove(abandon_time)
                self.state["queue"] -= 1
                self.state["abandoned_count"] += 1
            else:
                # Customer already served, ignore this event
                pass

    def get_mermaid_diagram(self, _t) -> str:
        s_start = _t("event_start")
        s_arr = _t("event_arrival")
        s_end = _t("event_service_end")
        d_arr = self.generators["arrival"].get_desc(_t)
        d_ser = self.generators["service"].get_desc(_t)
        d_aba = self.generators["abandonment"].get_desc(_t)
        
        return f"""graph TD
    Start(("{s_start}")) --> Arr["{s_arr} {d_arr}"]
    Arr --> Arr
    Arr --> Idle{{"{_t('diag_busy_q', default='Libre?')}"}}
    Idle -- {_t('diag_yes')} --> End["{s_end} {d_ser}"]
    Idle -- {_t('diag_no')} --> Wait["{_t('diag_wait_prog')} {d_aba}"]
    Wait --> Ab["{_t('event_reneging')}"]
    End --> Next{{"{_t('diag_q_gt_0')}"}}
    Next -- {_t('diag_yes')} --> End
    Next -- {_t('diag_no')} --> Libre["{_t('diag_idle')}"]
    Ab --> Leave["{_t('diag_leave_if')}"]"""

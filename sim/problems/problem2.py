from sim.problems.base import BaseProblem, Event
from utils.generators import ConstantGenerator, ListGenerator, Generator
from typing import Dict, Any

class Problem2(BaseProblem):
    def initial_state(self) -> Dict[str, Any]:
        return {
            "server_busy": 0,
            "queue": 0,
            "server_present": 1,  # 1: Working, 0: Resting
            "last_event": "START",
            "service_remaining": 0.0,
            "current_finish_time": None
        }

    def setup_generators(self, kwargs: Dict[str, Any]) -> Dict[str, Generator]:
        return {
            "arrival": kwargs.get("arrival_gen", ConstantGenerator(45)),
            "service": kwargs.get("service_gen", ConstantGenerator(40)),
            "work_duration": kwargs.get("work_gen", ConstantGenerator(30)),
            "rest_duration": kwargs.get("rest_gen", ConstantGenerator(60))
        }

    def schedule_initial_events(self):
        # Initial arrival
        self.schedule(next(self.generators["arrival"]), "ARRIVAL")
        # Initial work interval end
        self.schedule(next(self.generators["work_duration"]), "SERVER_DEPARTURE")

    def handle_event(self, event: Event):
        self.state["last_event"] = event.type
        
        if event.type == "ARRIVAL":
            self.schedule(next(self.generators["arrival"]), "ARRIVAL")
            if self.state["server_present"] == 1 and self.state["server_busy"] == 0:
                self.state["server_busy"] = 1
                duration = next(self.generators["service"])
                self.state["current_finish_time"] = self.clock + duration
                self.schedule(duration, "END_SERVICE")
            else:
                self.state["queue"] += 1
                
        elif event.type == "END_SERVICE":
            self.state["current_finish_time"] = None
            if self.state["queue"] > 0 and self.state["server_present"] == 1:
                self.state["queue"] -= 1
                duration = next(self.generators["service"])
                self.state["current_finish_time"] = self.clock + duration
                self.schedule(duration, "END_SERVICE")
            else:
                self.state["server_busy"] = 0
                
        elif event.type == "SERVER_DEPARTURE":
            self.state["server_present"] = 0
            # If server was busy, suspend the current service
            if self.state["server_busy"] == 1 and self.state["current_finish_time"] is not None:
                # Calculate remaining time
                self.state["service_remaining"] = self.state["current_finish_time"] - self.clock
                # Remove the pending END_SERVICE event from queue
                self.event_queue = [e for e in self.event_queue if e.type != "END_SERVICE"]
            
            duration = next(self.generators["rest_duration"])
            self.schedule(duration, "SERVER_ARRIVAL")
            
        elif event.type == "SERVER_ARRIVAL":
            self.state["server_present"] = 1
            # Resume service if it was suspended
            if self.state["server_busy"] == 1:
                duration = self.state["service_remaining"]
                self.state["current_finish_time"] = self.clock + duration
                self.schedule(duration, "END_SERVICE")
            elif self.state["queue"] > 0:
                # Server was idle but now it can serve queue
                self.state["server_busy"] = 1
                self.state["queue"] -= 1
                duration = next(self.generators["service"])
                self.state["current_finish_time"] = self.clock + duration
                self.schedule(duration, "END_SERVICE")
                
            # Schedule next departure
            self.schedule(next(self.generators["work_duration"]), "SERVER_DEPARTURE")

    def get_mermaid_diagram(self, _t) -> str:
        s_start = _t("event_start")
        s_arr = _t("event_arrival")
        s_end = _t("event_service_end")
        s_dep = "DEPARTURE"
        s_back = "SERVER_ARRIVAL"
        d_arr = self.generators["arrival"].get_desc(_t)
        d_ser = self.generators["service"].get_desc(_t)
        d_work = self.generators["work_duration"].get_desc(_t)
        d_rest = self.generators["rest_duration"].get_desc(_t)
        
        return f"""graph TD
    Start(("{s_start}")) --> Arr["{s_arr} {d_arr}"]
    Start --> Dep["{s_dep} {d_work}"]
    Arr --> Arr
    Arr --> Check{{"{_t('diag_pres_idle')}"}}
    Check -- {_t('diag_yes')} --> End["{s_end} {d_ser}"]
    Check -- {_t('diag_no')} --> Queue["{_t('diag_plus_queue')}"]
    Dep --> Rest["{_t('diag_rest')} {d_rest}"]
    Dep -- {_t('diag_busy')} --> Suspend["{_t('diag_suspend')}"]
    Rest --> Back["{s_back}"]
    Back --> Resume{{"{_t('diag_suspend_q')}"}}
    Resume -- {_t('diag_yes')} --> End
    Resume -- {_t('diag_no')} --> QCheck{{"{_t('diag_q_gt_0')}"}}
    QCheck -- {_t('diag_yes')} --> End
    Back --> NextDep["{_t('diag_sched_dep')}"]"""

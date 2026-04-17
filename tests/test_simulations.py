import pytest
from sim.problems.problem1 import Problem1
from sim.problems.problem2 import Problem2
from sim.problems.problem3 import Problem3
from utils.generators import ListGenerator, ConstantGenerator

def mock_t(key, default=None):
    return default if default else key

def test_problem1_logic():
    # Arrival every 10, Service 15 (Queue should build)
    sim = Problem1(
        arrival_gen=ListGenerator([10, 10, 10]),
        service_gen=ListGenerator([15, 15, 15])
    )
    sim.run_simulation(max_events=5)
    
    queues = [s["queue"] for s in sim.history]
    assert max(queues) == 1
    assert sim.history[-1]["clock"] == 40.0

def test_problem1_diagram():
    sim = Problem1()
    diagram = sim.get_mermaid_diagram(mock_t)
    assert "graph TD" in diagram
    assert "Arr" in diagram
    assert "Busy" in diagram

def test_problem2_logic():
    # Arrival at 5, Service 20, Depart at 10, Back at 20
    sim = Problem2(
        arrival_gen=ListGenerator([5, 5]),
        service_gen=ListGenerator([20]),
        work_gen=ListGenerator([10]),
        rest_gen=ListGenerator([10])
    )
    sim.run_simulation(max_events=10)
    
    departures = [s for s in sim.history if s["last_event"] == "SERVER_DEPARTURE"]
    assert len(departures) > 0
    assert departures[0]["service_remaining"] == 15.0
    
    arrivals = [s for s in sim.history if s["last_event"] == "SERVER_ARRIVAL"]
    assert len(arrivals) > 0
    assert arrivals[0]["server_present"] == 1

def test_problem2_diagram():
    sim = Problem2()
    diagram = sim.get_mermaid_diagram(mock_t)
    assert "graph TD" in diagram
    assert "Dep" in diagram
    assert "Rest" in diagram

def test_problem3_logic():
    sim = Problem3(
        arrival_gen=ListGenerator([5, 5, 5]),
        service_gen=ListGenerator([50]),
        abandon_gen=ListGenerator([10])
    )
    sim.run_simulation(max_events=10)
    
    reneging = [s for s in sim.history if s["last_event"] == "RENEGING"]
    assert len(reneging) > 0
    assert sim.history[-1]["abandoned_count"] >= 1

def test_problem3_diagram():
    sim = Problem3()
    diagram = sim.get_mermaid_diagram(mock_t)
    assert "graph TD" in diagram
    assert "Wait" in diagram
    assert "event_reneging" in diagram  # key from mock_t

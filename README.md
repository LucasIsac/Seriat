# Seriat: Queuing System Simulator

Seriat is a Python-based discrete-event simulation (DES) tool designed to model and analyze various queuing system configurations. This application was developed as a comprehensive solution for the Practical Work No. 1 (TP1) of the Systems Modelling and Simulation module.

## Overview

The application utilizes a priority-queue-based simulation engine to process events chronologically. It provides a structured CLI interface to configure and execute three distinct simulation scenarios.

## Key Features

- **Modular Architecture**: Separation of the core simulation engine, problem-specific logic, and user interface.
- **Interactive CLI**: Step-by-step configuration using the Rich library for formatted output and tables.
- **Predefined Presets**: Includes data sequences from TP1 tables to facilitate verification of manual simulations.
- **Flexible Generators**: Support for constant values and list-based sequences for time intervals.
- **State Tracking**: Detailed recording of system state changes (clock, queue size, server status) for every processed event.
- **Internationalization**: Support for English and Spanish languages.
- **Export Results**: Results can be exported to Markdown tables.

## Implemented Scenarios

### 1. Standard Single Server (FCFS)
Models a basic system where clients arrive at intervals and are served one-by-one in order of arrival.

### 2. Server with Work/Rest Intervals
Simulates a system where the server alternates between active work periods and rest intervals. Includes logic for suspending and resuming services when the server departs.

### 3. Reneging (Abandonment)
Introduces customer patience thresholds. Clients will leave the queue if their waiting time exceeds a specific limit before being served.

## Project Structure

```
seriat/
├── main.py                 # Application entry point
├── requirements.txt       # Dependencies
├── .gitignore          # Git ignore rules
├── sim/
│   ├── __init__.py
│   ├── engine.py        # Core DES engine using heapq
│   └── problems/
│       ├── __init__.py
│       ├── base.py     # Base Problem class
│       ├── problem1.py # Exercise 1: FCFS
│       ├── problem2.py # Exercise 2: Work/Rest
│       └── problem3.py # Exercise 3: Reneging
├── ui/
│   ├── __init__.py
│   └── cli.py      # Rich-based CLI
└── utils/
    ├── __init__.py
    ├── generators.py  # Time interval generators
    ├── exporter.py  # Results exporter
    └── i18n.py    # Internationalization
```

## Requirements

- Python 3.8 or higher
- Rich library (`pip install rich`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/LucasIsac/Seriat.git
cd Seriat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the simulator:
```bash
python main.py
```

Follow the on-screen prompts to:
1. **Select language** (English/Spanish)
2. **Choose problem** (1, 2, or 3)
3. **Configure time generators**:
   - Constant value (e.g., 45 seconds)
   - List of values (e.g., 65, 6, 2, 21, 42, 33, 21)
   - Preset from TP1 tables
4. **Define number of events** to simulate
5. **View results** in table format
6. Optionally **view event flow diagram** in browser

## How It Works

The simulation uses the **Next-Event Time Advance** algorithm:

1. Initialize clock at 0
2. Schedule initial events (first arrival, etc.)
3. Process events in chronological order using a priority queue (heapq)
4. For each event, update system state and schedule future events
5. Record state after each event

### Event Types

| Event | Description |
|-------|------------|
| `ARRIVAL` | New client arrives |
| `END_SERVICE` | Server finishes serving a client |
| `SERVER_DEPARTURE` | Server leaves for rest (Problem 2) |
| `SERVER_ARRIVAL` | Server returns from rest (Problem 2) |
| `RENEGING` | Client abandons queue (Problem 3) |

### System State Variables

| Variable | Description |
|----------|------------|
| `clock` | Current simulation time |
| `server_busy` | 0 = idle, 1 = busy |
| `server_present` | 0 = resting, 1 = at station |
| `queue` | Number of clients waiting |
| `abandoned_count` | Total abandoned clients (Problem 3) |

## Graphical Legend

In the simulation results tables, the **Graphical** column shows:

| Symbol | Meaning |
|--------|---------|
| `◠` | Server present but idle |
| `▣` | Server busy |
| `□` | Server idle (available) |
| `●` | Client in queue |

**Example:** `◠[▣] ● ●` = Server present, busy, 2 clients waiting

## License

MIT License
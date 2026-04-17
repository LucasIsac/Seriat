# Five Queuing System Simulation Problems

This document provides synthetic statements, lists of events, state variables, and manual simulation tables for five distinct queuing system scenarios.

## Problem 1: Basic Single Server Queue

### Description
Customers arrive individually at random time intervals to receive service one by one in the order of arrival (FCFS). Service times are also random. The server never leaves the service station. If the service station is occupied upon arrival, the customer must wait in a queue. When a service ends, the next customer in line immediately takes the position at the service station.

### Events
1. Customer arrival at the system.
2. End of service.

### State Variables
1. Service station status (Busy/Free).
2. Number of customers in queue.

### Generators
1. Arrival time generator: Inter-arrival time = 45 seconds (constant).
2. Service time generator: Service time = 40 seconds (constant).

### Manual Simulation Table (Problem 1)

| Current Time | Next Arrival | Next End of Service | Queue Count | Service Station State |
| :--- | :--- | :--- | :--- | :--- |
| 8:00:00 | 8:05:00 | 8:03:00 * | 3 | 1 (Busy) |
| 8:03:00 | 8:05:00 | 8:03:40 * | 2 | 1 (Busy) |
| 8:03:40 | 8:05:00 | 8:04:20 * | 1 | 1 (Busy) |
| 8:04:20 | 8:05:00 * | 8:05:00 | 0 | 1 (Busy) |
| 8:05:00 | 8:05:45 | 8:05:00 | 1 | 1 (Busy) |
| 8:05:00 | 8:05:45 | 8:05:40 | 0 | 1 (Busy) |
| 8:05:40 | 8:05:45 | - | 0 | 0 (Free) |
| 8:05:45 | 8:06:30 | 8:06:25 | 0 | 1 (Busy) |
| 8:06:25 | 8:06:30 | Etc. | 0 | 0 (Free) |

---

## Problem 2: Server with Break Cycles

### Description
Similar to Problem 1, but the server works during random time intervals and rests between them for random durations (cycles of working and resting).

### Events
1. Customer arrival at the system.
2. End of service.
3. Server departure (start of rest).
4. Server arrival (start of work).

### State Variables
1. Service station status (Busy/Free).
2. Number of customers in queue.
3. Server presence (Present/Absent).

### Manual Simulation Table (Problem 2)
**Data:**
* Inter-arrival times: 1'05", 6", 2", 21", 42", ...
* Service times: 5", 10", ...
* Rest interval: 60" (constant).
* Work interval: 30" (constant).

| Current Time | Next Arrival | Next End Service | Rest Start | Work Start | Queue Count | SS State | Server State |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 10:30:00 | 10:30:20 | | 10:31:34 | | 0 | 0 | 1 |
| 10:30:20 | 10:31:25 | 10:30:25 | 10:31:34 | | 0 | 1 | 1 |
| 10:30:25 | 10:31:25 | | 10:31:34 | | 0 | 0 | 1 |
| 10:31:25 | 10:31:31 | 10:31:35 | 10:31:34 | | 0 | 1 | 1 |
| 10:31:31 | 10:31:33 | 10:31:35 | 10:31:34 | | 1 | 1 | 1 |
| 10:31:33 | 10:31:54 | 10:31:35 | 10:31:34 | | 2 | 1 | 1 |
| 10:31:34 | 10:31:54 | 10:32:35 | | 10:32:34 | 2 | 1 | 0 |
| 10:31:54 | 10:32:36 | 10:32:35 | | 10:32:34 | 3 | 1 | 0 |
| 10:32:34 | 10:32:36 | 10:32:35 | 10:33:04 | | 3 | 1 | 1 |
| 10:32:35 | | | | | 2 | 1 | 1 |

---

## Problem 3: Queue Reneging (Abandonment)

### Description
Similar to Problem 1, but if a customer waits in the queue for a certain duration (e.g., 10 minutes), they abandon the queue and leave the system without returning.

### Events
1. Customer arrival at the system.
2. End of service.
3. Queue abandonment.

### State Variables
1. Service station status (Busy/Free).
2. Number of customers in queue.
3. Queue arrival time for each customer in line.

### Manual Simulation Table (Problem 3)
**Data:**
* Inter-arrival times: 10", 5", 7", 7", 1'47", 24", ...
* Service times: 50", 1'16", ...
* Maximum wait time: 2' (constant).

| Current Time | Next Arrival | Next End Service | Next Abandonment | Queue Count | SS State | C1 Arrival | C2 Arrival | C3 Arrival | C4 Arrival |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 9:00:32 | 9:00:49 | 9:01:07 | | 0 | 1 | | | | |
| 9:00:49 | 9:00:59 | 9:01:07 | 9:02:49 | 1 | 1 | 9:00:49 | | | |
| 9:00:59 | 9:01:04 | 9:01:07 | 9:02:49 | 2 | 1 | 9:00:49 | 9:00:59 | | |
| 9:01:04 | 9:01:11 | 9:01:07 | 9:02:49 | 3 | 1 | 9:00:49 | 9:00:59 | 9:01:04 | |
| 9:01:07 | 9:01:11 | 9:01:57 | 9:02:59 | 2 | 1 | 9:00:59 | 9:01:04 | | |
| 9:01:11 | 9:01:18 | 9:01:57 | 9:02:59 | 3 | 1 | 9:00:59 | 9:01:04 | 9:01:11 | |
| 9:01:18 | 9:03:05 | 9:01:57 | 9:02:59 | 4 | 1 | 9:00:59 | 9:01:04 | 9:01:11 | 9:01:18 |
| 9:01:57 | 9:03:05 | 9:03:13 | 9:03:04 | 3 | 1 | 9:01:04 | 9:01:11 | 9:01:18 | |
| 9:03:04 | 9:03:05 | 9:03:13 | 9:03:11 | 2 | 1 | 9:01:11 | 9:01:18 | | |
| 9:03:05 | 9:03:29 | 9:03:13 | 9:03:11 | 3 | 1 | 9:01:11 | 9:01:18 | 9:03:05 | |
| 9:03:11 | 9:03:29 | 9:03:13 | 9:03:18 | 2 | 1 | 9:01:18 | 9:03:05 | | |

---

## Problem 4: Priority Queuing

### Description
Similar to Problem 1, but two types of customers arrive: Type A and Type B. Type A customers have priority over Type B for entry into the service station (SS). No discrimination is made between customer types once they are inside the SS.

### Events
1. Arrival of Type A customer.
2. Arrival of Type B customer.
3. End of service.

### State Variables
1. Service station status (Busy/Free).
2. Number of Type A customers in queue.
3. Number of Type B customers in queue.

---

## Problem 5: Distant Service Station with Security Zone

### Description
Similar to Problem 1, but the service station (SS) is located away from the queue for safety reasons. The first customer in the queue can only enter the "security zone" (the path to the SS) when the customer currently being served leaves the SS. The next customer cannot enter the security zone until the preceding one reaches the SS and finishes service. The only exception is if a customer arrives when both the security zone and the SS are free, in which case they enter directly.

### Events
1. Customer arrival at the system.
2. Customer arrival at the SS.
3. End of service.

### State Variables
1. Service station status (Busy/Free).
2. Number of customers in queue.
3. Security zone status (Busy/Free).
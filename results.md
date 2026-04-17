# Servidor Único Estándar (tipo M/M/1)

## Config: arrival_gen: (45.0), service_gen: (40.0)

| # | Hora Actual | Evento | Estado P.S. | Cant. Cola | FEL: Próx. Llegada | FEL: Próx. Fin Serv. | Gráficamente |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 08:00:00 | INICIO | 0 | 0 | 08:00:45 | - | ◠[□] |
| 2 | 08:00:45 | LLEGADA | 1 | 0 | 08:01:30 | 08:01:25 | ◠[▣] |
| 3 | 08:01:25 | FIN_SERVICIO | 0 | 0 | 08:01:30 | - | ◠[□] |
| 4 | 08:01:30 | LLEGADA | 1 | 0 | 08:02:15 | 08:02:10 | ◠[▣] |
| 5 | 08:02:10 | FIN_SERVICIO | 0 | 0 | 08:02:15 | - | ◠[□] |
| 6 | 08:02:15 | LLEGADA | 1 | 0 | 08:03:00 | 08:02:55 | ◠[▣] |
| 7 | 08:02:55 | FIN_SERVICIO | 0 | 0 | 08:03:00 | - | ◠[□] |
| 8 | 08:03:00 | LLEGADA | 1 | 0 | 08:03:45 | 08:03:40 | ◠[▣] |
| 9 | 08:03:40 | FIN_SERVICIO | 0 | 0 | 08:03:45 | - | ◠[□] |
| 10 | 08:03:45 | LLEGADA | 1 | 0 | 08:04:30 | 08:04:25 | ◠[▣] |
| 11 | 08:04:25 | FIN_SERVICIO | 0 | 0 | 08:04:30 | - | ◠[□] |

# Servidor con Intervalos Trabajo/Descanso

## Config: arrival_gen: (65.0), rest_gen: (60.0), service_gen: (10.0), work_gen: (30.0)

| # | Hora Actual | Evento | Estado P.S. | Cant. Cola | FEL: Próx. Llegada | FEL: Próx. Fin Serv. | Gráficamente |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 08:00:00 | INICIO | 0 | 0 | 08:01:05 | - | ◠[□] |
| 2 | 08:00:30 | SALIDA_SERVIDOR | - | 0 | 08:01:05 | - | [□] |
| 3 | 08:01:05 | LLEGADA | - | 1 | 08:02:10 | - | [□]● |
| 4 | 08:01:30 | LLEGADA_SERVIDOR | 1 | 0 | 08:02:10 | 08:01:40 | ◠[▣] |
| 5 | 08:01:40 | FIN_SERVICIO | 0 | 0 | 08:02:10 | - | ◠[□] |
| 6 | 08:02:00 | SALIDA_SERVIDOR | - | 0 | 08:02:10 | - | [□] |
| 7 | 08:02:10 | LLEGADA | - | 1 | 08:03:15 | - | [□]● |
| 8 | 08:03:00 | LLEGADA_SERVIDOR | 1 | 0 | 08:03:15 | 08:03:10 | ◠[▣] |
| 9 | 08:03:10 | FIN_SERVICIO | 0 | 0 | 08:03:15 | - | ◠[□] |
| 10 | 08:03:15 | LLEGADA | 1 | 0 | 08:04:20 | 08:03:25 | ◠[▣] |
| 11 | 08:03:25 | FIN_SERVICIO | 0 | 0 | 08:04:20 | - | ◠[□] |

# Renegación (Abandono)

## Config: abandon_gen: (120.0), arrival_gen: (10.0), service_gen: (50.0)

| # | Hora Actual | Evento | Estado P.S. | Cant. Cola | FEL: Próx. Llegada | FEL: Próx. Fin Serv. | Gráficamente |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 08:00:00 | INICIO | 0 | 0 | 08:00:10 | - | ◠[□] |
| 2 | 08:00:10 | LLEGADA | 1 | 0 | 08:00:20 | 08:01:00 | ◠[▣] |
| 3 | 08:00:20 | LLEGADA | 1 | 1 | 08:00:30 | 08:01:00 | ◠[▣]● |
| 4 | 08:00:30 | LLEGADA | 1 | 2 | 08:00:40 | 08:01:00 | ◠[▣]●● |
| 5 | 08:00:40 | LLEGADA | 1 | 3 | 08:00:50 | 08:01:00 | ◠[▣]●●● |
| 6 | 08:00:50 | LLEGADA | 1 | 4 | 08:01:00 | 08:01:00 | ◠[▣]●●●● |
| 7 | 08:01:00 | FIN_SERVICIO | 1 | 3 | 08:01:00 | 08:01:50 | ◠[▣]●●● |
| 8 | 08:01:00 | LLEGADA | 1 | 4 | 08:01:10 | 08:01:50 | ◠[▣]●●●● |
| 9 | 08:01:10 | LLEGADA | 1 | 5 | 08:01:20 | 08:01:50 | ◠[▣]●●●●● |
| 10 | 08:01:20 | LLEGADA | 1 | 6 | 08:01:30 | 08:01:50 | ◠[▣]●●●●●● |
| 11 | 08:01:30 | LLEGADA | 1 | 7 | 08:01:40 | 08:01:50 | ◠[▣]●●●●●●● |

# Cola con Prioridad (Tipo A > B)

## Config: arrival_a_gen: (90.0), arrival_b_gen: (60.0), service_gen: (40.0)

| # | Hora Actual | Evento | Estado P.S. | Cant. Cola | FEL: Próx. Llegada | FEL: Próx. Fin Serv. | Gráficamente |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 08:00:00 | INICIO | 0 | 0 | - | - | ◠[□] |
| 2 | 08:01:00 | LLEGADA_B | 1 | 0 | - | 08:01:40 | ◠[▣] |
| 3 | 08:01:30 | LLEGADA_A | 1 | 1 | - | 08:01:40 | ◠[▣]● |
| 4 | 08:01:40 | FIN_SERVICIO | 1 | 0 | - | 08:02:20 | ◠[▣] |
| 5 | 08:02:00 | LLEGADA_B | 1 | 1 | - | 08:02:20 | ◠[▣]● |
| 6 | 08:02:20 | FIN_SERVICIO | 1 | 0 | - | 08:03:00 | ◠[▣] |
| 7 | 08:03:00 | LLEGADA_A | 1 | 1 | - | 08:03:00 | ◠[▣]● |
| 8 | 08:03:00 | LLEGADA_B | 1 | 2 | - | 08:03:00 | ◠[▣]●● |
| 9 | 08:03:00 | FIN_SERVICIO | 1 | 1 | - | 08:03:40 | ◠[▣]● |
| 10 | 08:03:40 | FIN_SERVICIO | 1 | 0 | - | 08:04:20 | ◠[▣] |
| 11 | 08:04:00 | LLEGADA_B | 1 | 1 | - | 08:04:20 | ◠[▣]● |

# Viaje a Zona de Seguridad

## Config: arrival_gen: (45.0), service_gen: (40.0), travel_gen: (10.0)

| # | Hora Actual | Evento | Estado P.S. | Cant. Cola | FEL: Próx. Llegada | FEL: Próx. Fin Serv. | Gráficamente |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 08:00:00 | INICIO | 0 | 0 | - | - | ◠[□] |
| 2 | 08:00:45 | event_arrival_system | 0 | 0 | - | - | ◠[□] |
| 3 | 08:00:45 | ENTRADA_ZS | 0 | 0 | - | - | ◠[□] |
| 4 | 08:00:55 | LLEGADA_PS | 1 | 0 | - | 08:01:35 | ◠[▣] |
| 5 | 08:01:30 | event_arrival_system | 1 | 1 | - | 08:01:35 | ◠[▣]● |
| 6 | 08:01:35 | FIN_SERVICIO | 0 | 0 | - | - | ◠[□] |
| 7 | 08:01:35 | ENTRADA_ZS | 0 | 0 | - | - | ◠[□] |
| 8 | 08:01:45 | LLEGADA_PS | 1 | 0 | - | 08:02:25 | ◠[▣] |
| 9 | 08:02:15 | event_arrival_system | 1 | 1 | - | 08:02:25 | ◠[▣]● |
| 10 | 08:02:25 | FIN_SERVICIO | 0 | 0 | - | - | ◠[□] |
| 11 | 08:02:25 | ENTRADA_ZS | 0 | 0 | - | - | ◠[□] |

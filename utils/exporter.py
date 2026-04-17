import os
import re
from typing import List, Dict, Any
from utils.generators import Generator

class Exporter:
    @staticmethod
    def get_config_id(problem_id: int, config: Dict[str, Any], i18n) -> str:
        """
        Generates a unique configuration string for the problem.
        Uses descriptions from generators.
        """
        parts = []
        # Sort keys to ensure consistent ID
        for key in sorted(config.keys()):
            val = config[key]
            if isinstance(val, Generator):
                parts.append(f"{key}: {val.get_desc(i18n.translate)}")
            else:
                parts.append(f"{key}: {val}")
        
        return ", ".join(parts)

    @staticmethod
    def format_history_to_md(history: List[Dict[str, Any]], i18n, cli_instance) -> str:
        """Converts history to a Markdown table."""
        if not history:
            return ""

        headers = [
            i18n.translate("col_index"),
            i18n.translate("col_time"),
            i18n.translate("col_event"),
            i18n.translate("col_state"),
            i18n.translate("col_queue"),
            i18n.translate("col_next_arrival"),
            i18n.translate("col_next_service"),
            i18n.translate("col_graphic")
        ]

        lines = []
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

        for idx, record in enumerate(history, 1):
            clock_formatted = cli_instance.format_time(record.get("clock", 0))
            
            # Event name (extracting name if it has rich tags)
            event_raw = record.get("last_event", "INICIO")
            if event_raw == "START": event = i18n.translate('event_start')
            elif event_raw == "ARRIVAL": event = i18n.translate('event_arrival')
            elif event_raw in ["END_SERVICE", "SERVICE_END"]: event = i18n.translate('event_service_end')
            elif event_raw == "SERVER_ARRIVAL": event = i18n.translate('event_server_arrival')
            elif event_raw == "SERVER_DEPARTURE": event = i18n.translate('event_server_departure')
            elif event_raw in ["ABANDONO", "RENEGING"]: event = i18n.translate('event_reneging')
            else: event = event_raw

            is_busy = record.get("server_busy", record.get("ps_busy", 0))
            is_present = record.get("server_present", 1)
            ps_state = "-" if is_present == 0 else str(is_busy)

            q_total = record.get("queue", 0)
            queue_count = str(q_total)

            fel = record.get("fel", {})
            next_arrival = fel.get("ARRIVAL", "-")
            if isinstance(next_arrival, (int, float)): next_arrival = cli_instance.format_time(next_arrival)
            
            next_end = fel.get("END_SERVICE", "-")
            if isinstance(next_end, (int, float)): next_end = cli_instance.format_time(next_end)

            # Graphic (Flattened for Markdown table)
            graphic = cli_instance.get_graphic_md(record)

            row = [
                str(idx),
                clock_formatted,
                event,
                ps_state,
                queue_count,
                str(next_arrival),
                str(next_end),
                graphic
            ]
            lines.append("| " + " | ".join(row) + " |")

        return "\n".join(lines)

    @staticmethod
    def save_result(problem_id: int, config: Dict[str, Any], history: List[Dict[str, Any]], i18n, cli_instance, file_path="results.md"):
        """Save results to results.md if not already present."""
        problem_title = f"{i18n.translate(f'problem_{problem_id}')}"
        config_desc = Exporter.get_config_id(problem_id, config, i18n)
        config_header = f"## Config: {config_desc}"
        
        content = ""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

        # Check if config already exists for this problem
        # We look for the combination of Problem Title and Config Header
        # More robust check: find the # Problem section first
        
        problem_section_pattern = rf"^# {re.escape(problem_title)}\s*$"
        has_problem = re.search(problem_section_pattern, content, re.MULTILINE)
        
        if has_problem:
            # Check if config exists within this problem section
            # We can find the start of the problem and the next problem or end of file
            start_pos = has_problem.end()
            next_problem = re.search(r"^# Problema", content[start_pos:], re.MULTILINE)
            end_pos = start_pos + next_problem.start() if next_problem else len(content)
            
            problem_content = content[start_pos:end_pos]
            if config_header in problem_content:
                # Already exists
                return False

        # If we reach here, we need to add it
        table_md = Exporter.format_history_to_md(history, i18n, cli_instance)
        new_entry = f"\n{config_header}\n\n{table_md}\n"
        
        if not has_problem:
            # Add problem header and internal config
            with open(file_path, "a", encoding="utf-8") as f:
                if content and not content.endswith("\n\n"):
                    f.write("\n")
                f.write(f"# {problem_title}\n")
                f.write(new_entry)
        else:
            # Insert under problem header
            # We insert at the end of the problem section
            insert_pos = has_problem.end()
            next_problem = re.search(r"^# Problema", content[insert_pos:], re.MULTILINE)
            if next_problem:
                final_insert_pos = insert_pos + next_problem.start()
                new_content = content[:final_insert_pos] + new_entry + content[final_insert_pos:]
            else:
                new_content = content + new_entry
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
                
        return True

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from utils.generators import ConstantGenerator, ListGenerator, Generator
from utils.i18n import I18n
import os
import webbrowser
import tempfile

console = Console()

class CLI:
    def __init__(self, language="en"):
        self.i18n = I18n(language)

    def _t(self, key, **kwargs):
        return self.i18n.translate(key, **kwargs)

    def select_language(self):
        self.clear()
        console.print(Panel.fit(
            "[bold blue]Seriat: Queuing System Simulator[/bold blue]",
            border_style="green"
        ))
        console.print(f"\n1. {self._t('lang_en')}")
        console.print(f"2. {self._t('lang_es')}")
        
        choice = IntPrompt.ask(self._t("select_language"), choices=["1", "2"], default=2)
        self.i18n.language = "en" if choice == 1 else "es"

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def welcome(self):
        self.clear()
        console.print(Panel.fit(
            f"[bold blue]{self._t('title')}[/bold blue]\n"
            f"[italic]{self._t('subtitle')}[/italic]",
            border_style="green"
        ))

    def select_problem(self) -> int:
        console.print(f"\n[bold yellow]{self._t('available_problems')}[/bold yellow]")
        console.print(f"1. {self._t('problem_1')}")
        console.print(f"2. {self._t('problem_2')}")
        console.print(f"3. {self._t('problem_3')}")
        
        return IntPrompt.ask(self._t("choose_problem"), choices=["1", "2", "3"], default=1)

    def get_generator_choice(self, name: str, default_const: float = 45.0) -> Generator:
        console.print(f"\n[bold]{self._t('config_generator', name=name)}[/bold]")
        console.print(f"1. {self._t('opt_constant', default_const=default_const)}")
        console.print(f"2. {self._t('opt_list')}")
        console.print(f"3. {self._t('opt_presets')}")
        
        choice = IntPrompt.ask(self._t("select_option"), choices=["1", "2", "3"], default=1)
        
        if choice == 1:
            val = float(Prompt.ask(self._t("enter_constant", name=name), default=str(default_const)))
            return ConstantGenerator(val)
        elif choice == 2:
            vals_str = Prompt.ask(self._t("enter_list", name=name))
            vals = [float(x.strip()) for x in vals_str.split(",") if x.strip()]
            return ListGenerator(vals)
        else:
            return self.get_preset_generator(name)

    def get_preset_generator(self, name: str) -> Generator:
        # Predefined sequences from TP1 tables
        presets = {
            "arrival": [65, 6, 2, 21, 42, 33, 21],
            "service": [5, 10, 35, 10, 20, 30],
            "abandon": [120],
            "work": [30],
            "rest": [60]
        }
        
        key = "arrival"
        if "service" in name.lower(): key = "service"
        elif "abandon" in name.lower(): key = "abandon"
        elif "work" in name.lower(): key = "work"
        elif "rest" in name.lower(): key = "rest"
        
        vals = presets.get(key, [45])
        console.print(self._t("using_presets", name=name, vals=vals))
        return ListGenerator(vals)

    def format_time(self, seconds: float) -> str:
        """Format seconds into HH:MM:SS starting from 08:00:00."""
        base_seconds = 8 * 3600
        total_seconds = int(base_seconds + seconds)
        h = (total_seconds // 3600) % 24
        m = (total_seconds // 60) % 60
        s = total_seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def display_results(self, history: list):
        if not history:
            console.print(f"[red]{self._t('no_history')}[/red]")
            return

        table = Table(title=self._t("results_title"), show_header=True, header_style="bold white on #1a202c")
        
        # Define Columns (matching screenshot)
        table.add_column(self._t("col_index"), justify="center")
        table.add_column(self._t("col_time"), justify="center", style="bold")
        table.add_column(self._t("col_event"), justify="center")
        table.add_column(self._t("col_state"), justify="center", style="bold")
        table.add_column(self._t("col_queue"), justify="center", style="blue")
        table.add_column(self._t("col_next_arrival"), justify="center", style="cyan")
        table.add_column(self._t("col_next_service"), justify="center", style="cyan")
        table.add_column(self._t("col_graphic"), justify="left")
        
        for idx, record in enumerate(history, 1):
            clock_formatted = self.format_time(record.get("clock", 0))
            event = record.get("last_event", "INICIO")
            
            # Robust mapping for Server State and Queue Count across all problems
            is_busy = record.get("server_busy", record.get("ps_busy", 0))
            is_present = record.get("server_present", 1)
            
            # S.P. State: Show 1 if busy, 0 if idle, and - if the server isn't even there
            if is_present == 0:
                ps_state = "-"
            else:
                ps_state = str(is_busy)

            # Queue Count: Sum up all queues (handles Problem 4 Priority A/B)
            q_total = record.get("queue", 0)
            queue_count = str(q_total)
            
            # FEL Extraction
            fel = record.get("fel", {})
            next_arrival = fel.get("ARRIVAL", "-")
            if isinstance(next_arrival, float): next_arrival = self.format_time(next_arrival)
            
            next_end = fel.get("END_SERVICE", "-")
            if isinstance(next_end, float): next_end = self.format_time(next_end)
            
            # Modern event mapping with distinct colors for server/abandonment
            if event == "START":
                event_display = f"[white on #4a5568] {self._t('event_start')} [/]"
            elif event == "ARRIVAL":
                event_display = f"[white on #3182ce] {self._t('event_arrival')} [/]"
            elif event == "END_SERVICE" or event == "SERVICE_END":
                event_display = f"[black on #c6f6d5] {self._t('event_service_end')} [/]"
            elif event == "SERVER_ARRIVAL":
                event_display = f"[white on #805ad5] {self._t('event_server_arrival')} [/]"
            elif event == "SERVER_DEPARTURE":
                event_display = f"[white on #9b2c2c] {self._t('event_server_departure')} [/]"
            elif event == "ABANDONO" or event == "RENEGING":
                event_display = f"[white on #dd6b20] {self._t('event_reneging')} [/]"
            else:
                event_display = event
                
            table.add_row(
                str(idx),
                clock_formatted,
                event_display,
                ps_state,
                queue_count,
                str(next_arrival),
                str(next_end),
                self._get_graphic_representation(record)
            )
            
        console.print(table)

    def _get_graphic_representation(self, record: dict) -> str:
        """Generate a graphical representation of the system state."""
        is_present = record.get("server_present", 1)
        is_busy = record.get("server_busy", record.get("ps_busy", 0))
        
        queue_count = record.get("queue", 0)

        # Symbols
        server_char = "▣" if is_busy else "□"
        active_char = "◠" if is_present else " "
        queue_chars = " ●" * int(queue_count)

        # Return a 2-line representation
        return f" {active_char} \n[{server_char}]{queue_chars}"

    def get_graphic_md(self, record: dict) -> str:
        """Generate a single-line graphical representation for Markdown tables."""
        is_present = record.get("server_present", 1)
        is_busy = record.get("server_busy", record.get("ps_busy", 0))
        
        queue_count = record.get("queue", 0)

        # Symbols
        server_char = "▣" if is_busy else "□"
        active_char = "◠" if is_present else ""
        queue_chars = "●" * int(queue_count)
        
        # Format: ◠[▣]●●
        return f"{active_char}[{server_char}]{queue_chars}"

    def display_diagram(self, sim):
        """Display the logical event flow diagram in Mermaid format."""
        diagram = sim.get_mermaid_diagram(self.i18n.translate)
        console.print(f"\n[bold yellow] {self._t('diagram_title')} [/bold yellow]")
        console.print(Panel(
            f"```mermaid\n{diagram}\n```",
            title="Mermaid logic",
            border_style="cyan"
        ))
        
        if Confirm.ask(f"\n{self._t('prompt_render')}", default=True):
            self._render_mermaid_html(diagram)

    def _render_mermaid_html(self, diagram: str):
        """Generate a temporary HTML file and open it in the browser."""
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Seriat - Logical Event Flow</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    background-color: #f7fafc;
                    margin: 0;
                    padding: 20px;
                }}
                h1 {{ color: #2d3748; }}
                .mermaid {{ 
                    background: white; 
                    padding: 20px; 
                    border-radius: 8px; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
            </style>
        </head>
        <body>
            <h1>{self._t('diagram_title')}</h1>
            <pre class="mermaid">
{diagram}
            </pre>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
            </script>
        </body>
        </html>
        """
        
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f:
            f.write(html_template)
            tmp_path = f.name
            
        console.print(f"[cyan]{self._t('msg_opening_diagram')}[/cyan]")
        webbrowser.open('file://' + os.path.realpath(tmp_path))

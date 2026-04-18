import sys
from ui.cli import CLI
from sim.problems.problem1 import Problem1
from sim.problems.problem2 import Problem2
from sim.problems.problem3 import Problem3
from rich.prompt import IntPrompt
from utils.exporter import Exporter

def main():
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            # Handle cases where reconfigure is not available
            pass
    cli = CLI("es")
    cli.select_language()
    cli.welcome()
    
    problem_choice = cli.select_problem()
    
    config = {}
    
    if problem_choice == 1:
        config["arrival_gen"] = cli.get_generator_choice(cli._t("gen_arrival"), 45)
        config["service_gen"] = cli.get_generator_choice(cli._t("gen_service"), 40)
        sim = Problem1(**config)
    elif problem_choice == 2:
        config["arrival_gen"] = cli.get_generator_choice(cli._t("gen_arrival"), 65)
        config["service_gen"] = cli.get_generator_choice(cli._t("gen_service"), 10)
        config["work_gen"] = cli.get_generator_choice(cli._t("gen_work"), 30)
        config["rest_gen"] = cli.get_generator_choice(cli._t("gen_rest"), 60)
        sim = Problem2(**config)
    elif problem_choice == 3:
        config["arrival_gen"] = cli.get_generator_choice(cli._t("gen_arrival"), 10)
        config["service_gen"] = cli.get_generator_choice(cli._t("gen_service"), 50)
        config["abandon_gen"] = cli.get_generator_choice(cli._t("gen_abandon"), 120)
        sim = Problem3(**config)

    max_events = IntPrompt.ask(f"\n{cli._t('how_many_events')}", default=10)
    
    sim.run_simulation(max_events)
    
    cli.display_results(sim.history)
    cli.display_diagram(sim)
    
    # Export results to results.md
    if Exporter.save_result(problem_choice, config, sim.history, cli.i18n, cli):
        print(f"\n[✓] {cli._t('msg_results_exported')}")
    else:
        print(f"\n[i] {cli._t('msg_results_already_exists')}")

if __name__ == "__main__":
    main()

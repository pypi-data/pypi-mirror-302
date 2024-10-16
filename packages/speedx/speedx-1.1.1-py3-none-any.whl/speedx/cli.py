import click
from colorama import Fore, Style
from .core import run_speed_test
from .history import save_report, get_latest_reports
from .graphs import plot_speed_graph

@click.group()
def cli():
    """SpeedX - A simple network speed tester."""
    pass

@cli.command()
def test():
    """Run a speed test."""
    report = run_speed_test()
    
    # Display test results with colors
    click.echo(Fore.GREEN + f"Download Speed: {report['download_speed']} Mbps" + Style.RESET_ALL)
    click.echo(Fore.BLUE + f"Upload Speed: {report['upload_speed']} Mbps" + Style.RESET_ALL)
    click.echo(Fore.YELLOW + f"Latency (Ping): {report['ping']} ms" + Style.RESET_ALL)
    click.echo(Fore.CYAN + f"IP Address: {report['ip_address']}" + Style.RESET_ALL)
    click.echo(Fore.MAGENTA + f"Server: {report['server']['name']}, {report['server']['country']} ({report['server']['host']})" + Style.RESET_ALL)

    # Save the report
    save_report(report)
    click.echo(Fore.GREEN + "Test results saved." + Style.RESET_ALL)

    # Plot the graph for the latest results
    history_reports = get_latest_reports()
    if history_reports:
        plot_speed_graph(history_reports)


@cli.command()
@click.option('--limit', default=5, help='Number of latest reports to show')
def history(limit):
    """Show the history of speed tests."""
    reports = get_latest_reports(limit)
    if not reports:
        click.echo(Fore.RED + "No history found." + Style.RESET_ALL)
        return
    
    click.echo(Fore.YELLOW + f"Showing last {len(reports)} tests:" + Style.RESET_ALL)
    for i, report in enumerate(reports, 1):
        click.echo(Fore.LIGHTWHITE_EX + f"\nTest {i}:" + Style.RESET_ALL)
        click.echo(Fore.GREEN + f"Download Speed: {report['download_speed']} Mbps" + Style.RESET_ALL)
        click.echo(Fore.BLUE + f"Upload Speed: {report['upload_speed']} Mbps" + Style.RESET_ALL)
        click.echo(Fore.YELLOW + f"Latency (Ping): {report['ping']} ms" + Style.RESET_ALL)
        click.echo(Fore.CYAN + f"IP Address: {report['ip_address']}" + Style.RESET_ALL)
        click.echo(Fore.MAGENTA + f"Server: {report['server']['name']}, {report['server']['country']} ({report['server']['host']})" + Style.RESET_ALL)

    # Plot the graph for the history
    plot_speed_graph(reports)

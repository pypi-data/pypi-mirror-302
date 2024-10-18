import click

__version__ = "2.0.0"


@click.group(help=f"theTrial CLI Tool v{__version__}")
@click.version_option(version=__version__, prog_name="theTrial")
def main():
    pass


@click.command("start", short_help="Init your application.")
@click.option("--name", default="app", help="Name of the application.")
def start_command(name: str) -> None:
    """Initialize a new project structure."""
    pass


@click.command("run", short_help="Run the application.")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging.")
def run_command(verbose):
    """Run the application."""
    pass


main.add_command(start_command)
main.add_command(run_command)

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)


class ConsoleLogger:

    def __init__(self):
        self.console = Console()

    def get_console(self):
        return self.console

    def show_header(self):
        self.console.clear()
        self.console.print(
            Panel.fit(
                "[bold cyan]YouTube MP3 Downloader[/bold cyan]\n[dim]Baixe áudios com qualidade e estilo![/dim]",
                border_style="cyan",
            )
        )

    def show_message(self, msg: str):
        self.console.print(msg)

    def show_warning(self, msg: str):
        self.console.print(f"[yellow][WARNING] {msg}[/yellow]")

    def show_error(self, msg: str):
        self.console.print(f"[red][ERRO] {msg}[/red]")

    def create_progress(self) -> Progress:
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=self.console,
        )


class YtDlpLogger:
    def __init__(self, ui: ConsoleLogger):
        self.ui = ui

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        self.ui.show_error(msg)

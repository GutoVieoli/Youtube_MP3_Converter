# pylint: disable=missing-function-docstring
# pylint: disable=broad-exception-caught
import os
import shutil
import platform
import concurrent.futures
import yt_dlp
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
import questionary

console = Console()


def get_ffmpeg_path():
    pasta_projeto = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == "Linux":
        return shutil.which("ffmpeg")
    return os.path.join(pasta_projeto, "ffmpeg/ffmpeg.exe")


def show_header():
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]YouTube MP3 Downloader[/bold cyan]\n[dim]Baixe áudios com qualidade e estilo![/dim]",
            border_style="cyan",
        )
    )


class IDLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        console.print(f"[red][ERRO] {msg}[/red]")


def progress_hook(d, task_id, progress):
    if d["status"] == "downloading":
        total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate")
        downloaded_bytes = d.get("downloaded_bytes", 0)
        if total_bytes:
            progress.update(task_id, total=total_bytes, completed=downloaded_bytes)
    elif d["status"] == "finished":
        progress.update(task_id, completed=d.get("total_bytes"), description="[green]Processando MP3...[/green]")


def baixar_audio(url: str, quality: int, progress: Progress, task_id):
    pasta_projeto = os.path.dirname(os.path.abspath(__file__))
    caminho_ffmpeg = get_ffmpeg_path()
    pasta_destino = os.path.join(pasta_projeto, "downloads")
    os.makedirs(pasta_destino, exist_ok=True)

    if not caminho_ffmpeg or (platform.system() != "Linux" and not os.path.exists(caminho_ffmpeg)):
        console.print("[red]FFmpeg não encontrado! Verifique a instalação.[/red]")
        return

    ydl_opts = {
        "format": "bestaudio/best",
        "ffmpeg_location": caminho_ffmpeg,
        "outtmpl": os.path.join(pasta_destino, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": str(quality),
            }
        ],
        "logger": IDLogger(),
        "progress_hooks": [lambda d: progress_hook(d, task_id, progress)],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "Desconhecido")
            progress.update(task_id, description=f"[cyan]Baixando: {title}[/cyan]")
            ydl.download([url])
            progress.update(task_id, description=f"[green]Concluído: {title}[/green]")
    except Exception as exc:
        progress.update(task_id, description=f"[red]Erro: {exc}[/red]")


def processar_lista_urls(arquivo: str, quality: int):
    if not os.path.exists(arquivo):
        console.print(f"[red]Arquivo não encontrado: {arquivo}[/red]")
        return

    urls = []
    try:
        with open(arquivo, "r", encoding="utf-8") as F:
            urls = [line.strip() for line in F if line.strip().startswith(("http", "https"))]
    except Exception as e:
        console.print(f"[red]Erro ao ler arquivo: {e}[/red]")
        return

    if not urls:
        console.print("[yellow]Nenhuma URL válida encontrada.[/yellow]")
        return
    
    console.print(f"\n[bold green]Iniciando download de {len(urls)} vídeos...[/bold green]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        
        # Create a task for each URL immediately so they show up
        tasks = {}
        for url in urls:
            task_id = progress.add_task(f"[dim]Aguardando: {url}[/dim]", start=False)
            tasks[url] = task_id

        # Run downloads in parallel (max 3 workers)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for url in urls:
                task_id = tasks[url]
                progress.start_task(task_id)
                futures.append(executor.submit(baixar_audio, url, quality, progress, task_id))
            concurrent.futures.wait(futures)

    console.print(Panel("[bold green]Todos os downloads concluídos![/bold green]", border_style="green"))


def main():
    while True:
        show_header()
        
        modo = questionary.select(
            "Escolha o modo de operação:",
            choices=[
                "Única URL",
                "Lote de URLs (arquivo .txt)",
                "Sair"
            ]
        ).ask()

        if modo == "Sair":
            console.print("[blue]Até logo![/blue]")
            break

        quality_str = questionary.select(
            "Escolha a qualidade do áudio:",
            choices=[
                "128 Kbps (Baixa)",
                "192 Kbps (Recomendada)",
                "256 Kbps (Alta)"
            ]
        ).ask()
        
        quality = int(quality_str.split()[0])

        if modo == "Única URL":
            url = questionary.text("Cole a URL do vídeo do YouTube:").ask()
            if url:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeRemainingColumn(),
                    console=console,
                ) as progress:
                    task_id = progress.add_task("[cyan]Iniciando...[/cyan]", total=None)
                    baixar_audio(url, quality, progress, task_id)
                
                input("\nPressione Enter para continuar...")

        else:
            caminho_txt = questionary.text(
                "Caminho do arquivo .txt:",
                default="batch.txt"
            ).ask()
            
            # Limpa aspas extras se houver
            caminho_txt = caminho_txt.replace('"', "").replace("'", "").strip()
            
            if caminho_txt:
                processar_lista_urls(caminho_txt, quality)
                input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Interrompido pelo usuário.[/red]")

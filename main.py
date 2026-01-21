# pylint: disable=missing-function-docstring
# pylint: disable=broad-exception-caught
import os
import yt_dlp


def baixar_audio(url: str, quality: int):

    # Configuração de caminhos
    # Pega a pasta onde este script (.py) está localizado
    pasta_projeto = os.path.dirname(os.path.abspath(__file__))
    caminho_ffmpeg = os.path.join(pasta_projeto, "ffmpeg/ffmpeg.exe")

    pasta_destino = os.path.join(pasta_projeto, "downloads")
    os.makedirs(pasta_destino, exist_ok=True)

    if not os.path.exists(caminho_ffmpeg):
        print("=" * 60)
        print("ERRO: ffmpeg.exe não encontrado na pasta!")
        print(f"Certifique-se de que o ffmpeg.exe esteja em: {pasta_projeto}/ffmpeg")
        print("=" * 60)
        return

    ydl_opts = {
        "format": "bestaudio/best",
        "ffmpeg_location": caminho_ffmpeg,  # Força o uso do EXE da pasta
        "outtmpl": os.path.join(pasta_destino, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": str(quality),
            }
        ],
        # Evita warnings chatos de interface
        "quiet": False,
        "no_warnings": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\n[INFO] Analisando: {url}")
            ydl.download([url])
            print("\n" + "=" * 60)
            print("CONCLUÍDO COM SUCESSO!")
            print("O seu MP3 está na pasta do script.")
            print("Pressione Ctrl+C para sair ou baixe mais áudios.")
            print("=" * 60 + "\n")
    except Exception as exc:
        print(f"\n[ERRO] Ocorreu um problema: {exc}")


def cabecalho_programa() -> str:
    print("=" * 60)
    print("Bem-vindo ao dowloader de áudio MP3 do Youtube!")
    print("Sinta-se a vontade para mexer no código e alterá-lo")
    print("=" * 60)


def ler_url() -> str:
    while True:
        input_url = input("Cole a URL do vídeo do YouTube: ").strip()
        if not input_url:
            continue
        elif not input_url.startswith(("http://", "https://")):
            print("\nURL inválida. Deve começar com http:// ou https://")
        else:
            return input_url


def ler_qualidade_kbps() -> int:
    print("\nDigite a opção escolhida para qualidade do áudio: ")

    while True:
        print("[A] - 128 Kbps (baixa)")
        print("[B] - 192 Kbps (recomendada)")
        print("[C] - 256 Kbps (alta)")
        input_quality = input("Digite: ").strip().upper()

        if not input_quality or input_quality not in ["A", "B", "C"]:
            print("\nOpção inválida, digite somente A, B ou C.")
        else:
            if input_quality == "A":
                return 128
            elif input_quality == "B":
                return 192
            else:
                return 256


if __name__ == "__main__":
    try:
        cabecalho_programa()

        while True:
            url: str = ler_url()
            quality: int = ler_qualidade_kbps()
            baixar_audio(url=url, quality=quality)

    except KeyboardInterrupt:
        print("\n\nPrograma encerrado pelo usuário.\n")

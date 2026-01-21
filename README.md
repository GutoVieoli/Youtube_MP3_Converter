# 🎵 YouTube MP3 Converter

Um conversor simples de **YouTube para MP3**, feito em Python, criado para resolver um problema pessoal:  
Evitar sites lentos, cheios de propagandas e vírus e com limites artificiais para download de áudio.

O projeto utiliza a biblioteca **yt-dlp** junto com um **ffmpeg.exe local**, eliminando a necessidade de instalar o ffmpeg no sistema ou configurar variáveis de ambiente.

---

## 🚀 Funcionalidades

- Baixa áudio de vídeos do YouTube
- Converte automaticamente para **MP3**
- Escolha de qualidade:
  - 128 kbps (baixa)
  - 192 kbps (recomendada)
  - 256 kbps (alta)
- Download direto para a pasta de downloads do projeto
- Interface simples via terminal
- Sem anúncios, sem limites e sem dependência de sites externos

---

## 🛠️ Tecnologias utilizadas

- **Python 3**
- **yt-dlp**
- **FFmpeg (ffmpeg.exe incluso no projeto)**

---

## 📂 Estrutura do projeto

```

youtube-mp3-converter/
│
├── main.py
├── requirements.txt
├── downloads/
└── ffmpeg/
   ├── ffmpeg.exe
   └── ffprobe.exe

````

---

## 📦 Requisitos

- Python 3.9 ou superior
- Sistema operacional: **Windows** (uso do ffmpeg.exe)

---

## ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/GutoVieoli/Youtube_MP3_Converter.git
    ```

2. Entre na pasta do projeto:

   ```bash
   cd Youtube_MP3_Converter
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

> O `requirements.txt` contém apenas a versão do **yt-dlp**, mantendo o projeto simples e limpo.

---

## ▶️ Como usar

Execute o programa com:

```bash
python main.py
```

### Passo a passo:

1. Cole a URL do vídeo do YouTube
2. Escolha a qualidade do áudio:

   * A → 128 kbps
   * B → 192 kbps
   * C → 256 kbps
3. O MP3 será baixado e salvo automaticamente na pasta `downloads`


---

## ⚠️ Observações

* O projeto é destinado **apenas para uso pessoal**
* Certifique-se de respeitar os **termos do YouTube** e os **direitos autorais**
* O nome do arquivo é baseado no título do vídeo

---

## 🧠 Motivação

Este projeto foi criado para:

* Evitar sites online cheios de propagandas
* Ter mais controle sobre qualidade e destino dos arquivos
* Aprender e praticar automação com Python

---

## 📄 Licença

Este projeto é de uso livre para fins educacionais e pessoais.

import pytubefix
import ffmpeg
import openai
import tkinter as tk

from tkinter import filedialog, messagebox, ttk
from pytubefix import YouTube
from pytubefix.cli import on_progress


def baixar_video():
    link = entrada_link.get()
    if not link:
        messagebox.showwarning("Aviso", "Por favor, insira o link do vídeo.")
        return

    try:
        yt = YouTube(link, on_progress_callback=on_progress)
        
        # Usar o título do vídeo sem alterar a codificação
        titulo_texto = yt.title
        titulo.config(text=f"Baixando: {titulo_texto}")

        progresso.start()

        ys = yt.streams.get_highest_resolution()
        download_path = filedialog.askdirectory(title="Selecione a pasta de download")

        if download_path:
            ys.download(output_path=download_path)
            progresso.stop()
            progresso['value'] = 100
            messagebox.showinfo("Sucesso", f"Download concluído com sucesso em {download_path}!")
        else:
            progresso.stop()
            messagebox.showwarning("Aviso", "Nenhuma pasta selecionada.")
    except Exception as e:
        progresso.stop()
        messagebox.showerror("Erro", f"Algo deu errado: {str(e)}")

# Criando a janela principal
janela = tk.Tk()
janela.title("YouTube Video Downloader")
janela.geometry("500x300")
janela.configure(bg="#282c34")

# Estilos
estilo_label = {'font': ('Helvetica', 12), 'bg': '#282c34', 'fg': '#ffffff'}
estilo_entry = {'font': ('Helvetica', 12)}
estilo_botao = {'font': ('Helvetica', 12, 'bold'), 'bg': '#61afef', 'fg': '#ffffff', 'bd': 0, 'activebackground': '#3e4451'}

# Entrada para o link do vídeo
tk.Label(janela, text="Insira o link do vídeo:", **estilo_label).pack(pady=10)
entrada_link = tk.Entry(janela, width=50, **estilo_entry)
entrada_link.pack(pady=10)

# Botão para iniciar o download
botao_baixar = tk.Button(janela, text="Baixar Vídeo", command=baixar_video, **estilo_botao)
botao_baixar.pack(pady=20)

# Label para exibir o título do vídeo
titulo = tk.Label(janela, text="", **estilo_label)
titulo.pack(pady=10)

# Barra de progresso
progresso = ttk.Progressbar(janela, orient="horizontal", length=400, mode="indeterminate")
progresso.pack(pady=20)

# Mantendo a janela aberta
janela.mainloop()
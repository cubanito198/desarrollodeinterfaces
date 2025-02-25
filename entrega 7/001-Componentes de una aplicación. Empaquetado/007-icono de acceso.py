import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import threading
import subprocess
import sys

class Installer(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Instalador de Space Invaders")
        self.geometry("500x450")
        self.resizable(False, False)
        
        self.install_path = tk.StringVar(value=os.getcwd())
        
        self.frames = {}
        for F in (WelcomeScreen, SelectFolderScreen, ProgressScreen, SuccessScreen):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(WelcomeScreen)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

class WelcomeScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        title_label = ttk.Label(self, text="Bienvenido al Instalador", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        description_label = ttk.Label(self, text="Siga los pasos para instalar el juego.")
        description_label.pack(pady=10)
        
        next_button = ttk.Button(self, text="Siguiente", command=lambda: parent.show_frame(SelectFolderScreen), bootstyle=PRIMARY)
        next_button.pack(pady=20)

class SelectFolderScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        instruction_label = ttk.Label(self, text="Seleccione la carpeta de instalación", font=("Arial", 12, "bold"))
        instruction_label.pack(pady=20)
        
        folder_frame = ttk.Frame(self)
        folder_frame.pack(pady=5)
        
        self.folder_entry = ttk.Entry(folder_frame, textvariable=parent.install_path, width=40)
        self.folder_entry.pack(side="left", padx=(0, 10))
        
        browse_button = ttk.Button(folder_frame, text="Buscar...", command=self.browse_folder, bootstyle=SECONDARY)
        browse_button.pack(side="left")
        
        self.next_button = ttk.Button(self, text="Siguiente", command=lambda: parent.show_frame(ProgressScreen), bootstyle=SUCCESS)
        self.next_button.pack(pady=20)

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=os.getcwd(), title="Seleccionar carpeta de instalación")
        if folder:
            self.master.install_path.set(folder)

class ProgressScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        title_label = ttk.Label(self, text="Instalando...", font=("Arial", 14, "bold"))
        title_label.pack(pady=20)
        
        self.progress = ttk.Progressbar(self, orient=HORIZONTAL, length=300, mode="determinate", bootstyle=SUCCESS)
        self.progress.pack(pady=10)
        
        self.status_label = ttk.Label(self, text="Preparando instalación...")
        self.status_label.pack(pady=5)
        
        self.next_button = ttk.Button(self, text="Siguiente", command=lambda: parent.show_frame(SuccessScreen), bootstyle=SUCCESS)
        self.next_button.pack(pady=20)
        self.next_button.config(state="disabled")

    def on_show(self):
        threading.Thread(target=self.start_installation, daemon=True).start()

    def start_installation(self):
        install_folder = self.master.install_path.get()
        os.makedirs(install_folder, exist_ok=True)
        
        game_files = ["programa_instalado.py", "player.png", "enemy.png", "bullet.png"]
        for i, file in enumerate(game_files):
            src = os.path.join(os.getcwd(), file)
            dest = os.path.join(install_folder, file)
            if os.path.exists(src):
                shutil.copy(src, dest)
            self.progress["value"] = (i + 1) / len(game_files) * 100
            self.status_label.config(text=f"Copiando {file}...")
            self.update_idletasks()
            threading.Event().wait(0.5)
        
        self.status_label.config(text="Instalación completada.")
        self.next_button.config(state="normal")

class SuccessScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        success_label = ttk.Label(self, text="¡Instalación Completa!", font=("Arial", 14, "bold"))
        success_label.pack(pady=20)
        
        detail_label = ttk.Label(self, text="El juego se ha instalado correctamente.")
        detail_label.pack(pady=10)
        
        launch_button = ttk.Button(self, text="Abrir juego", command=self.launch_game, bootstyle=PRIMARY)
        launch_button.pack(pady=10)

        exit_button = ttk.Button(self, text="Finalizar", command=self.master.destroy, bootstyle=DANGER)
        exit_button.pack(pady=10)

    def launch_game(self):
        game_path = os.path.join(self.master.install_path.get(), "programa_instalado.py")
        if os.path.exists(game_path):
            subprocess.Popen([sys.executable, game_path], cwd=self.master.install_path.get())
        else:
            messagebox.showerror("Error", "No se encontró el archivo del juego.")

if __name__ == "__main__":
    app = Installer()
    app.mainloop()

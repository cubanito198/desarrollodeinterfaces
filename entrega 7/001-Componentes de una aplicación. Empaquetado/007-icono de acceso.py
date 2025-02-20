import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import zipfile
import os
import threading
import subprocess
import sys
import platform

# Intentar importar winshell y pywin32 para la creación de accesos directos en Windows
try:
    import winshell
    from win32com.client import Dispatch
    WINDOWS_SHORTCUT_AVAILABLE = True
except ImportError:
    WINDOWS_SHORTCUT_AVAILABLE = False

class Installer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg='#282828')  # Color de fondo oscuro
        
        self.title("Instalador coches")
        self.geometry("500x450")  # Tamaño de la ventana
        self.resizable(False, False)  # Evita que la ventana sea redimensionable
        
        self.install_path = tk.StringVar(value=os.getcwd())  # Carpeta de instalación por defecto
        
        self.frames = {}  # Diccionario que almacenará las diferentes pantallas del instalador
        
        # Crear e inicializar las pantallas del instalador
        for F in (WelcomeScreen, SelectFolderScreen, ProgressScreen, SuccessScreen):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(WelcomeScreen)  # Mostrar la primera pantalla

    def show_frame(self, frame_class):
        """Muestra la pantalla especificada."""
        frame = self.frames[frame_class]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

class WelcomeScreen(tk.Frame):
    """Pantalla de bienvenida del instalador."""
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#282828')

        # Mensaje de bienvenida
        title_label = tk.Label(self, text="Hola, este es el instalador de Porsche", font=("Arial", 16, "bold"), fg="white", bg="#282828")
        title_label.pack(pady=20)
        
        # Descripción del proceso de instalación
        description_label = tk.Label(self, text="Sigue los pasos para instalar\nel programa de Porsche.", fg="white", bg="#282828")
        description_label.pack(pady=10)
        
        # Botón para continuar
        next_button = ttk.Button(self, text="Next", command=self.go_next)
        next_button.pack(pady=20)
        
        self.parent = parent

    def go_next(self):
        """Avanza a la siguiente pantalla."""
        self.parent.show_frame(SelectFolderScreen)

class SelectFolderScreen(tk.Frame):
    """Pantalla para seleccionar la carpeta de instalación."""
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#282828')

        # Instrucciones
        instruction_label = tk.Label(self, text="Seleccione la carpeta de instalación", font=("Arial", 12, "bold"), fg="white", bg="#282828")
        instruction_label.pack(pady=20)
        
        folder_frame = tk.Frame(self)
        folder_frame.pack(pady=5)
        
        # Campo de entrada para la ruta de la carpeta
        self.folder_entry = tk.Entry(folder_frame, textvariable=parent.install_path, width=40, bg="#3c3c3c", fg="white", insertbackground="white")
        self.folder_entry.pack(side="left", padx=(0, 10))
        
        # Botón para buscar carpeta
        browse_button = ttk.Button(folder_frame, text="Buscar...", command=self.browse_folder)
        browse_button.pack(side="left")
        
        # Mensaje de error si la carpeta no es válida
        self.error_label = tk.Label(self, text="", fg="red", font=("Arial", 10))
        self.error_label.pack(pady=5)
        
        # Botón de siguiente (deshabilitado hasta que la carpeta sea válida)
        self.next_button = ttk.Button(self, text="Next", command=self.go_next)
        self.next_button.pack(pady=20)
        self.next_button.config(state="disabled")
        
        self.parent = parent
        self.parent.install_path.trace_add('write', self.on_path_change)
        self.check_folder_empty()

    def browse_folder(self):
        """Abre el explorador de archivos para seleccionar una carpeta."""
        folder = filedialog.askdirectory(initialdir=os.getcwd(), title="Seleccionar carpeta de instalación")
        if folder:
            self.parent.install_path.set(folder)
    
    def on_path_change(self, *args):
        self.check_folder_empty()
    
    def check_folder_empty(self):
        """Verifica si la carpeta seleccionada está vacía."""
        path = self.parent.install_path.get()
        if os.path.isdir(path):
            try:
                if not os.listdir(path):
                    self.next_button.config(state="normal")
                    self.error_label.config(text="")
                else:
                    self.next_button.config(state="disabled")
                    self.error_label.config(text="La carpeta seleccionada no está vacía. Seleccione otra.")
            except PermissionError:
                self.next_button.config(state="disabled")
                self.error_label.config(text="No tienes permisos para acceder a esta carpeta.")
        else:
            self.next_button.config(state="disabled")
            self.error_label.config(text="Ruta inválida.")

    def go_next(self):
        """Avanza a la pantalla de progreso."""
        self.parent.show_frame(ProgressScreen)
       


class ProgressScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#282828')  # Fondo oscuro

        
        # Title
        title_label = tk.Label(self, text="Installing...", font=("Arial", 14, "bold"),fg="white", bg="#282828")
        title_label.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(self, text="Preparing to install...", font=("Arial", 10),fg="white", bg="#282828")
        self.status_label.pack(pady=5)
        
        # Next button (initially disabled)
        self.next_button = ttk.Button(self, text="Next", command=self.go_next)
        self.next_button.pack(pady=20)
        self.next_button.config(state="disabled")
        
        self.parent = parent
        self.installation_started = False  # Flag to prevent multiple starts

    def on_show(self):
        """
        Called when the ProgressScreen is shown.
        Starts the extraction if not already started.
        """
        if not self.installation_started:
            self.installation_started = True
            threading.Thread(target=self.start_extraction, daemon=True).start()

    def start_extraction(self):
        archivo_original = "paquete.zip"
        salida = self.parent.install_path.get()
        
        # Determine the path of the zip file relative to the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        zip_path = os.path.join(script_dir, archivo_original)
        
        if not os.path.isfile(zip_path):
            messagebox.showerror("Error", f"Cannot find '{archivo_original}' in '{script_dir}'.")
            self.status_label.config(text="Installation failed.")
            return

        try:
            with zipfile.ZipFile(zip_path, 'r') as zipped:
                # Get file list to compute progress
                file_list = zipped.namelist()
                total_files = len(file_list)
                
                for i, file in enumerate(file_list, start=1):
                    zipped.extract(file, salida)
                    
                    # Update progress
                    progress_value = int((i / total_files) * 100)
                    self.progress["value"] = progress_value
                    
                    # Update UI elements
                    self.status_label.config(text=f"Extracting {file} ({i}/{total_files})")
                    self.parent.update_idletasks()
            
            # Extraction successful
            self.status_label.config(text="Extraction completed.")
            self.next_button.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during extraction:\n{str(e)}")
            self.status_label.config(text="Installation failed.")

    def go_next(self):
        self.parent.show_frame(SuccessScreen)

class SuccessScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#282828')  # Fondo oscuro

        
        # Title
        success_label = tk.Label(self, text="Instalacion completada!", font=("Arial", 14, "bold"),fg="white", bg="#282828")
        success_label.pack(pady=20)
        
        # Description
        detail_label = tk.Label(self, text="tu programa se a instalado correctamente", font=("Arial", 10),fg="white", bg="#282828")
        detail_label.pack(pady=10)
        
        # Checkbox variable
        self.launch_var = tk.BooleanVar(value=True)  # Default to checked
        
        # Checkbox
        self.launch_checkbox = tk.Checkbutton(
            self,
            text="Iniciar la aplicacion ahora",
            variable=self.launch_var,
            font=("Arial", 10),
            bg="#282828", fg="white", selectcolor="#282828"
        )
        self.launch_checkbox.pack(pady=10)
        
        # Checkbox for creating desktop shortcut
        self.shortcut_var = tk.BooleanVar(value=True)  # Default to checked
        self.shortcut_checkbox = tk.Checkbutton(
            self,
            text="crear acceso directo",
            variable=self.shortcut_var,
            font=("Arial", 10),
            bg="#282828", fg="white", selectcolor="#282828"
        )
        self.shortcut_checkbox.pack(pady=5)
        
        # Exit button
        exit_button = ttk.Button(self, text="Finish", command=self.finish_installation)
        exit_button.pack(pady=20)
        
        self.parent = parent

    def finish_installation(self):
        # Create desktop shortcut if the checkbox is selected
        if self.shortcut_var.get():
            threading.Thread(target=self.create_shortcut, daemon=True).start()
        
        # Launch the application if the checkbox is selected
        if self.launch_var.get():
            self.launch_main_py()
        
        # Close the installer
        self.parent.destroy()

    def create_shortcut(self):
        current_os = platform.system()
        target_path = os.path.join(self.parent.install_path.get(), "main.py")
        shortcut_name = "My Application"  # You can customize the shortcut name
        
        if not os.path.isfile(target_path):
            messagebox.showerror("Error", f"Cannot find 'main.py' in '{self.parent.install_path.get()}'. Cannot create shortcut.")
            return
        
        if current_os == "Windows":
            self.create_windows_shortcut(target_path, shortcut_name)
        elif current_os == "Darwin":
            self.create_macos_shortcut(target_path, shortcut_name)
        elif current_os == "Linux":
            self.create_linux_shortcut(target_path, shortcut_name)
        else:
            messagebox.showerror("Error", f"Unsupported operating system: {current_os}. Cannot create shortcut.")

    def create_windows_shortcut(self, target_path, shortcut_name):
        if not WINDOWS_SHORTCUT_AVAILABLE:
            messagebox.showerror("Error", "winshell and pywin32 modules are not installed. Unable to create shortcut on Windows.")
            return
        
        try:
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, f"{shortcut_name}.lnk")
            with winshell.shortcut(shortcut_path) as link:
                link.path = sys.executable
                link.arguments = f'"{target_path}"'
                link.description = "Launch My Application"
                link.icon_location = (sys.executable, 0)
            messagebox.showinfo("Success", "Desktop shortcut created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create Windows shortcut:\n{str(e)}")

    def create_macos_shortcut(self, target_path, shortcut_name):
        try:
            # Path to the desktop
            desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
            alias_path = os.path.join(desktop, f"{shortcut_name}.app")
            
            # AppleScript to create alias
            applescript = f'''
            tell application "Finder"
                make alias file to POSIX file "{target_path}" at POSIX file "{desktop}"
                set name of result to "{shortcut_name}.app"
            end tell
            '''
            subprocess.run(['osascript', '-e', applescript], check=True)
            messagebox.showinfo("Success", "Desktop alias created successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to create macOS alias:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")

    def create_linux_shortcut(self, target_path, shortcut_name):
        try:
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            shortcut_path = os.path.join(desktop, f"{shortcut_name}.desktop")
            
            # Content of the .desktop file
            desktop_entry = f"""[Desktop Entry]
Type=Application
Name={shortcut_name}
Exec={sys.executable} "{target_path}"
Icon=utilities-terminal
Terminal=false
"""
            with open(shortcut_path, 'w') as f:
                f.write(desktop_entry)
            
            # Make the .desktop file executable
            os.chmod(shortcut_path, 0o755)
            messagebox.showinfo("Success", "Desktop shortcut created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create Linux shortcut:\n{str(e)}")

    def launch_main_py(self):
        """
        Launches the extracted main.py file.
        """
        main_py_path = os.path.join(self.parent.install_path.get(), "main.py")
        
        if not os.path.isfile(main_py_path):
            messagebox.showerror("Error", f"Cannot find 'main.py' in '{self.parent.install_path.get()}'.")
            return
        
        try:
            # Launch main.py using the same Python interpreter
            subprocess.Popen([sys.executable, main_py_path], cwd=self.parent.install_path.get())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch 'main.py':\n{str(e)}")
            return

if __name__ == "__main__":
    app = Installer()
    app.mainloop()

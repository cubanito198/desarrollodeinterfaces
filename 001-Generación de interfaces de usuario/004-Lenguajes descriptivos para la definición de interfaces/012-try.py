import tkinter as tk
from tkinter import filedialog
import subprocess

ventana = tk.Tk()

marco = tk.Frame(ventana)
marco.pack(padx=10,pady=10)

anchura = tk.StringVar()
altura = tk.StringVar()

salida = None
entrada = None

def procesar():
    print("Vamos a por ello")
    command = "ffmpeg -i '"+entrada+"' -vf scale="+anchura.get()+":"+altura.get()+" '"+salida+"'"
    print(command)
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print("FFmpeg output:", result.stdout)
        print("FFmpeg error (if any):", result.stderr)
        
        if result.returncode == 0:
            print("Video procesado con éxito")
        else:
            print("Error en el procesamiento del video")
    except Exception as e:
        print("Error ejecutando el comando:", e)
    
def seleccionaEntrada():
    global entrada
    entrada = filedialog.askopenfilename()
    

def seleccionaSalida():
    global salida
    salida = filedialog.asksaveasfilename()
    

selector_video_entrada = tk.Button(
    marco,
    text="Selecciona el video de entrada",
    command=seleccionaEntrada
    )

selector_video_entrada.pack(padx=50,pady=20);

tk.Label(
    marco,
    text="Indica la anchura de salida que quieres"
    ).pack(padx=50,pady=20);

tk.Entry(
    marco,
    textvariable=anchura).pack(padx=50,pady=20);

tk.Label(
    marco,
    text="Indica la altura de salida que quieres"
    ).pack(padx=50,pady=20);

tk.Entry(
    marco,
    textvariable=altura).pack(padx=50,pady=20);

selector_video_salida = tk.Button(
    marco,
    text="Selecciona el video de salida",
    command=seleccionaSalida
    )

selector_video_salida.pack(padx=50,pady=20);

tk.Button(marco,text="Comenzamos",command=procesar).pack(padx=50,pady=20);

ventana.mainloop()

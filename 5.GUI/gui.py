import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading
import re

# ---------- Funções ----------

def select_input_folder():
    folder = filedialog.askdirectory(title="Selecione a pasta de entrada")
    if folder:
        input_folder_var.set(folder)
        select_input_folder.selected_folder = folder

def select_output_folder():
    folder = filedialog.askdirectory(title="Selecione a pasta de saída")
    if folder:
        output_folder_var.set(folder)
        select_output_folder.selected_folder = folder

def log(message):
    log_text.configure(state='normal')
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    log_text.configure(state='disabled')

def run_segmentation_thread():
    thread = threading.Thread(target=segment)
    thread.start()

def segment():
    if not hasattr(select_input_folder, "selected_folder"):
        messagebox.showerror("Erro", "Selecione a pasta de entrada!")
        return

    if not hasattr(select_output_folder, "selected_folder"):
        messagebox.showerror("Erro", "Selecione a pasta de saída!")
        return

    input_folder = select_input_folder.selected_folder
    output_folder = select_output_folder.selected_folder

    dataset_id = dataset_var.get()
    config = config_var.get()
    trainer = trainer_var.get()
    checkpoint = checkpoint_var.get()
    fold = fold_var.get()
    device = device_var.get()

    cmd = [
        "nnUNetv2_predict",
        "-i", input_folder,
        "-o", output_folder,
        "-d", dataset_id,
        "-c", config,
        "-tr", trainer,
        "-chk", checkpoint,
        "-f", fold,
        "-device", device
    ]

    log(f"Executando comando: {' '.join(cmd)}")
    
    # Contar arquivos de entrada para a barra de progresso
    input_files = [f for f in os.listdir(input_folder) if f.endswith(".nii.gz")]
    progress["maximum"] = len(input_files)
    progress["value"] = 0

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            line = line.strip()
            log(line)

            # Atualiza barra de progresso quando detectar "predicting case X/Y"
            match = re.search(r'predicting case (\d+)/(\d+)', line.lower())
            if match:
                current = int(match.group(1))
                total = int(match.group(2))
                progress["maximum"] = total
                progress["value"] = current

        process.wait()

        if process.returncode == 0:
            log("Segmentação concluída!")
        else:
            log(f"Erro durante a segmentação. Código de saída: {process.returncode}")
            messagebox.showerror("Erro", f"Erro durante a segmentação. Código: {process.returncode}")
            return

    except Exception as e:
        log(f"Erro ao rodar nnUNetv2_predict: {e}")
        messagebox.showerror("Erro", f"Erro ao rodar nnUNetv2_predict:\n{e}")
        return

    # Abrir arquivos no ITK-SNAP (Windows)
    itk_snap_exe = r"C:\Program Files\ITK-SNAP 4.4\bin\ITK-SNAP.exe"
    for f in os.listdir(output_folder):
        if f.endswith(".nii.gz"):
            pred_file = os.path.join(output_folder, f)
            ref_file = os.path.join(input_folder, input_files[0])
            ref_win = f"\\\\wsl.localhost\\Ubuntu\\{ref_file.replace('/', '\\')}"
            pred_win = f"\\\\wsl.localhost\\Ubuntu\\{pred_file.replace('/', '\\')}"
            try:
                log(f"Abrindo {f} no ITK-SNAP...")
                subprocess.run(["cmd.exe", "/C", itk_snap_exe, "-g", ref_win, "-s", pred_win])
                log(f"{f} aberto no ITK-SNAP.")
            except Exception as e:
                log(f"Erro ao abrir ITK-SNAP: {e}")

# ---------- GUI ----------

root = tk.Tk()
root.title("GUI nnUNet -> ITK SNAP")
root.geometry("800x700")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Variáveis
input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()
dataset_var = tk.StringVar(value="Dataset001_MyBraTS")
config_var = tk.StringVar(value="3d_fullres")
trainer_var = tk.StringVar(value="nnUNetTrainer_200epochs")
checkpoint_var = tk.StringVar(value="checkpoint_best.pth")
fold_var = tk.StringVar(value="2")
device_var = tk.StringVar(value="cpu")

# Estilo
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))

main_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
main_frame.pack(fill="both", expand=True)

# Pastas
folder_frame = ttk.LabelFrame(main_frame, text="Pastas", padding=(10,10))
folder_frame.pack(fill="x", pady=5)
ttk.Label(folder_frame, text="Pasta de entrada:").grid(row=0, column=0, sticky="w")
ttk.Button(folder_frame, text="Selecionar", command=select_input_folder).grid(row=0, column=1, padx=5)
ttk.Label(folder_frame, textvariable=input_folder_var, foreground="blue").grid(row=1, column=0, columnspan=2, sticky="w", pady=2)
ttk.Label(folder_frame, text="Pasta de saída:").grid(row=2, column=0, sticky="w", pady=(5,0))
ttk.Button(folder_frame, text="Selecionar", command=select_output_folder).grid(row=2, column=1, padx=5, pady=(5,0))
ttk.Label(folder_frame, textvariable=output_folder_var, foreground="blue").grid(row=3, column=0, columnspan=2, sticky="w", pady=2)

# Parâmetros
param_frame = ttk.LabelFrame(main_frame, text="Parâmetros nnU-Net v2", padding=(10,10))
param_frame.pack(fill="x", pady=5)
labels = ["Dataset ID:", "Configuração:", "Trainer:", "Checkpoint:", "Fold:", "Device:"]
vars = [dataset_var, config_var, trainer_var, checkpoint_var, fold_var, device_var]
for i, (label_text, var) in enumerate(zip(labels, vars)):
    ttk.Label(param_frame, text=label_text).grid(row=i, column=0, sticky="e", pady=2)
    ttk.Entry(param_frame, textvariable=var, width=25).grid(row=i, column=1, sticky="w", pady=2, padx=5)

# Botão
seg_button = tk.Button(main_frame, text="Segmentar", command=run_segmentation_thread,
                       bg="#4caf50", fg="white", font=("Segoe UI", 12, "bold"), relief="raised")
seg_button.pack(pady=10, ipadx=10, ipady=5)

# Barra de progresso
progress = ttk.Progressbar(main_frame, orient="horizontal", length=700, mode="determinate")
progress.pack(pady=5)

# Log
log_frame = ttk.LabelFrame(main_frame, text="Log de execução", padding=(10,10))
log_frame.pack(fill="both", expand=True, pady=5)
log_text = tk.Text(log_frame, height=20, state='disabled', bg="#f9f9f9", fg="#333333", font=("Consolas", 10))
log_text.pack(fill="both", expand=True)

root.mainloop()

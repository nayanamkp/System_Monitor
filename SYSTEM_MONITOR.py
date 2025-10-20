import tkinter as tk
from tkinter import ttk
import psutil
import GPUtil

def get_system_info():
    cpu_percent = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    ram_used = ram.used / (1024 ** 3)
    ram_total = ram.total / (1024 ** 3)
    ram_percent = ram.percent
    return cpu_percent, ram_used, ram_total, ram_percent

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]
        vram_used = gpu.memoryUsed / 1024  # MB -> GB
        vram_total = gpu.memoryTotal / 1024  # MB -> GB
        gpu_percent = gpu.load * 100
        vram_percent = (vram_used / vram_total) * 100 if vram_total else 0
        return gpu_percent, vram_used, vram_total, vram_percent
    else:
        return 0, 0, 0, 0

def update_info():
    cpu_percent, ram_used, ram_total, ram_percent = get_system_info()
    gpu_percent, vram_used, vram_total, vram_percent = get_gpu_info()

    cpu_label.config(text=f"CPU: {cpu_percent:.1f}%")
    ram_label.config(text=f"RAM: {ram_used:.1f}GB / {ram_total:.1f}GB")
    cpu_bar['value'] = cpu_percent
    ram_bar['value'] = ram_percent

    gpu_label.config(text=f"GPU: {gpu_percent:.1f}%")
    vram_label.config(text=f"VRAM: {vram_used:.1f}GB / {vram_total:.1f}GB")
    gpu_bar['value'] = gpu_percent
    vram_bar['value'] = vram_percent

    root.after(1000, update_info)

def resize_widgets(event=None):
    w = root.winfo_width()
    h = root.winfo_height()

    # 기준(base) 해상도
    base_w, base_h = 480, 320

    # 현재 창에 대한 스케일 계산 (가로/세로 중 작은 쪽을 채택)
    scale_w = w / base_w
    scale_h = h / base_h    

    # 기본 폰트 사이즈 (base)
    base_big = 16
    base_mid = 12

    # 스케일 적용 (최소/최대 제한 없이 계산)
    font_big_size = int(base_big * scale_w)
    font_mid_size = int(base_mid * scale_h)

    font_big = ("맑은 고딕", font_big_size, "bold")
    font_mid = ("맑은 고딕", font_mid_size)

    style.configure("Big.TLabelframe.Label", font=font_big)
    cpu_label.config(font=font_mid)
    ram_label.config(font=font_mid)
    gpu_label.config(font=font_mid)
    vram_label.config(font=font_mid)

def set_theme(theme):
    if theme == "기본":
        style.theme_use('default')
        style.configure("Big.TLabelframe", background="#f0f0f0")
        style.configure("Big.TLabelframe.Label", background="#f0f0f0", foreground="black")
        style.configure("TLabel", background="#f0f0f0", foreground="black")
        style.configure("TProgressbar", background="green", troughcolor="#e0e0e0")
        root.configure(bg="#f0f0f0")
    elif theme == "블랙":
        style.theme_use('default')
        style.configure("Big.TLabelframe", background="#222222")
        style.configure("Big.TLabelframe.Label", background="#222222", foreground="white")
        style.configure("TLabel", background="#222222", foreground="white")
        style.configure("TProgressbar", background="lime", troughcolor="#444444")
        root.configure(bg="#222222")

def on_theme_change(event=None):
    set_theme(theme_var.get())

root = tk.Tk()
root.title("시스템 모니터")
root.geometry("480x320")
root.minsize(480, 320)
root.resizable(True, True)

style = ttk.Style()
style.configure("Big.TLabelframe.Label", font=("맑은 고딕", 14, "bold"))

# 테마 선택 체크버튼
theme_var = tk.StringVar(value="기본")
theme_check = ttk.Checkbutton(root, text="기본/블랙", variable=theme_var, onvalue="블랙", offvalue="기본", command=on_theme_change, style="TLabel")
theme_check.pack(anchor="ne", padx=8, pady=4)

set_theme(theme_var.get())

# System Frame
system_frame = ttk.LabelFrame(root, text="System", style="Big.TLabelframe")
system_frame.pack(fill="both", padx=8, pady=4)

cpu_label = ttk.Label(system_frame, text="CPU: ")
cpu_label.pack(anchor="w", padx=8, pady=1)
cpu_bar = ttk.Progressbar(system_frame, maximum=100)
cpu_bar.pack(fill="both", padx=8, pady=1)

ram_label = ttk.Label(system_frame, text="RAM: ")
ram_label.pack(anchor="w", padx=8, pady=1)
ram_bar = ttk.Progressbar(system_frame, maximum=100)
ram_bar.pack(fill="both", padx=8, pady=1)

# GPU Frame
gpu_frame = ttk.LabelFrame(root, text="GPU", style="Big.TLabelframe")
gpu_frame.pack(fill="both", padx=8, pady=4)

gpu_label = ttk.Label(gpu_frame, text="GPU: ")
gpu_label.pack(anchor="w", padx=8, pady=2)
gpu_bar = ttk.Progressbar(gpu_frame, maximum=100)
gpu_bar.pack(fill="both", padx=8, pady=2)

vram_label = ttk.Label(gpu_frame, text="VRAM: ")
vram_label.pack(anchor="w", padx=8, pady=2)
vram_bar = ttk.Progressbar(gpu_frame, maximum=100)
vram_bar.pack(fill="both", padx=8, pady=2)

root.bind("<Configure>", resize_widgets)

update_info()
root.mainloop()
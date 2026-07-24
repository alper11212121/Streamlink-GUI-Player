import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import os
import sys
import json
import shutil

# --- APPDATA CONFIGURATION (Single .exe Setup) ---
# Stores the JSON config inside Windows AppData directory.
APPDATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'StreamlinkPlayer')
os.makedirs(APPDATA_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(APPDATA_DIR, "favorites.json")

# Prevents popping up a CMD console window on Windows
CREATE_NO_WINDOW = 0x08000000

# Dynamically detect Streamlink and Python paths
def get_streamlink_cmd(url, quality):
    # 1. Default Installation Paths
    p_exec = r"C:\Program Files\Streamlink\Python\python.exe"
    l_script = r"C:\Program Files\Streamlink\Streamlink.launch.pyw"
    
    if os.path.exists(p_exec) and os.path.exists(l_script):
        return [p_exec, l_script, url, quality]
    
    # 2. Search Streamlink via System PATH
    streamlink_path = shutil.which("streamlink")
    if streamlink_path:
        return [streamlink_path, url, quality]
        
    return None

# Default 5 favorite slots
default_favorites = {f"Favorite {i+1}": "" for i in range(5)}

def load_favorites():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return default_favorites

def save_favorites(favs):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(favs, f, ensure_ascii=False, indent=4)

favorites = load_favorites()

def start_stream(url, quality="best"):
    if not url:
        messagebox.showwarning("Warning", "No URL set for this button!\nYou can add a link using the '⚙' edit button.")
        return
    
    cmd = get_streamlink_cmd(url, quality)
    if not cmd:
        messagebox.showerror("Error", "Streamlink was not found on this computer!\nPlease ensure Streamlink is installed.")
        return

    try:
        subprocess.Popen(cmd, creationflags=CREATE_NO_WINDOW)
        status_label.config(text=f"Launching stream ({quality})...", fg="#4caf50")
    except Exception as e:
        messagebox.showerror("Error", f"Could not launch stream:\n{e}")

def manual_start(event=None):
    url = url_entry.get().strip()
    quality = quality_cb.get().strip()
    start_stream(url, quality)

def edit_favorite(index_key):
    keys = list(favorites.keys())
    current_name = keys[index_key]
    current_url = favorites[current_name]
    
    new_name = simpledialog.askstring("Edit Button", f"Enter new label for Button {index_key+1}:", initialvalue=current_name)
    if new_name is None: return
    
    new_url = simpledialog.askstring("Edit Button", f"Enter stream URL for '{new_name}':", initialvalue=current_url)
    if new_url is None: return
    
    old_key = keys[index_key]
    if old_key != new_name:
        del favorites[old_key]
    
    favorites[new_name] = new_url.strip()
    save_favorites(favorites)
    update_buttons()

def update_buttons():
    for widget in fav_frame.winfo_children():
        widget.destroy()
        
    keys = list(favorites.keys())
    for i, name in enumerate(keys):
        url = favorites[name]
        
        btn = tk.Button(fav_frame, text=name if name else f"Empty {i+1}", 
                        font=("Segoe UI", 9, "bold"), bg="#333333", fg="#ffffff", 
                        activebackground="#444444", activeforeground="white", relief="flat",
                        command=lambda u=url: start_stream(u, quality_cb.get().strip()))
        btn.grid(row=0, column=i, padx=3, sticky="ew")
        
        edit_btn = tk.Button(fav_frame, text="⚙", font=("Segoe UI", 8), bg="#2d2d2d", fg="#aaaaaa",
                             activebackground="#444444", activeforeground="white", relief="flat",
                             command=lambda idx=i: edit_favorite(idx))
        edit_btn.grid(row=1, column=i, padx=3, pady=2, sticky="ew")
        
        fav_frame.grid_columnconfigure(i, weight=1)

# --- GUI LAYOUT ---
root = tk.Tk()
root.title("Streamlink GUI Player - Pro")
root.geometry("500x310")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

title_label = tk.Label(root, text="Streamlink GUI Player", font=("Segoe UI", 14, "bold"), bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=8)

url_frame = tk.Frame(root, bg="#1e1e1e")
url_frame.pack(fill="x", padx=20, pady=5)

tk.Label(url_frame, text="Stream URL:", font=("Segoe UI", 9), bg="#1e1e1e", fg="#cccccc").pack(anchor="w")
url_entry = tk.Entry(url_frame, font=("Segoe UI", 10), width=50, bg="#2d2d2d", fg="#ffffff", insertbackground="white", relief="flat")
url_entry.pack(fill="x", pady=2, ipady=3)
url_entry.focus()

control_frame = tk.Frame(root, bg="#1e1e1e")
control_frame.pack(fill="x", padx=20, pady=5)

tk.Label(control_frame, text="Quality:", font=("Segoe UI", 9), bg="#1e1e1e", fg="#cccccc").pack(side="left")

style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground="#2d2d2d", background="#2d2d2d", foreground="#ffffff", selectbackground="#007acc", selectforeground="#ffffff")

quality_cb = ttk.Combobox(control_frame, values=["best", "1080p60", "720p60", "480p", "worst"], state="readonly", width=10)
quality_cb.set("best")
quality_cb.pack(side="left", padx=10)

btn_start = tk.Button(control_frame, text="Start Stream (Enter)", font=("Segoe UI", 9, "bold"), bg="#007acc", fg="white", activebackground="#005999", activeforeground="white", relief="flat", padx=10, pady=2, command=manual_start)
btn_start.pack(side="right")

separator = tk.Label(root, text="--- Quick Access Favorites (Click ⚙ to configure) ---", font=("Segoe UI", 8), bg="#1e1e1e", fg="#777777")
separator.pack(pady=(8, 2))

fav_frame = tk.Frame(root, bg="#1e1e1e")
fav_frame.pack(fill="x", padx=15, pady=2)

update_buttons()

status_label = tk.Label(root, text="", font=("Segoe UI", 8, "italic"), bg="#1e1e1e", fg="#888888")
status_label.pack(pady=5)

root.bind('<Return>', manual_start)
root.mainloop()
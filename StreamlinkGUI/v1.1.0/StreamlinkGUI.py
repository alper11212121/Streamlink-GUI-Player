import customtkinter as ctk
from tkinter import messagebox, simpledialog
import subprocess
import os
import sys
import json
import shutil

# --- APPEARANCE & THEME SETTINGS ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- APPDATA CONFIGURATION (Persistent Path) ---
# Data persists in Windows AppData even when the .exe is updated.
APPDATA_PATH = os.environ.get('APPDATA') or os.path.expanduser('~')
APPDATA_DIR = os.path.join(APPDATA_PATH, 'StreamlinkPlayer')

try:
    os.makedirs(APPDATA_DIR, exist_ok=True)
except Exception as e:
    print(f"Directory creation error: {e}")

CONFIG_FILE = os.path.join(APPDATA_DIR, "favorites.json")
CREATE_NO_WINDOW = 0x08000000

def get_streamlink_cmd(url, quality):
    p_exec = r"C:\Program Files\Streamlink\Python\python.exe"
    l_script = r"C:\Program Files\Streamlink\Streamlink.launch.pyw"
    
    if os.path.exists(p_exec) and os.path.exists(l_script):
        return [p_exec, l_script, url, quality]
    
    streamlink_path = shutil.which("streamlink")
    if streamlink_path:
        return [streamlink_path, url, quality]
        
    return None

def load_favorites():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and data:
                    return data
        except Exception as e:
            print(f"Could not load favorites: {e}")
            
    default_data = {"Sample Channel 1": "https://twitch.tv/example1"}
    save_favorites(default_data)
    return default_data

def save_favorites(favs):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(favs, f, ensure_ascii=False, indent=4)
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save favorites:\n{e}")

favorites = load_favorites()

def start_stream(url, quality="best"):
    if not url:
        messagebox.showwarning("Warning", "Please enter or select a valid stream URL!")
        return
    
    cmd = get_streamlink_cmd(url, quality)
    if not cmd:
        messagebox.showerror("Error", "Streamlink was not found on this system!\nPlease make sure it is installed.")
        return

    try:
        subprocess.Popen(cmd, creationflags=CREATE_NO_WINDOW)
        status_label.configure(text=f"Launching stream ({quality})...", text_color="#4caf50")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch stream:\n{e}")

def manual_start(event=None):
    url = url_entry.get().strip()
    quality = quality_cb.get().strip()
    start_stream(url, quality)

# --- SEPARATE FAVORITES WINDOW ---
fav_window = None

def open_favorites_window():
    global fav_window
    
    if fav_window is not None and fav_window.winfo_exists():
        fav_window.focus()
        return

    fav_window = ctk.CTkToplevel(root)
    fav_window.title("Favorite Channels")
    fav_window.geometry("420x220")
    fav_window.resizable(False, False)
    fav_window.attributes('-topmost', True)

    title_fav = ctk.CTkLabel(fav_window, text="⭐ Favorite Channels", font=ctk.CTkFont(size=16, weight="bold"))
    title_fav.pack(pady=(15, 10))

    fav_cb = ctk.CTkComboBox(fav_window, width=280, height=35, font=ctk.CTkFont(size=13))
    fav_cb.pack(pady=10)

    def update_fav_cb(select_name=None):
        names = list(favorites.keys())
        if names:
            fav_cb.configure(values=names)
            if select_name and select_name in names:
                fav_cb.set(select_name)
            else:
                fav_cb.set(names[0])
        else:
            fav_cb.configure(values=["No favorites yet"])
            fav_cb.set("No favorites yet")

    def play_fav():
        selected_name = fav_cb.get()
        if selected_name in favorites:
            url = favorites[selected_name]
            quality = quality_cb.get().strip()
            fav_window.destroy()
            start_stream(url, quality)
        else:
            messagebox.showwarning("Warning", "Please select a valid favorite!", parent=fav_window)

    def add_fav():
        name = simpledialog.askstring("New Favorite", "Channel/Stream Name:", parent=fav_window)
        if not name or not name.strip(): return
        
        url = simpledialog.askstring("New Favorite", f"Stream URL for '{name.strip()}':", parent=fav_window)
        if not url or not url.strip(): return
        
        favorites[name.strip()] = url.strip()
        save_favorites(favorites)
        update_fav_cb(select_name=name.strip())

    def edit_fav():
        selected_name = fav_cb.get()
        if not selected_name or selected_name not in favorites:
            messagebox.showwarning("Warning", "Please select a favorite to edit!", parent=fav_window)
            return
            
        current_url = favorites[selected_name]
        new_name = simpledialog.askstring("Edit Favorite", "New Channel Name:", initialvalue=selected_name, parent=fav_window)
        if not new_name or not new_name.strip(): return
        
        new_url = simpledialog.askstring("Edit Favorite", "New Stream URL:", initialvalue=current_url, parent=fav_window)
        if not new_url or not new_url.strip(): return
        
        if new_name.strip() != selected_name:
            del favorites[selected_name]
            
        favorites[new_name.strip()] = new_url.strip()
        save_favorites(favorites)
        update_fav_cb(select_name=new_name.strip())

    def delete_fav():
        selected_name = fav_cb.get()
        if not selected_name or selected_name not in favorites:
            messagebox.showwarning("Warning", "Please select a favorite to delete!", parent=fav_window)
            return
            
        confirm = messagebox.askyesno("Delete Favorite", f"Remove '{selected_name}' from favorites?", parent=fav_window)
        if confirm:
            del favorites[selected_name]
            save_favorites(favorites)
            update_fav_cb()

    btn_frame = ctk.CTkFrame(fav_window, fg_color="transparent")
    btn_frame.pack(pady=15)

    btn_play = ctk.CTkButton(btn_frame, text="▶ Play", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#2e7d32", hover_color="#1b5e20", width=80, height=32, command=play_fav)
    btn_play.pack(side="left", padx=3)

    btn_add = ctk.CTkButton(btn_frame, text="Add", font=ctk.CTkFont(size=12), fg_color="#333333", hover_color="#444444", width=60, height=32, command=add_fav)
    btn_add.pack(side="left", padx=3)

    btn_edit = ctk.CTkButton(btn_frame, text="Edit", font=ctk.CTkFont(size=12), fg_color="#333333", hover_color="#444444", width=70, height=32, command=edit_fav)
    btn_edit.pack(side="left", padx=3)

    btn_del = ctk.CTkButton(btn_frame, text="Delete", font=ctk.CTkFont(size=12), fg_color="#c62828", hover_color="#8e0000", width=60, height=32, command=delete_fav)
    btn_del.pack(side="left", padx=3)

    update_fav_cb()

def on_closing():
    save_favorites(favorites)
    root.destroy()

# --- MAIN WINDOW ---
root = ctk.CTk()
root.title("Streamlink GUI Player")
root.geometry("480x210")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_closing)

# Title
title_label = ctk.CTkLabel(root, text="Streamlink GUI Player", font=ctk.CTkFont(size=18, weight="bold"))
title_label.pack(pady=(15, 10))

# URL Input Area
url_frame = ctk.CTkFrame(root, fg_color="transparent")
url_frame.pack(fill="x", padx=20, pady=2)

ctk.CTkLabel(url_frame, text="Manual Stream URL:", font=ctk.CTkFont(size=12), text_color="#aaaaaa").pack(anchor="w")
url_entry = ctk.CTkEntry(url_frame, font=ctk.CTkFont(size=13), placeholder_text="https://...", height=35)
url_entry.pack(fill="x", pady=(3, 0))

# Control Area
control_frame = ctk.CTkFrame(root, fg_color="transparent")
control_frame.pack(fill="x", padx=20, pady=15)

ctk.CTkLabel(control_frame, text="Quality:", font=ctk.CTkFont(size=12), text_color="#aaaaaa").pack(side="left")

quality_cb = ctk.CTkComboBox(control_frame, values=["best", "1080p60", "720p60", "480p", "worst"], width=100, height=32)
quality_cb.set("best")
quality_cb.pack(side="left", padx=(5, 10))

btn_fav_popup = ctk.CTkButton(control_frame, text="⭐ Favorites", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#333333", hover_color="#444444", height=32, command=open_favorites_window)
btn_fav_popup.pack(side="left")

btn_start = ctk.CTkButton(control_frame, text="Play (Enter)", font=ctk.CTkFont(size=13, weight="bold"), height=32, command=manual_start)
btn_start.pack(side="right")

status_label = ctk.CTkLabel(root, text="", font=ctk.CTkFont(size=11, slant="italic"), text_color="#888888")
status_label.pack(pady=2)

root.bind('<Return>', manual_start)
root.mainloop()
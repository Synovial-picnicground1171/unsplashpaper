import json
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from pathlib import Path

CATEGORIES = [
    "nature", "architecture", "travel", "animals", "food",
    "space", "abstract", "minimalism", "city", "ocean",
    "mountains", "forest", "technology", "art", "flowers",
]
RESOLUTIONS = ["1920x1080", "2560x1440", "3840x2160", "1366x768"]
INTERVALS = [
    ("Every hour", 1),
    ("Every 6 hours", 6),
    ("Every 12 hours", 12),
    ("Every day", 24),
    ("Every 2 days", 48),
]


def _center_window(win, w, h):
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")


class SettingsForm:
    def __init__(self, root, config_path, on_save=None, is_wizard=False):
        self.root = root
        self.config_path = Path(config_path)
        self.on_save = on_save
        self.saved = False

        config = {}
        if self.config_path.exists():
            with open(self.config_path, encoding="utf-8") as f:
                config = json.load(f)

        title = "UnsplashPaper — Setup" if is_wizard else "UnsplashPaper — Settings"
        root.title(title)
        root.resizable(False, False)
        _center_window(root, 460, 380)

        root.configure(bg="#f5f5f5")

        main = ttk.Frame(root, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="UnsplashPaper", font=("Segoe UI", 16, "bold")).pack(pady=(0, 5))
        ttk.Label(main, text="Wallpaper that changes automatically", font=("Segoe UI", 9)).pack(pady=(0, 15))

        form = ttk.Frame(main)
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)

        row = 0
        ttk.Label(form, text="API Key:").grid(row=row, column=0, sticky="w", pady=6)
        key_frame = ttk.Frame(form)
        key_frame.grid(row=row, column=1, sticky="ew", pady=6)
        key_frame.columnconfigure(0, weight=1)

        self.key_var = tk.StringVar(value=config.get("unsplash_access_key", ""))
        self.key_entry = ttk.Entry(key_frame, textvariable=self.key_var, show="*")
        self.key_entry.grid(row=0, column=0, sticky="ew")

        self.show_key = tk.BooleanVar(value=False)
        ttk.Checkbutton(key_frame, text="Show", variable=self.show_key,
                         command=self._toggle_key_visibility).grid(row=0, column=1, padx=(5, 0))

        row += 1
        link = ttk.Label(form, text="Get a free API key →", foreground="#0066cc",
                          cursor="hand2", font=("Segoe UI", 8, "underline"))
        link.grid(row=row, column=1, sticky="w", pady=(0, 8))
        link.bind("<Button-1>", lambda e: webbrowser.open("https://teyk0o.github.io/unsplashpaper/#api-guide"))

        row += 1
        ttk.Label(form, text="Category:").grid(row=row, column=0, sticky="w", pady=6)
        self.cat_var = tk.StringVar(value=config.get("category", "nature"))
        cat_combo = ttk.Combobox(form, textvariable=self.cat_var, values=CATEGORIES)
        cat_combo.grid(row=row, column=1, sticky="ew", pady=6)

        row += 1
        ttk.Label(form, text="Resolution:").grid(row=row, column=0, sticky="w", pady=6)
        self.res_var = tk.StringVar(value=config.get("resolution", "1920x1080"))
        ttk.Combobox(form, textvariable=self.res_var, values=RESOLUTIONS,
                      state="readonly").grid(row=row, column=1, sticky="ew", pady=6)

        row += 1
        ttk.Label(form, text="Interval:").grid(row=row, column=0, sticky="w", pady=6)
        current_hours = config.get("interval_hours", 24)
        interval_labels = [label for label, _ in INTERVALS]
        current_label = next((l for l, h in INTERVALS if h == current_hours), "Every day")
        self.interval_var = tk.StringVar(value=current_label)
        ttk.Combobox(form, textvariable=self.interval_var, values=interval_labels,
                      state="readonly").grid(row=row, column=1, sticky="ew", pady=6)

        btn_frame = ttk.Frame(main)
        btn_frame.pack(pady=(20, 0))
        ttk.Button(btn_frame, text="Save", command=self._save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self._cancel).pack(side="left", padx=5)

        root.protocol("WM_DELETE_WINDOW", self._cancel)

    def _toggle_key_visibility(self):
        self.key_entry.config(show="" if self.show_key.get() else "*")

    def _save(self):
        key = self.key_var.get().strip()
        if len(key) < 10 or " " in key:
            messagebox.showerror("Invalid API Key",
                                  "Please enter a valid Unsplash API key.\n\n"
                                  "Get one for free at unsplash.com/developers")
            return

        interval_hours = next((h for l, h in INTERVALS if l == self.interval_var.get()), 24)

        config = {
            "unsplash_access_key": key,
            "category": self.cat_var.get().strip().lower() or "nature",
            "resolution": self.res_var.get(),
            "interval_hours": interval_hours,
        }

        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        self.saved = True
        if self.on_save:
            self.on_save()
        self.root.destroy()

    def _cancel(self):
        self.root.destroy()


def run_wizard(config_path):
    root = tk.Tk()
    form = SettingsForm(root, config_path, is_wizard=True)
    root.mainloop()
    return form.saved


def open_settings(config_path, on_save_callback=None):
    import threading

    def _run():
        root = tk.Tk()
        SettingsForm(root, config_path, on_save=on_save_callback)
        root.mainloop()

    threading.Thread(target=_run, daemon=True).start()


if __name__ == "__main__":
    run_wizard("config.json")

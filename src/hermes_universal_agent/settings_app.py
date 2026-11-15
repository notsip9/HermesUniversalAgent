"""Small local Tk settings UI. All sensitive desktop permissions default off."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .config import DEFAULT_PERMISSIONS, load_config, save_config

LABELS = {
    "file_writes": "Allow workspace file writes",
    "screen_capture": "Allow screen capture",
    "window_control": "Allow focusing application windows",
    "mouse_input": "Allow mouse clicks",
    "keyboard_input": "Allow keyboard typing and approved shortcuts",
}

def main() -> None:
    config = load_config()
    root = tk.Tk()
    root.title("Hermes Universal Agent Settings")
    root.geometry("600x510")
    root.minsize(540, 460)

    frame = ttk.Frame(root, padding=18)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Hermes Universal Agent", font=("Segoe UI", 17, "bold")).pack(anchor="w")
    ttk.Label(
        frame,
        text="Local settings. Desktop permissions are off until you enable them here.",
        wraplength=540,
    ).pack(anchor="w", pady=(4, 16))

    ttk.Label(frame, text="Workspace folder").pack(anchor="w")
    path_var = tk.StringVar(value=config["workspace"])
    path_row = ttk.Frame(frame)
    path_row.pack(fill="x", pady=(4, 14))
    ttk.Entry(path_row, textvariable=path_var).pack(side="left", fill="x", expand=True)
    def browse() -> None:
        selected = filedialog.askdirectory(initialdir=path_var.get() or None)
        if selected:
            path_var.set(selected)
    ttk.Button(path_row, text="Browse…", command=browse).pack(side="left", padx=(8, 0))

    ttk.Label(frame, text="Local permissions", font=("Segoe UI", 11, "bold")).pack(anchor="w")
    vars_by_key = {}
    for key in DEFAULT_PERMISSIONS:
        var = tk.BooleanVar(value=config["permissions"].get(key, False))
        vars_by_key[key] = var
        ttk.Checkbutton(frame, text=LABELS[key], variable=var).pack(anchor="w", pady=3)

    ttk.Label(
        frame,
        text=("Every write or desktop action also requires confirm=true in that individual MCP call. "
              "No arbitrary shell execution is provided. Screen images and keystrokes may contain "
              "private information; enable only what you need."),
        wraplength=540,
    ).pack(anchor="w", pady=(16, 12))

    def save() -> None:
        if not path_var.get().strip():
            messagebox.showerror("Invalid workspace", "Choose a workspace folder.")
            return
        config["workspace"] = path_var.get().strip()
        config["permissions"] = {key: var.get() for key, var in vars_by_key.items()}
        save_config(config)
        messagebox.showinfo("Saved", "Hermes settings were saved locally.")
    buttons = ttk.Frame(frame)
    buttons.pack(fill="x", side="bottom")
    ttk.Button(buttons, text="Save settings", command=save).pack(side="right")
    ttk.Button(buttons, text="Close", command=root.destroy).pack(side="right", padx=8)
    root.mainloop()

if __name__ == "__main__":
    main()

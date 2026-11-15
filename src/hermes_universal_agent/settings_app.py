from pathlib import Path
import tkinter as tk
from tkinter import filedialog,messagebox
from .config import Settings,load_settings,save_settings

def main() -> None:
    root=tk.Tk(); root.title("Hermes Universal Agent Settings"); root.geometry("620x390"); root.minsize(560,350)
    current=load_settings()
    workspace=tk.StringVar(value=current.workspace_root)
    writes=tk.BooleanVar(value=current.allow_file_writes)
    desktop=tk.BooleanVar(value=current.allow_desktop_control)
    capture=tk.BooleanVar(value=current.allow_screen_capture)
    frame=tk.Frame(root,padx=20,pady=18); frame.pack(fill="both",expand=True)
    tk.Label(frame,text="Hermes Universal Agent",font=("Segoe UI",16,"bold")).pack(anchor="w")
    tk.Label(frame,text="Local permissions are off by default. Enable only what you intend to use.",
             wraplength=560,justify="left").pack(anchor="w",pady=(5,18))
    tk.Label(frame,text="Workspace folder").pack(anchor="w")
    row=tk.Frame(frame); row.pack(fill="x",pady=(4,14))
    tk.Entry(row,textvariable=workspace).pack(side="left",fill="x",expand=True)
    def browse():
        selected=filedialog.askdirectory(initialdir=workspace.get() or str(Path.home()))
        if selected: workspace.set(selected)
    tk.Button(row,text="Browse…",command=browse).pack(side="left",padx=(8,0))
    tk.Checkbutton(frame,text="Allow workspace file writes (each write also requires confirm=true)",variable=writes).pack(anchor="w",pady=3)
    tk.Checkbutton(frame,text="Allow desktop interaction (window listing, focus, mouse, typing)",variable=desktop).pack(anchor="w",pady=3)
    tk.Checkbutton(frame,text="Allow screen capture (separate permission; each capture requires confirmation)",variable=capture).pack(anchor="w",pady=3)
    tk.Label(frame,text="Every desktop action and screen capture must also be explicitly confirmed by the MCP client.",
             wraplength=560,justify="left",fg="#555").pack(anchor="w",pady=(12,16))
    def save():
        folder=Path(workspace.get()).expanduser()
        if not folder.exists() or not folder.is_dir():
            messagebox.showerror("Invalid workspace","Choose an existing folder."); return
        try: location=save_settings(Settings(str(folder.resolve()),writes.get(),desktop.get(),capture.get()))
        except OSError as exc: messagebox.showerror("Could not save settings",str(exc)); return
        messagebox.showinfo("Settings saved",f"Saved locally to:\n{location}")
    tk.Button(frame,text="Save settings",command=save,width=18).pack(anchor="e")
    root.mainloop()
if __name__=="__main__": main()

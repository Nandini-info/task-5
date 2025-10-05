#!/usr/bin/env python3
"""
Safe educational keystroke logger (consented + focused only).
Logs keys pressed while this Tkinter window is focused and "Start logging" is active.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import os

LOG_FILENAME = "keystrokes_log.txt"

class ConsentKeyLogger:
    def __init__(self, root):
        self.root = root
        self.root.title("Consented Keystroke Logger (Educational Demo)")
        self.root.geometry("650x400")

        # Consent checkbox
        self.consent_var = tk.BooleanVar(value=False)
        consent_frame = tk.Frame(self.root)
        consent_frame.pack(fill="x", padx=8, pady=(8,0))
        tk.Checkbutton(consent_frame, text="I understand and CONSENT to logging my keystrokes in this window",
                       variable=self.consent_var).pack(side="left", anchor="w")

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=8, pady=6)
        self.start_btn = tk.Button(btn_frame, text="Start logging", command=self.start_logging)
        self.start_btn.pack(side="left")
        self.stop_btn = tk.Button(btn_frame, text="Stop logging", command=self.stop_logging, state="disabled")
        self.stop_btn.pack(side="left", padx=(6,0))
        tk.Button(btn_frame, text="Clear display", command=self.clear_display).pack(side="left", padx=(6,0))

        # Info label
        self.info_label = tk.Label(self.root, text="Logging is OFF. The app must have focus for keys to be recorded.")
        self.info_label.pack(fill="x", padx=8, pady=(0,8))

        # Scrolled text to show logged keys
        self.text_area = scrolledtext.ScrolledText(self.root, wrap="word", height=15, state="disabled")
        self.text_area.pack(fill="both", expand=True, padx=8, pady=(0,8))

        # Ensure the window gets keyboard focus when clicked
        self.root.bind("<Button-1>", lambda e: self.root.focus_set())

        # Internal state
        self.logging = False

    def start_logging(self):
        if not self.consent_var.get():
            messagebox.showwarning("Consent required", "You must check the consent box before starting logging.")
            return
        if self.logging:
            return
        # Bind <Key> on the root — captures keys when the window has focus.
        self.root.bind("<Key>", self.on_key)
        self.logging = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.info_label.config(text="Logging is ON. App must be focused to capture keys. Consent recorded.")

        # Make sure file exists
        if not os.path.exists(LOG_FILENAME):
            with open(LOG_FILENAME, "w", encoding="utf-8") as f:
                f.write(f"Keystroke log started: {datetime.now().isoformat()}\n")

    def stop_logging(self):
        if not self.logging:
            return
        self.root.unbind("<Key>")
        self.logging = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.info_label.config(text="Logging is OFF.")

    def clear_display(self):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state="disabled")

    def on_key(self, event):
        """
        event.char is the printed character (may be empty for special keys),
        event.keysym is the symbolic name (e.g., 'Return', 'BackSpace', 'a').
        """
        # Build readable key representation
        char = event.char
        keysym = event.keysym

        if char and char.isprintable():
            key_repr = char
        else:
            # For non-printable: use the keysym wrapped
            key_repr = f"<{keysym}>"

        timestamp = datetime.now().isoformat(timespec="seconds")
        line = f"{timestamp}\t{key_repr}\n"

        # Append to file
        try:
            with open(LOG_FILENAME, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception as e:
            # If file write fails, inform user and stop logging for safety
            messagebox.showerror("Write error", f"Failed to write to log file: {e}")
            self.stop_logging()
            return

        # Show in GUI
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, line)
        # Auto-scroll
        self.text_area.see(tk.END)
        self.text_area.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConsentKeyLogger(root)
    root.mainloop()
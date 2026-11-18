"""
Remote Command Center - Tkinter client (Week 16).

Calls the Django JsonResponse endpoint with `requests` and shows the data in a window.
Start the Django server first:   python manage.py runserver
Then run this file:              python tkinter_client/client.py
"""
import os
import tkinter as tk
from tkinter import ttk

import requests

# Must match the address printed by `python manage.py runserver`.
# Override without editing code:  set COMMAND_CENTER_URL=http://127.0.0.1:8001/api/status/
API_URL = os.environ.get("COMMAND_CENTER_URL", "http://127.0.0.1:8000/api/status/")
REQUEST_TIMEOUT = 5          # seconds; never wait forever on a dead server
AUTO_REFRESH_MS = 10_000     # auto-refresh every 10 seconds

# Same dark purple palette as the web projects
BG, CARD, BORDER = "#120a1f", "#21153a", "#3a2766"
PRIMARY, ACCENT = "#7c3aed", "#c4b5fd"
TEXT, MUTED = "#f3effc", "#b3a7d1"
GOOD, BAD = "#34d399", "#fb7185"
FONT = "Segoe UI"


def fetch_status(url=API_URL):
    """Call the endpoint and return (data, error_message). Exactly one of them is None.

    Kept separate from the GUI so it is easy to test and the window never crashes.
    """
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        return None, "Server unreachable. Is `python manage.py runserver` running?"
    except requests.exceptions.Timeout:
        return None, "The server took too long to respond."
    except requests.exceptions.RequestException as exc:
        return None, f"Request failed: {exc}"

    # Only trust the body after confirming the request succeeded.
    if response.status_code != 200:
        return None, f"Server returned HTTP {response.status_code}."

    try:
        return response.json(), None
    except ValueError:
        return None, "The server did not return valid JSON."


class CommandCenter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Remote Command Center")
        self.geometry("560x560")
        self.minsize(520, 520)
        self.configure(bg=BG)
        self._build_style()
        self._build_widgets()
        self.refresh()

    # ---------- styling ----------
    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=TEXT,
                        bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
                        rowheight=30, font=(FONT, 10))
        style.configure("Treeview.Heading", background=BG, foreground=ACCENT,
                        font=(FONT, 9, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", PRIMARY)])

    def _card(self, parent):
        return tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)

    def _stat(self, parent, caption):
        card = self._card(parent)
        tk.Label(card, text=caption.upper(), bg=CARD, fg=MUTED, font=(FONT, 8, "bold")).pack(
            anchor="w", padx=14, pady=(12, 0))
        value = tk.Label(card, text="--", bg=CARD, fg=TEXT, font=(FONT, 20, "bold"), justify="left")
        value.pack(anchor="w", padx=14, pady=(0, 12))
        return card, value

    # ---------- layout ----------
    def _build_widgets(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=24, pady=(22, 6))
        tk.Label(header, text="H", bg=PRIMARY, fg="white", width=2,
                 font=(FONT, 14, "bold")).pack(side="left")
        tk.Label(header, text="  Remote Command Center", bg=BG, fg=TEXT,
                 font=(FONT, 16, "bold")).pack(side="left")

        status_row = tk.Frame(self, bg=BG)
        status_row.pack(fill="x", padx=24, pady=(4, 12))
        self.dot = tk.Label(status_row, text="●", bg=BG, fg=MUTED, font=(FONT, 12))
        self.dot.pack(side="left")
        self.status_label = tk.Label(status_row, text="Connecting...", bg=BG, fg=MUTED,
                                     font=(FONT, 11), anchor="w", justify="left", wraplength=470)
        self.status_label.pack(side="left", padx=6)

        stats = tk.Frame(self, bg=BG)
        stats.pack(fill="x", padx=24)
        for col in range(3):
            stats.columnconfigure(col, weight=1, uniform="stat")
        c1, self.employee_value = self._stat(stats, "Employees")
        c2, self.online_value = self._stat(stats, "Online now")
        c3, self.time_value = self._stat(stats, "Server time")
        self.time_value.config(font=(FONT, 11, "bold"))
        for i, card in enumerate((c1, c2, c3)):
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 0))

        tk.Label(self, text="Departments", bg=BG, fg=TEXT, font=(FONT, 12, "bold")).pack(
            anchor="w", padx=24, pady=(20, 6))
        table_frame = self._card(self)
        table_frame.pack(fill="both", expand=True, padx=24)
        self.table = ttk.Treeview(table_frame, columns=("name", "staff", "online"),
                                  show="headings", height=4)
        for col, title, width, anchor in (("name", "Department", 220, "w"),
                                          ("staff", "Staff", 90, "center"),
                                          ("online", "Online", 90, "center")):
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor=anchor)
        self.table.pack(fill="both", expand=True, padx=2, pady=2)

        footer = tk.Frame(self, bg=BG)
        footer.pack(fill="x", padx=24, pady=16)
        self.refresh_button = tk.Button(
            footer, text="Refresh", command=self.refresh, bg=PRIMARY, fg="white",
            activebackground="#8b5cf6", activeforeground="white", relief="flat", bd=0,
            padx=20, pady=8, font=(FONT, 10, "bold"), cursor="hand2")
        self.refresh_button.pack(side="left")
        self.url_label = tk.Label(footer, text=API_URL, bg=BG, fg=MUTED, font=(FONT, 8))
        self.url_label.pack(side="right")

    # ---------- behaviour ----------
    def refresh(self):
        data, error = fetch_status()
        if error:
            self.show_error(error)
        else:
            self.show_data(data)
        # Schedule the next automatic refresh (replaces any pending one).
        if getattr(self, "_after_id", None):
            self.after_cancel(self._after_id)
        self._after_id = self.after(AUTO_REFRESH_MS, self.refresh)

    def show_data(self, data):
        try:
            self.dot.config(fg=GOOD)
            self.status_label.config(text=f"Server status: {data['status'].upper()}", fg=GOOD)
            self.employee_value.config(text=str(data["employee_count"]))
            self.online_value.config(text=str(data["online_now"]))
            self.time_value.config(text=data["server_time"].replace(" ", "\n"))
            self.table.delete(*self.table.get_children())
            for dept in data["departments"]:
                self.table.insert("", "end", values=(dept["name"], dept["staff"], dept["online"]))
        except (KeyError, TypeError):
            self.show_error("The server's reply is missing expected fields.")

    def show_error(self, message):
        self.dot.config(fg=BAD)
        self.status_label.config(text=message, fg=BAD)
        for label in (self.employee_value, self.online_value, self.time_value):
            label.config(text="--")
        self.table.delete(*self.table.get_children())


if __name__ == "__main__":
    CommandCenter().mainloop()

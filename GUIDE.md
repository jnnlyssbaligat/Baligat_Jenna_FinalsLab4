# Step-by-Step Guide: Remote Command Center (Week 16)

A **separate project** from Weeks 13–15. A headless Django view returns JSON, and a Tkinter window
fetches it with `requests` and displays it. Tests: 5 for the Django endpoint, 5 for the client's
network logic. I also ran the real window against the real server, with the server up and down.

---

## Part 1 — Set up the project folder

```
command_center_project/
├── manage.py
├── requirements.txt
├── README.md  GUIDE.md  JSON_PAYLOAD_DESIGN_NOTE.md  .gitignore
├── config/            settings.py, urls.py, wsgi.py
├── center/            views.py  ← JsonResponse endpoint,  urls.py  ← route,  tests.py
└── tkinter_client/    client.py  ← the Tkinter interface,  test_client.py
```

1. Make a **new** folder (e.g. `Baligat_Jenna_FinalsLab4`) and put the extracted project in it.
2. Open a terminal in the folder that contains `manage.py` (run `dir` to check).
3. Install the packages with `python -m pip` (your PC blocks `pip.exe`):
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```
   This installs Django **and `requests`** (Step 3 of the sheet). Tkinter comes with the python.org
   installer, so it needs no install. Check with `python -m tkinter`, which should open a small test window.
4. No database setup is needed because the endpoint doesn't use models.

---

## Part 2 — Run it (you need TWO terminals)

**Terminal 1 — the Django server (leave it running):**
```powershell
python manage.py runserver
```
Note the address it prints, normally `http://127.0.0.1:8000/`.

**Step 2 of the sheet — test the endpoint in the browser first:** open
http://127.0.0.1:8000/api/status/. You should see raw JSON text, like:
```json
{"status": "ok", "server_time": "...", "employee_count": 29, "online_now": 22, "departments": [...]}
```

**Terminal 2 — the Tkinter app** (open a new terminal, activate the venv again):
```powershell
python tkinter_client\client.py
```
The window shows the status, the totals, the server time and a department table. It refreshes every
10 seconds, and the **Refresh** button updates it immediately.

**If your server uses another port** (e.g. 8001), either edit `API_URL` at the top of `client.py`, or:
```powershell
$env:COMMAND_CENTER_URL = "http://127.0.0.1:8001/api/status/"
python tkinter_client\client.py
```

**Test the failure case (Step 7):** stop the Django server with Ctrl + C and click **Refresh**. The window
should turn red with "Server unreachable..." and **not crash**. Start the server again and click Refresh to recover.

> **Personalize it:** change the department names and numbers in `center/views.py`, the field names, the
> window title and the colours in `client.py`. If you rename the keys, update them in `client.py` too (the
> `show_data` method) and in `center/tests.py`.

---

## Part 3 — Map the task steps to the code

| Step in the sheet | Where it lives |
|---|---|
| 1. Headless view returning `JsonResponse`, routed in `urls.py` | `center/views.py` → `status()`, `center/urls.py` → `api/status/` |
| 2. Test in browser first | Part 2 above |
| 3. Install and import `requests` | `requirements.txt`, `import requests` in `client.py` |
| 4. `requests.get()` to the dev-server URL | `fetch_status()` using `API_URL` (local address, not production) |
| 5. Check `status_code` before `.json()` | `if response.status_code != 200: ...` then `response.json()` |
| 6. Show the parsed data in the window | `show_data()` fills Labels and the department table |
| 7. try/except so a stopped server doesn't crash the GUI | `fetch_status()` handles `ConnectionError`, `Timeout`, other `RequestException`s, and invalid JSON |

**Be ready to explain:** `timeout=5` stops the app from freezing forever if the server hangs; `fetch_status()`
is separate from the window so the network logic can be tested alone; the table is built by looping
over `data["departments"]`, which is a list of dicts inside the JSON.

---

## Part 4 — Run the tests

```powershell
python manage.py test                     # Django endpoint: status 200, JSON type, keys, totals
python -m unittest discover tkinter_client   # client: success, server down, timeout, HTTP 500, bad JSON
```

---

## Part 5 — Screenshots for the PDF

**Code:**
1. `center/views.py` (the `status` view)
2. `center/urls.py` (and optionally `config/urls.py`)
3. `tkinter_client/client.py`: take two shots (top half with `fetch_status`, then the window class)

**Output:**
4. The browser at `/api/status/` showing the raw JSON (address bar visible)
5. The **Tkinter window displaying the data** returned by the endpoint
6. **The running Django server**: the terminal showing `Starting development server at http://127.0.0.1:8000/` and the `"GET /api/status/ HTTP/1.1" 200` lines
7. Optional: the window's red "Server unreachable" state, and the passing tests

Put them in Word or Google Docs with captions (Code and Output headings), then export to PDF.

---

## Part 6 — GitHub

1. https://github.com/new → e.g. `Baligat_Jenna_FinalsLab4`, **Public**, no README/.gitignore.
2. In the folder with `manage.py`:
   ```powershell
   git init
   git add .
   git status
   git commit -m "Add Week 16 remote command center: Django JsonResponse API and Tkinter client"
   git branch -M main
   git remote add origin https://github.com/jnnlyssbaligat/Baligat_Jenna_FinalsLab4.git
   git push -u origin main
   ```
3. Confirm `venv/` and `db.sqlite3` are not listed.

---

## Part 7 — JSON Payload Design Note

A draft is in `JSON_PAYLOAD_DESIGN_NOTE.md`. Your instructor's template wasn't in the PDF, so copy the
answers into theirs, in your own words.

---

## Submission checklist

- [ ] Project zip or GitHub link (−25 pts if missing)
- [ ] PDF of screenshots: code and output (−15 pts if missing)
- [ ] Completed JSON Payload Design Note
- [ ] Submitted before the end of the lab session

## Troubleshooting

| Problem | Fix |
|---|---|
| Window says "Server unreachable" | Start `python manage.py runserver` in the other terminal; make sure the port in `API_URL` matches |
| `ModuleNotFoundError: requests` | `python -m pip install requests` (inside the activated venv) |
| `ModuleNotFoundError: tkinter` | Reinstall Python from python.org with "tcl/tk and IDLE" ticked |
| `pip.exe` blocked | Use `python -m pip ...` |
| Browser shows 404 at `/` | Normal for other paths; the endpoint is `/api/status/` |
| Window opens but table stays empty | Open `/api/status/` in the browser. If it errors, read the server terminal |
| "Missing expected fields" | Key names in `views.py` and `client.py` don't match |

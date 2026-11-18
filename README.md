# Remote Command Center (Django + Tkinter) — Week 16

A headless Django endpoint returns JSON; a Tkinter desktop window calls it with `requests` and displays the data.

## Run it (two terminals)

```bash
python -m venv venv
venv\Scripts\activate          # Windows   (macOS/Linux: source venv/bin/activate)
python -m pip install -r requirements.txt

# Terminal 1
python manage.py runserver

# Terminal 2 (activate the venv again first)
python tkinter_client/client.py
```

Check the endpoint in a browser first: http://127.0.0.1:8000/api/status/

## Tests

```bash
python manage.py test
python -m unittest discover tkinter_client
```

## Structure

| Path | Purpose |
|------|---------|
| `center/views.py` | `status()` returns `JsonResponse` |
| `center/urls.py` | Routes `api/status/` |
| `tkinter_client/client.py` | Tkinter interface using `requests.get()` |
| `JSON_PAYLOAD_DESIGN_NOTE.md` | Payload design notes |

Course: PC15 Python Programming 2 w/ Lab — National Teachers College

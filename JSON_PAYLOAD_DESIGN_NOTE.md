# JSON Payload Design Note — Week 16: Remote Command Center

**Name:** Jenna Baligat  **Course:** PC15 Python Programming 2 w/ Lab  **Date:** November 18, 2026

> Draft based on this project's code. Your instructor's template wasn't in the assignment PDF, so
> adapt it to their questions and rewrite in your own words.

## 1. Endpoint

| Item | Value |
|---|---|
| URL | `GET http://127.0.0.1:8000/api/status/` |
| Django view | `center.views.status` |
| Response type | `application/json` via `JsonResponse` |
| Success status | `200 OK` |
| Authentication | None (local practice endpoint) |

## 2. Payload

```json
{
  "status": "ok",
  "server_time": "2026-11-18 18:41:52",
  "employee_count": 29,
  "online_now": 22,
  "departments": [
    {"name": "Engineering", "staff": 14, "online": 11},
    {"name": "Support", "staff": 9, "online": 7},
    {"name": "Operations", "staff": 6, "online": 4}
  ]
}
```

| Field | Type | Meaning | Used by the Tkinter app for |
|---|---|---|---|
| `status` | string | Health of the server (`"ok"`) | Status line and its colour |
| `server_time` | string | Server's local time, `YYYY-MM-DD HH:MM:SS` | "Server time" card |
| `employee_count` | integer | Total staff | "Employees" card |
| `online_now` | integer | Staff currently online | "Online now" card |
| `departments` | list of objects | One entry per department | Rows of the table |
| `departments[].name` | string | Department name | Table column |
| `departments[].staff` | integer | Staff in that department | Table column |
| `departments[].online` | integer | Staff of that department online | Table column |

## 3. Design decisions and why

1. **Flat top-level fields for headline values.** The client can read `data["employee_count"]` directly, with no digging.
2. **A list of objects for repeating data.** Departments can grow or shrink without changing the client, which just loops over the list.
3. **Totals computed on the server** from the same list, so the numbers can never disagree with the table.
4. **Only JSON-safe types** (strings, integers, lists, dicts). Django's `JsonResponse` converts Python dicts directly. A `datetime` would not serialise, so I send the time as a formatted string.
5. **Only what the screen needs.** No passwords, emails or personal details are included. This is data minimisation, and it means a leaked response reveals little.
6. **A status field** gives the client one simple value to show health at a glance.

## 4. How the client handles the response

1. `requests.get(url, timeout=5)`, so the client never waits forever.
2. `except ConnectionError / Timeout / RequestException` shows a friendly message, and the GUI stays open.
3. Check `response.status_code == 200` **before** calling `.json()`.
4. Catch `ValueError` if the body isn't valid JSON.
5. If a key is missing (`KeyError`), show an error instead of crashing.

## 5. Error cases tested

| Situation | Result in the window |
|---|---|
| Server stopped | Red "Server unreachable..." message, values reset to `--` |
| Server very slow | "The server took too long to respond." |
| HTTP 500 / 404 | "Server returned HTTP 500." and the body is not parsed |
| Not valid JSON | "The server did not return valid JSON." |
| Server restarted | The next refresh recovers automatically |

## 6. Changes and security for a real deployment

- **Authentication:** this endpoint is open. In the final project, require a login or an API token so only authorised admin tools can read the data (builds on Week 15).
- **HTTPS** instead of plain HTTP once off the local machine.
- **Versioning** (`/api/v1/status/`) so the payload can change without breaking old clients.
- **Real data** from Django models instead of the sample list, and error responses in JSON too (e.g. `{"error": "..."}` with a correct status code).
- **Don't block the GUI:** for slower endpoints, run `requests` in a background thread so the window stays responsive.

## 7. Reflection

JSON is the shared language between the Django back end and the Tkinter front end. Neither side needs
to know how the other is built, only the agreed shape of the payload. Designing that shape carefully,
and checking the status code before trusting the body, makes the connection predictable. These are
the same patterns my final project will use to link its Tkinter admin tool to the Django backend.

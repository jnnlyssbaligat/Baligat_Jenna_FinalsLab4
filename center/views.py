from django.http import JsonResponse
from django.utils import timezone

# Sample data for the command center. In the final project this would come from the database.
DEPARTMENTS = [
    {"name": "Engineering", "staff": 14, "online": 11},
    {"name": "Support", "staff": 9, "online": 7},
    {"name": "Operations", "staff": 6, "online": 4},
]


def index(request):
    """Tiny helper so the root URL isn't a 404 when you open the server in a browser."""
    return JsonResponse({"service": "Remote Command Center API", "endpoints": ["/api/status/"]})


def status(request):
    """Headless view: no template, just a plain Python dict turned into JSON."""
    staff_total = sum(d["staff"] for d in DEPARTMENTS)
    online_total = sum(d["online"] for d in DEPARTMENTS)

    data = {
        "status": "ok",
        "server_time": timezone.localtime().strftime("%Y-%m-%d %H:%M:%S"),
        "employee_count": staff_total,
        "online_now": online_total,
        "departments": DEPARTMENTS,
    }
    return JsonResponse(data)

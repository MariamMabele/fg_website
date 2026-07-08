upcoming = frappe.db.get_all(
    "Workshop Event",
    filters={
        "published": 1,
        "status": ["in", ["Open", "Full", "Closed"]]
    },
    fields=[
        "name",
        "title",
        "city",
        "country",
        "display_date",
        "start_date",
        "end_date",
        "seat_count",
        "seats_taken",
        "status",
        "short_description",
        "cover_image",
        "learning_course"
    ],
    order_by="start_date asc",
    limit=3
)

past = frappe.db.get_all(
    "Workshop Event",
    filters={
        "published": 1,
        "status": "Completed"
    },
    fields=[
        "name",
        "title",
        "city",
        "country",
        "display_date",
        "start_date",
        "end_date",
        "cover_image",
        "short_description",
        "learning_course"
    ],
    order_by="start_date desc",
    limit=3
)

def normalize(rows):
    clean = []
    for row in rows:
        clean.append({
            "name": row.get("name"),
            "title": row.get("title") or "",
            "city": row.get("city") or "",
            "country": row.get("country") or "",
            "display_date": str(row.get("display_date") or ""),
            "start_date": str(row.get("start_date") or ""),
            "end_date": str(row.get("end_date") or ""),
            "seat_count": row.get("seat_count") or 0,
            "seats_taken": row.get("seats_taken") or 0,
            "status": row.get("status") or "",
            "short_description": row.get("short_description") or "",
            "cover_image": row.get("cover_image") or "",
            "learning_course": row.get("learning_course") or ""
        })
    return clean

data["page_data"] = {
    "upcoming_events": normalize(upcoming),
    "past_events": normalize(past)
}
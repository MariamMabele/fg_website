global_sponsors = frappe.db.get_all(
    "Sponsor Profile",
    filters={
        "published": 1,
    },
    fields=[
        "name",
        "organization_name",
        "logo",
        "website",
        "country",
        "city",
        "sponsor_level",
        "default_tier",
        "short_description",
        "featured_quote",
        "sort_order"
    ],
    order_by="sort_order asc, modified desc"
)

event_sponsors = frappe.db.get_all(
    "Event Sponsorship",
    filters={
        "published": 1,
    },
    fields=[
        "name",
        "workshop_event",
        "sponsor_profile",
        "tier",
        "support_type",
        "amount_or_value",
        "notes"
    ],
    order_by="modified desc"
)

event_names = [row.get("workshop_event") for row in event_sponsors if row.get("workshop_event")]
sponsor_names = [row.get("sponsor_profile") for row in event_sponsors if row.get("sponsor_profile")]

event_map = {}
if event_names:
    event_rows = frappe.db.get_all(
        "Workshop Event",
        filters={"name": ["in", event_names]},
        fields=["name", "title", "city", "country"]
    )
    event_map = {row["name"]: row for row in event_rows}

sponsor_map = {}
if sponsor_names:
    sponsor_rows = frappe.db.get_all(
        "Sponsor Profile",
        filters={"name": ["in", sponsor_names]},
        fields=["name", "organization_name", "logo", "website"]
    )
    sponsor_map = {row["name"]: row for row in sponsor_rows}

def normalize_global(rows):
    clean = []
    for row in rows:
        clean.append({
            "name": row.get("name"),
            "organization_name": row.get("organization_name") or "",
            "logo": row.get("logo") or "",
            "website": row.get("website") or "",
            "country": row.get("country") or "",
            "city": row.get("city") or "",
            "sponsor_level": row.get("sponsor_level") or "",
            "default_tier": row.get("default_tier") or "",
            "short_description": row.get("short_description") or "",
            "featured_quote": row.get("featured_quote") or "",
            "sort_order": row.get("sort_order") or 0
        })
    return clean

def normalize_event(rows):
    clean = []
    for row in rows:
        sponsor = sponsor_map.get(row.get("sponsor_profile")) or {}
        event = event_map.get(row.get("workshop_event")) or {}
        clean.append({
            "name": row.get("name"),
            "sponsor_name": sponsor.get("organization_name") or "",
            "logo": sponsor.get("logo") or "",
            "website": sponsor.get("website") or "",
            "event_title": event.get("title") or "",
            "event_city": event.get("city") or "",
            "event_country": event.get("country") or "",
            "tier": row.get("tier") or "",
            "support_type": row.get("support_type") or "",
            "amount_or_value": row.get("amount_or_value") or "",
            "notes": row.get("notes") or ""
        })
    return clean

data["page_data"] = {
    "global_sponsors": normalize_global(global_sponsors),
    "event_sponsors": normalize_event(event_sponsors),
}

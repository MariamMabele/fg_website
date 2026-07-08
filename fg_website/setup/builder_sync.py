from __future__ import annotations

from pathlib import Path
import re

import frappe
from frappe.utils import now

PAGE_DEFINITIONS = [
	{"key": "home", "title": "Home", "route": "home", "is_home_page": True},
	{"key": "events", "title": "Events", "route": "events"},
	{"key": "contribute", "title": "Contribute", "route": "contribute"},
	{"key": "organize", "title": "Organize", "route": "organize"},
	{"key": "coach", "title": "Coach", "route": "coach"},
	{"key": "sponsors", "title": "Sponsors", "route": "sponsors"},
	{"key": "code_of_conduct", "title": "Code of Conduct", "route": "code-of-conduct"},
]

HTML_MARKER_TEMPLATE = "<!-- fg_website:managed:{kind}:{key} -->"
SCRIPT_MARKER_TEMPLATE = "# fg_website:managed:script:{key}"


def after_install():
	sync_builder_pages()


def after_migrate():
	sync_builder_pages()


def sync_builder_pages(force: bool = False):
	"""Create or update Builder pages from app-owned page source files."""
	if not frappe.db.exists("DocType", "Builder Page"):
		return

	for definition in PAGE_DEFINITIONS:
		_sync_builder_page(definition, force=force)

	_set_builder_home_page()


def _sync_builder_page(definition: dict, force: bool = False):
	source = _load_page_source(definition["key"])
	page_name = frappe.db.get_value("Builder Page", {"route": definition["route"]}, "name")

	if page_name:
		doc = frappe.get_doc("Builder Page", page_name)
		if not force and not _is_managed_page(doc, definition["key"]):
			return
		if not force and _has_meaningful_blocks(doc):
			return
	else:
		doc = frappe.new_doc("Builder Page")
		doc.route = definition["route"]

	preview_html, runtime_html = _split_body_html(source["body_html"])
	blocks_json = _build_blocks_json(preview_html)

	doc.page_title = definition["title"]
	doc.route = definition["route"]
	doc.head_html = _build_head_html(definition["key"], source["head_html"])
	doc.body_html = _build_body_html(definition["key"], runtime_html)
	doc.page_data_script = _build_page_data_script(definition["key"], source["page_data_script"])
	doc.blocks = blocks_json
	doc.draft_blocks = blocks_json
	doc.published = 1
	doc.published_at = doc.published_at or now()

	doc.flags.ignore_permissions = True
	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)


def _set_builder_home_page():
	if not frappe.db.exists("DocType", "Builder Settings"):
		return

	current_home_page = frappe.db.get_single_value("Builder Settings", "home_page")
	if current_home_page:
		return

	frappe.db.set_single_value("Builder Settings", "home_page", "home")


def _load_page_source(page_key: str) -> dict[str, str]:
	page_dir = _get_pages_root() / page_key
	return {
		"head_html": _read_optional(page_dir / "head.html"),
		"body_html": _read_optional(page_dir / "body.html"),
		"page_data_script": _read_optional(page_dir / "data_script.py"),
	}


def _get_pages_root() -> Path:
	return Path(__file__).resolve().parents[1] / "frappe_girls" / "page_source" / "pages"


def _read_optional(path: Path) -> str:
	return path.read_text(encoding="utf-8").strip() if path.exists() else ""


def _build_head_html(page_key: str, content: str) -> str:
	if not content:
		return ""
	return f"{HTML_MARKER_TEMPLATE.format(kind='head', key=page_key)}\n{content}"


def _build_body_html(page_key: str, content: str) -> str:
	marker = HTML_MARKER_TEMPLATE.format(kind="body", key=page_key)
	if not content:
		return marker
	return f"{marker}\n{content}"


def _build_page_data_script(page_key: str, content: str) -> str:
	if not content:
		return ""
	return f"{SCRIPT_MARKER_TEMPLATE.format(key=page_key)}\n{content}"


def _is_managed_page(doc, page_key: str) -> bool:
	body_marker = HTML_MARKER_TEMPLATE.format(kind="body", key=page_key)
	script_marker = SCRIPT_MARKER_TEMPLATE.format(key=page_key)

	body_html = (doc.body_html or "").lstrip()
	page_data_script = (doc.page_data_script or "").lstrip()

	return body_html.startswith(body_marker) or page_data_script.startswith(script_marker)


def _split_body_html(content: str) -> tuple[str, str]:
	if not content:
		return "", ""

	script_pattern = re.compile(r"<script\b[^>]*>[\s\S]*?</script>", re.IGNORECASE)
	scripts = script_pattern.findall(content)
	preview_html = script_pattern.sub("", content).strip()
	runtime_html = "\n".join(scripts).strip()
	return preview_html, runtime_html


def _build_blocks_json(content: str) -> str:
	root_block = {
		"blockId": "root",
		"element": "div",
		"originalElement": "body",
		"attributes": {},
		"baseStyles": {
			"display": "flex",
			"flexWrap": "wrap",
			"flexShrink": 0,
			"flexDirection": "column",
			"alignItems": "center",
		},
		"rawStyles": {},
		"mobileStyles": {},
		"tabletStyles": {},
		"classes": [],
		"customAttributes": {},
		"dataKey": None,
		"children": [],
	}

	if content:
		root_block["children"].append(
			{
				"blockId": f"managed-html-{frappe.generate_hash(length=8)}",
				"blockName": "Managed HTML",
				"element": "div",
				"originalElement": "__raw_html__",
				"attributes": {},
				"baseStyles": {
					"width": "100%",
					"height": "fit-content",
				},
				"rawStyles": {},
				"mobileStyles": {},
				"tabletStyles": {},
				"classes": [],
				"customAttributes": {},
				"dataKey": None,
				"children": [],
				"innerHTML": content,
			}
		)

	return frappe.as_json([root_block], indent=None, separators=(",", ":"))


def _has_meaningful_blocks(doc) -> bool:
	blocks = frappe.parse_json(doc.draft_blocks or doc.blocks or "[]")
	if not isinstance(blocks, list) or not blocks:
		return False

	root = blocks[0] or {}
	children = root.get("children") or []
	return bool(children)

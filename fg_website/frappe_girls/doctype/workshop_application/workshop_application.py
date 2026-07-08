import frappe
from frappe.model.document import Document
from frappe.utils import cint


def sync_event_seats(workshop_event):
	if not workshop_event:
		return

	approved_count = frappe.db.count(
		"Workshop Application",
		{"workshop_event": workshop_event, "status": "Approved"},
	)
	event_values = frappe.db.get_value(
		"Workshop Event",
		workshop_event,
		["seat_count", "status"],
		as_dict=True,
	) or {}

	update_values = {"seats_taken": approved_count}
	seat_count = cint(event_values.get("seat_count"))
	status = event_values.get("status")

	if seat_count:
		if approved_count >= seat_count and status == "Open":
			update_values["status"] = "Full"
		elif approved_count < seat_count and status == "Full":
			update_values["status"] = "Open"

	frappe.db.set_value("Workshop Event", workshop_event, update_values, update_modified=True)


class WorkshopApplication(Document):
	def validate(self):
		self.status = self.status or "Pending"

		if self.workshop_event:
			event_values = frappe.db.get_value(
				"Workshop Event",
				self.workshop_event,
				["learning_course", "learning_batch"],
				as_dict=True,
			) or {}
			if not self.learning_course:
				self.learning_course = event_values.get("learning_course")
			if not self.learning_batch:
				self.learning_batch = event_values.get("learning_batch")

	def after_insert(self):
		sync_event_seats(self.workshop_event)

	def on_update(self):
		sync_event_seats(self.workshop_event)

	def on_trash(self):
		sync_event_seats(self.workshop_event)

import frappe
from frappe.model.document import Document
from frappe.utils import cint, formatdate


class WorkshopEvent(Document):
	def validate(self):
		if self.start_date and self.end_date and self.end_date < self.start_date:
			frappe.throw("End Date cannot be before Start Date.")

		self.seat_count = max(cint(self.seat_count), 0)
		self.seats_taken = max(cint(self.seats_taken), 0)

		if self.seat_count and self.seats_taken > self.seat_count:
			self.seats_taken = self.seat_count

		if not self.display_date and self.start_date:
			if self.end_date and self.end_date != self.start_date:
				self.display_date = f"{formatdate(self.start_date)} - {formatdate(self.end_date)}"
			else:
				self.display_date = formatdate(self.start_date)

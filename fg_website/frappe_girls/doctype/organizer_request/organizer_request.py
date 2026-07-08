from frappe.model.document import Document


class OrganizerRequest(Document):
	def validate(self):
		self.status = self.status or "New"

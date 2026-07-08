from frappe.model.document import Document


class CoachInterest(Document):
	def validate(self):
		self.status = self.status or "New"

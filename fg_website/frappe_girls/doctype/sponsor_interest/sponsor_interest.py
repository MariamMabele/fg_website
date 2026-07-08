from frappe.model.document import Document


class SponsorInterest(Document):
	def validate(self):
		self.status = self.status or "New"

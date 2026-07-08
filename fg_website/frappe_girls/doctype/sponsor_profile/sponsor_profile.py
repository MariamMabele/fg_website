from frappe.model.document import Document


class SponsorProfile(Document):
	def validate(self):
		if self.sort_order is None:
			self.sort_order = 0

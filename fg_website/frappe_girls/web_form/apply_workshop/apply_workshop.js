frappe.ready(function () {
	const params = new URLSearchParams(window.location.search);
	const workshopEvent = params.get("workshop_event");
	if (workshopEvent && frappe.web_form) {
		frappe.web_form.set_value("workshop_event", workshopEvent);
	}
});

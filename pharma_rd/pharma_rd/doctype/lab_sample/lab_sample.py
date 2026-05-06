from frappe.model.document import Document

class LabSample(Document):
    def before_save(self):
        if not self.sample_id:
            self.sample_id = self.name

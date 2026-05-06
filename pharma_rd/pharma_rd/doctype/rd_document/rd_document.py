import frappe
from frappe.model.document import Document
from frappe.utils import add_months, getdate

class RDDocument(Document):
    def validate(self):
        if self.effective_date and self.review_period and not self.expiry_date:
            self.expiry_date = add_months(self.effective_date, self.review_period)
        
    def on_submit(self):
        if self.status == "Approved":
            self.db_set("status", "Effective")

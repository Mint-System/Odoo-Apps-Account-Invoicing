from odoo import fields, models


class ResCurrency(models.Model):
    _inherit = "res.currency"

    def _default_invoice_reference_model(self):
        """Get the invoice reference model according to the company's country."""
        country_code = self.env.company.country_id.code
        country_code = country_code and country_code.lower()
        if country_code:
            for model in self._fields["invoice_reference_model"].get_values(self.env):
                if model.startswith(country_code):
                    return model
        return "odoo"

    invoice_reference_type = fields.Selection(
        string="Communication Type",
        required=True,
        selection=[("none", "Open"), ("partner", "Based on Customer"), ("invoice", "Based on Invoice")],
        default="invoice",
        help="You can set here the default communication that will appear on customer invoices, \
            once validated, to help the customer to refer to that particular invoice when making the payment.",
    )
    invoice_reference_model = fields.Selection(
        string="Communication Standard",
        required=True,
        selection=[("odoo", "Odoo"), ("euro", "European"), ("ch", "Switzerland")],
        default=_default_invoice_reference_model,
        help="You can choose different models for each type of reference. The default one is the Odoo reference.",
    )

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    date_order = fields.Date(compute="_compute_date_order", store=True)

    @api.depends("sale_line_ids")
    def _compute_date_order(self):
        for line in self:
            if line.sale_line_ids:
                line.date_order = max(line.sale_line_ids.order_id.mapped("date_order"))
            else:
                line.date_order = False

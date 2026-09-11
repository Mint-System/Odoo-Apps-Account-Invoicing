from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

  
    @api.model_create_multi
    def create(self, vals_list):
        """ Only with this override the original behviour of 
            OCA module (computing external_name) is preserved and
            external_name is not overriden if created from sale order
        """
        pending = {}
        for i, vals in enumerate(vals_list):
            if vals.get("external_name") and vals.get("product_id"):
                pending[i] = vals.pop("external_name")

        lines = super().create(vals_list)

        for i, value in pending.items():
            lines[i].external_name = value

        return lines

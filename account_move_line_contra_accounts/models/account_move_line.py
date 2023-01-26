from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    contra_accounts = fields.Chart(compute='_compute_contra_accounts', readonly='1', store=True)

    @api.depends('move_id.line_ids')
    def _compute_contra_accounts(self):
        for rec in self:
            account_codes = rec.move_id.line_ids.mapped('code')
            account_codes.remove(rec.code)
            account_codes.sort()
            rec.contra_accounts = ', '.join(account_codes)

from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    ref = fields.Text()

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    ref = fields.Text()

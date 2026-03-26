# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AccountMoveSendWizard(models.TransientModel):
    _inherit = "account.move.send.wizard"

    is_move_sent = fields.Boolean(related="move_id.is_move_sent")
    is_being_sent = fields.Boolean(related="move_id.is_being_sent")

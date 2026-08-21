import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        """Show warning if one is set."""

        # Copied from odoo/addons/account/models/account_move.py
        for move in self:
            warning = {}
            if move.partner_id:
                p = move.partner_id
                if p.invoice_warn == "no-message" and p.parent_id:
                    p = p.parent_id
                if p.invoice_warn and p.invoice_warn != "no-message":
                    # Block if partner only has warning but parent company is blocked
                    if (
                        p.invoice_warn != "block"
                        and p.parent_id
                        and p.parent_id.invoice_warn == "block"
                    ):
                        p = p.parent_id
                    warning = {
                        "title": _("Warning for %s", p.name),
                        "message": p.invoice_warn_msg,
                    }
                    if p.invoice_warn == "block":
                        move.partner_id = False
                        warning = {"warning": warning}

            if warning:
                odoobot = move.env.ref("base.partner_root")
                move.message_post(
                    body=warning["title"] + ": " + warning["message"],
                    message_type="comment",
                    subtype_xmlid="mail.mt_note",
                    author_id=odoobot.id,
                )

        return super().action_post()

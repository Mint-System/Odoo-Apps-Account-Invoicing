import logging

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"

    @api.model
    def _send_email(self, options):
        """
        Method overwrite to set a new `subtype_id`, `email_layout_xmlid` and add `email_add_signature`.
        """
        partner = self.env["res.partner"].browse(options.get("partner_id"))
        followup_contacts = partner._get_all_followup_contacts() or partner
        followup_recipients = options.get("email_recipient_ids", followup_contacts)
        sent_at_least_once = False
        for to_send_partner in followup_recipients:
            email = to_send_partner.email
            if email and email.strip():
                self = self.with_context(lang=partner.lang or self.env.user.lang)
                body_html = self.with_context(mail=True).get_followup_report_html(options)

                attachment_ids = options.get(
                    "attachment_ids",
                    partner._get_invoices_to_print(options).message_main_attachment_id.ids,
                )

                partner.with_context(
                    mail_post_autofollow=True,
                    mail_notify_author=True,
                    lang=partner.lang or self.env.user.lang,
                ).message_post(
                    partner_ids=[to_send_partner.id],
                    author_id=partner._get_followup_responsible().partner_id.id,
                    email_from=self._get_email_from(options) or None,
                    body=body_html,
                    subject=self._get_email_subject(options),
                    reply_to=self._get_email_reply_to(options),
                    subtype_id=self.env.ref("mail.mt_comment").id,
                    model_description=_("payment reminder"),
                    email_layout_xmlid="mail.mail_notification_layout",
                    attachment_ids=attachment_ids,
                    email_add_signature=False,
                )
                sent_at_least_once = True
        if not sent_at_least_once:
            raise UserError(
                _(
                    "You are trying to send an Email, but no follow-up contact has any email address set for customer '%s'",
                    partner.name,
                )
            )

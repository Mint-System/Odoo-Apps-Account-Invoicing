import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"

    def _get_followup_report_columns_name(self):
        """
        OVERWRITE: Return the columns without inlinde style.
        """
        return [
            {"name": _("Reference"), "class": "o_reference"},
            {"name": _("Date"), "class": "date o_date"},
            {"name": _("Due Date"), "class": "date o_due_date"},
            {"name": _("Origin"), "class": "o_origin"},
            {"name": _("Communication"), "class": "o_communication"},
            {"name": _("Total Due"), "class": "number o_price_total"},
        ]

    def _get_followup_report_lines(self, options):
        lines = super()._get_followup_report_lines(options)
        for line in lines:
            line["columns"][0]["style"] = ""
            line["columns"][1]["style"] = ""
            line["columns"][2]["style"] = ""
            line["columns"][3]["style"] = ""
            line["columns"][4]["style"] = ""
        return lines

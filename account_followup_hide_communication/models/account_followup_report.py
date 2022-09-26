from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"

    def _get_columns_name(self, options):
        res = super(AccountFollowupReport , self)._get_columns_name(options)
        for index, item in enumerate(res):
            if item.get('name') and item.get('name') == _('Communication'):
                res[index]['style'] = 'display:none;'
        return res

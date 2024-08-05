from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    def _cron_try_auto_reconcile_statement_lines(self, batch_size=None, limit_time=0):
        def _compute_st_lines_to_reconcile(configured_company_ids):
            remaining_line_id = None
            limit = batch_size + 1 if batch_size else None
            domain = [
                ("is_reconciled", "=", False),
                ("create_date", ">", start_time.date() - relativedelta(months=3)),
                ("company_id", "in", configured_company_ids),
            ]
            query_obj = self._search(domain, limit=limit)
            query_obj.order = '"account_bank_statement_line"."cron_last_check" ASC NULLS FIRST,"account_bank_statement_line"."id"'
            query_str, query_params = query_obj.select("account_bank_statement_line.id")
            self._cr.execute(query_str, query_params)
            st_line_ids = [r[0] for r in self._cr.fetchall()]
            if batch_size and len(st_line_ids) > batch_size:
                remaining_line_id = st_line_ids[batch_size]
                st_line_ids = st_line_ids[:batch_size]
            st_lines = self.env["account.bank.statement.line"].browse(st_line_ids)
            return st_lines, remaining_line_id

        start_time = fields.Datetime.now()

        self.env["account.reconcile.model"].flush_model()

        query_obj = self.env["account.reconcile.model"]._search(
            [
                ("auto_reconcile", "=", True),
                ("rule_type", "in", ("writeoff_suggestion", "invoice_matching")),
            ]
        )
        query_obj.order = "company_id"
        query_str, query_params = query_obj.select("DISTINCT company_id")
        self._cr.execute(query_str, query_params)
        configured_company_ids = [r[0] for r in self._cr.fetchall()]
        if not configured_company_ids:
            return

        self.env["account.bank.statement.line"].flush_model()
        st_lines, remaining_line_id = (
            (self, None)
            if self
            else _compute_st_lines_to_reconcile(configured_company_ids)
        )

        nb_auto_reconciled_lines = 0
        for index, st_line in enumerate(st_lines):
            if (
                limit_time
                and fields.Datetime.now().timestamp() - start_time.timestamp()
                > limit_time
            ):
                remaining_line_id = st_line.id
                st_lines = st_lines[:index]
                break
            wizard = (
                self.env["bank.rec.widget"]
                .with_context(default_st_line_id=st_line.id)
                .new({})
            )
            wizard._action_trigger_matching_rules()
            if wizard.state == "valid" and wizard.matching_rules_allow_auto_reconcile:
                try:
                    wizard.button_validate(async_action=False)
                    if st_line.is_reconciled:
                        st_line.move_id.message_post(
                            body=_(
                                "This bank transaction has been automatically validated using the reconciliation model '%s'.",
                                ", ".join(
                                    st_line.move_id.line_ids.reconcile_model_id.mapped(
                                        "name"
                                    )
                                ),
                            )
                        )
                        nb_auto_reconciled_lines += 1
                except UserError:
                    continue

        st_lines.write({"cron_last_check": start_time})

        if remaining_line_id:
            remaining_st_line = self.env["account.bank.statement.line"].browse(
                remaining_line_id
            )
            if nb_auto_reconciled_lines or not remaining_st_line.cron_last_check:
                self.env.ref(
                    "account_accountant.auto_reconcile_bank_statement_line"
                )._trigger()

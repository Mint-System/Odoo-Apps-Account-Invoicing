##############################################################################
#
# Nivels GmbH
# Comercialstrasse 19
# 7000 Chur
#
# Copyright (C) 2022 Nivels GmbH.
# All Rights Reserved
#
##############################################################################

from datetime import datetime, timedelta

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    has_discount = fields.Boolean("Discount", default=False)


class AccountMove(models.Model):
    _inherit = "account.move"

    discount_payment_term_id = fields.Many2one(
        "account.payment.term",
        string="Vendor Discount Term",
        help="Assigned supplier payment term used for discount calculation.",
    )
    has_discount = fields.Boolean(
        string="Supplier Discount",
        help="True if the vendor has can be used for discount",
    )
    discount_date = fields.Date("Discount Date")

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        """
        Override of this method, Onchange of customer set the Discount Payment Term on Bill
        Latter It'll be modified
        """
        super()._onchange_partner_id()
        for rec in self:
            if rec.partner_id.discount_payment_term_id:
                rec.discount_payment_term_id = (
                    rec.partner_id.discount_payment_term_id.id
                )

    def action_update_discount(self):
        """
        Call this methood via server action, this method will add/update/remove
        the discount product or change in price,
        Based on the Discount Payment Term set on the Bill.
        """

        # To check & remove if the bill have removed Discount Payment Term or
        # present of discount line in invoice line.``
        for move in self.filtered(
            lambda x: not x.discount_payment_term_id and x.state != "cancel"
        ):
            context = {
                "default_move_type": self._context.get("default_move_type"),
                "journal_id": move.journal_id,
                "default_partner_id": move.commercial_partner_id,
                "default_currency_id": move.currency_id or move.company_currency_id,
            }
            posted_invoice = []

            # check if any record is posted them first, change the state(Draft),
            # and add to the posted_invoice list
            if move.state == "posted":
                posted_invoice.append(move)
                move.button_draft()

            invoice_line = move.invoice_line_ids.filtered(lambda x: x.has_discount)

            # if any present discounted lines the remove it
            if invoice_line:
                move.with_context(context).write(
                    {
                        "has_discount": False,
                        "discount_date": False,
                        "invoice_line_ids": [(2, line.id) for line in invoice_line],
                    }
                )

            # check the if posted_invoice list is contain recored then rechange the state
            if posted_invoice:
                move.action_post()

        # make lopp for checking if record having discount payment term and state is not cancel
        # If found then exexute below logic and add discount product if applicable
        for rec in self.filtered(
            lambda x: x.discount_payment_term_id and x.state != "cancel"
        ):
            # check if any record is posted them first, change the state(Draft),
            # and add to the posted_invoice list
            posted_invoice = []

            # for adding seprate line due to different taxes added on different invoice lines
            tax_groups = [
                []
                for _ in range(0, 1)
                if rec.invoice_line_ids.filtered(
                    lambda x: not x.has_discount and not x.tax_ids
                )
            ]

            # prepare list to remove old invoice line and add new
            invoice_line = [
                (2, line.id)
                for line in rec.invoice_line_ids.filtered(lambda x: x.has_discount)
            ]

            for tax in rec.invoice_line_ids.filtered(lambda x: not x.has_discount):
                if tax.tax_ids.ids not in tax_groups:
                    tax_groups.append(tax.tax_ids.ids)

            # if posted then add posted_invoice and make them to draft
            if rec.state == "posted":
                posted_invoice.append(rec)
                rec.button_draft()

            # to get first minimun days discount term line from discount payment term
            discount_line = rec.discount_payment_term_id.line_ids.filtered(
                lambda x: x.value == "discount" and x.discount_product
            ).sorted(key=lambda x: x.days, reverse=False)

            context = {
                "default_move_type": self._context.get("default_move_type"),
                "journal_id": rec.journal_id,
                "default_partner_id": rec.commercial_partner_id,
                "default_currency_id": rec.currency_id or rec.company_currency_id,
            }

            # First remove all discount line, after if condition satisfy then line will be added.
            if invoice_line:
                rec.with_context(context).write(
                    {
                        "has_discount": False,
                        "discount_date": False,
                        "invoice_line_ids": invoice_line,
                    }
                )

            # discount line is adding on the basis of invoice date and discount_line if any
            # break the looping first discount line is appear also it's sorted by the days
            if rec.invoice_date and discount_line:
                for discount in discount_line:
                    # calculate days different
                    discount_date = rec.invoice_date + timedelta(discount.days)

                    # check if descount line is below from today
                    if discount_date > datetime.today().date():

                        # add context data for some default value
                        # With looping prepare the list of tuple (number of discount line),
                        # base on the taxes group
                        rec.with_context(context).write(
                            {
                                "has_discount": True,
                                "discount_date": discount_date,
                                "invoice_line_ids": [
                                    (
                                        0,
                                        0,
                                        {
                                            "name": discount.discount_product.name,
                                            "product_id": discount.discount_product.id,
                                            "tax_ids": [(6, 0, tax)],
                                            "move_id": rec.id,
                                            "account_id": discount.discount_product.property_account_expense_id.id or rec.journal_id.default_account_id.id,
                                            "quantity": 1,
                                            "has_discount": True,
                                            "price_unit": -(
                                                sum(
                                                    rec.invoice_line_ids.filtered(
                                                        lambda x: not x.has_discount
                                                        and x.tax_ids.ids == tax
                                                    ).mapped("price_subtotal")
                                                )
                                                * (1 - (discount.value_amount / 100))
                                            ),
                                        },
                                    )
                                    for tax in tax_groups
                                ],
                            }
                        )
                        break

            # check the if posted_invoice list is contain recored then rechange the state
            if posted_invoice:
                for post in posted_invoice:
                    post.action_post()

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        """
            Override of this method to remove contextual action from the action menu
            and will be adding on only if invoice type is not In Invoice.
        Args:
            view_id (_type_, optional): To specify Id perticular view.
                                        Defaults to None.
            view_type (str, optional): To specify the type of view e.g. Form, tree,etc.
                                        Defaults to "form".
            toolbar (bool, optional): Tolbar contain print menu and contextual action.
                                        Defaults to False.
            submenu (bool, optional): If any used. Defaults to False.

        Returns:
            _type_: xml architecture of all views
        """
        result = super(AccountMove, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )

        #  This condition is true if invoice type is not in invoice
        #  and context having default_move_type
        # Then we will remove the Update Discount server action
        if (
            toolbar
            and result.get("toolbar")
            and self._context.get("default_move_type") != "in_invoice"
        ):
            for action in result["toolbar"]["action"]:
                if (
                    action["name"] == "Update Discount"
                    and action["type"] == "ir.actions.server"
                ):
                    result["toolbar"]["action"].remove(action)
        return result

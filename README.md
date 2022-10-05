# Odoo Apps: Account Invoicing

Collection of account and invoicing model related modules.

## Usage

Clone module into Odoo addon directory.

```bash
git clone git@github.com:mint-system/odoo-apps-account-invoicing.git ./addons/account_invoicing
```

## Available modules

| Module | Summary |
| --- | --- |
| [account_followup_hide_communication](account_followup_hide_communication) |         Remove communication column from followup report. |
| [account_invoice_carrier](account_invoice_carrier) |         Set delivery method on invoice. |
| [account_invoice_comment](account_invoice_comment) |         Comment field in invoice. |
| [account_invoice_description](account_invoice_description) |         Add description to invoice form and report. |
| [account_invoice_detail](account_invoice_detail) |         Add field salesperson to invoice. |
| [account_invoice_notes](account_invoice_notes) |         Footer and header notes for invoice that are copied from sale order. |
| [account_invoice_sale_partner](account_invoice_sale_partner) |         Set sale order contact on invoice. |
| [account_invoice_select_bank](account_invoice_select_bank) |         Select bank by matching currency of invoice. |
| [account_move_invoice_partner](account_move_invoice_partner) |         Separate field for invoice address. |
| [account_move_line_accounting_description_stock](account_move_line_accounting_description_stock) |         Copy stock move description to external name on invoice creation. |
| [account_move_line_link_pickings](account_move_line_link_pickings) |         Get linked pickings for each account move line. |
| [account_move_line_position](account_move_line_position) |         Get line position from purchase or sale order. |
| [account_move_post_warn](account_move_post_warn) |         When an invoice is posted show the warning message from the partner. |
| [account_move_reconciled_date](account_move_reconciled_date) |         Show reconcile date of bank statement for account move. |
| [l10n_ch_disable_default_reports](l10n_ch_disable_default_reports) |         Disable QR and ISR report generation. |
| [l10n_ch_qr_iban](l10n_ch_qr_iban) |         Create payment references for QR invoice without ISR subscription. |
| [nivels_deduct_supplier_discount](nivels_deduct_supplier_discount) |     "license": "OPL-1", |
| [purchase_invoice_prepare_partner](purchase_invoice_prepare_partner) |         Copy invoice and shipping contacts to invoice. |
| [sale_invoice_carrier](sale_invoice_carrier) |         Set delivery method of transfer when creating invoice from sale order. |
| [sale_invoice_cash_rounding_default](sale_invoice_cash_rounding_default) |         Apply default cash rounding when invoicing sale orders. |
| [sale_invoice_line_description](sale_invoice_line_description) |         When invoicing a sale order use product reference and name as line description. |
| [sale_invoice_prepare_bank](sale_invoice_prepare_bank) |         Set bank on invoice by matching currency. |
| [sale_invoice_prepare_partner](sale_invoice_prepare_partner) |         Copy invoice and shipping contacts to invoice. |

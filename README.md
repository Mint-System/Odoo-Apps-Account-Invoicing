# Odoo Apps: Account Invoicing

Collection of account and invoicing model related modules.

## Usage

Clone module into Odoo addon directory.

```bash
git clone git@github.com:mint-system/odoo-apps-account-invoicing.git ./addons/account_invoicing
```

## Available modules

| Module                                                                    | Summary                                                              |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [account_invoice_description](account_invoice_description/)               | Add description to invoice form and report.                          |
| [account_invoice_detail](account_invoice_detail/)                         | Add field salesperson to invoice.                                    |
| [account_move_line_position](account_move_line_position/)                 | Get line position from purchase or sale order.                       |
| [account_move_line_link_pickings](account_move_line_link_pickings/)       | Get linked pickings foreach account move line.                       |
| [sale_invoice_cash_rounding_default](sale_invoice_cash_rounding_default/) | Apply default cash rounding when invoicing sale orders.              |
| [account_move_reconciled_date](account_move_reconciled_date/)             | Show reconcile date of bank statement for account move.              |
| [account_move_post_warn](account_move_post_warn/)                         | When an invoice is posted show the warning message from the partner. |
| [nivels_deduct_supplier_discount](nivels_deduct_supplier_discount/)       | Allow discount deduction on vendor bills.                            |
| [l10n_ch_qr_iban](l10n_ch_qr_iban/)                                       | Create payment references for QR invoice without ISR subscription.   |

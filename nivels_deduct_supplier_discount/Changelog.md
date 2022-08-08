# README

This modul allows to deduct discount on supplier invoices

### History

- 1.0:

### Technical description

This module allows to deduct discount on supplier invoices. To do that the user can
specify a product in the settings which will be used to calculate a discount on the
supplier invoice. The calculation of the discount is depending on the payment terms.

### New fields

To have no influence on the original ODOO booking system additional fields are required:

| Table                | Field name               | Description                                                                    |
| -------------------- | ------------------------ | ------------------------------------------------------------------------------ |
| res.partner          | discount_payment_term_id | Default payment term used for this supplier                                    |
| account.move         | discount_payment_term_id | Assigned supplier payment term used for discount calculation                   |
| account.move         | discount_date            | Calculated date until the discount can be taken                                |
| account.move         | has_discount             | Calculated boolean field indicating if the vendor has can be used for discount |
| account.payment.term | discount                 | Payment term option to indicate that this payment term is a discount           |
| account.payment.term | discount_product         | Product to use for the discount in vendor bills                                |

## Form extensions

### Payment term

In the form for _Payment Term_ we need a forth option indicating that this payment term
is used for discount. If this option is selected the "percentage" field and the
"discount_product" field should be available for the user.

### Partner form

In the "partner" form on the "Sale / Purchase" tab we need the field
"discount_payment_term_id" named "Vendor Discount Term". This should be taken to the
"Vendor bill" form as default if set.

### Vendor bill form

In the "vendor bill" form below the "Due Date" field we need the fields
"discount_payment_term_id" and "discount_date" (read-only). The field "has_discount"
will only be used for filtering (see below)

Here we need also an action for adding/updating the discount line item.

## Filters

In the "vendor bills" overview we need two filters:

- "Invoice has discount" (account.move.has_discount == True)
- "Invoice has no discount" (account.move.has_discount == False)

## Action

In the "vendor bill" overview and form we need an action called
"action_update_discount". This action will calculate the "discount_date" in the
account.move. The following rules should apply:

- The lowest number of days will be used for the calculation of the "discount_date". The
  percentage will be used for the calculation of the amount
- If this calculated discount_date is already in the past check if there are additional
  days/percentage combinations available to calculate the discount_date
- If the last discount_date is also already in the past the account.move.line with the
  discount product will be removed
- If the discount_date is in the future or today update/add the discount line with the
  specified discount product and taxes

### Use cases

- The user creates a vendor bill
- Within this invoice the user specifies the invoice date
- If the supplier has set the "use_supplier_discount" the assigned
  "supplier_payment_term" will be used as "supplier_discount_term"
- The user presses a button called "Add/update discount" and the discount will be
  calculated and added/updated in the vendor bill

### Calculation

Odoo recommends to use as follows:

- Percent = 98% if you want to have 2% discount from the total amount
- Number of days where this discount apply

### Odoo Info

- Odoo 14 Enterprise

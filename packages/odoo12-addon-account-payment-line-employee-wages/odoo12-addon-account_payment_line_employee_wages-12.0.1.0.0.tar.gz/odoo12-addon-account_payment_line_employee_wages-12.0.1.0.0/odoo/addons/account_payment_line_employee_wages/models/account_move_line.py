from odoo import models, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def _prepare_payment_line_vals(self, payment_order):
        """
        When creating an account_payment_line, chose by default an employee's
        bank account if the selected partner is also an employee
        and the payment is part of a salary retribution.
        """
        vals = super()._prepare_payment_line_vals(payment_order)

        wage_account_group = self.env.ref("l10n_es.account_group_46")

        if payment_order.payment_type == "outbound" and (
            self.account_id.group_id == wage_account_group
            or self.account_id.group_id.parent_id == wage_account_group
        ):
            employee = self.env["hr.employee"].search(
                [("address_home_id", "=", self.partner_id.id)]
            )
            if employee and employee.bank_account_id:
                vals["partner_bank_id"] = employee.bank_account_id.id

        return vals

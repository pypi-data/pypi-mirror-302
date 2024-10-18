from odoo.tests.common import TransactionCase


class TestAccountMoveLine(TransactionCase):
    def setUp(self):
        super(TestAccountMoveLine, self).setUp()
        self.env.cr.execute(
            "ALTER TABLE account_account DROP CONSTRAINT IF EXISTS account_account_code_company_uniq"  # noqa
        )

        wage_account = self.env["account.account"].create(
            {
                "name": "Wage Account",
                "code": "460000",
                "user_type_id": self.env.ref("account.data_account_type_payable").id,
                "reconcile": True,
            }
        )
        counterpart_account = self.env["account.account"].create(
            {
                "name": "Compensation Account",
                "code": "570000",
                "user_type_id": self.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )
        self.employee_partner = self.env["res.partner"].create(
            {
                "name": "Employee Partner",
                "bank_ids": [
                    (
                        0,
                        0,
                        {
                            "acc_number": "ES9000246912501234567891",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "acc_number": "ES9000246912501234567892",
                        },
                    ),
                ],
            }
        )
        self.regular_partner = self.env["res.partner"].create(
            {
                "name": "Regular Partner",
                "bank_ids": [
                    (
                        0,
                        0,
                        {
                            "acc_number": "ES9000246912501234567893",
                        },
                    ),
                ],
            }
        )
        self.employee = self.env["hr.employee"].create(
            {
                "name": "Test Employee",
                "address_home_id": self.employee_partner.id,
                "bank_account_id": self.employee_partner.bank_ids[
                    1
                ].id,  # not the first one
            }
        )
        # Crear un payment order de tipus outbound
        self.payment_order = self.env["account.payment.order"].create(
            {
                "payment_type": "outbound",
                "payment_mode_id": self.env.ref(
                    "account_payment_mode.payment_mode_outbound_dd1"
                ).id,
            }
        )
        journal = self.env["account.journal"].create(
            {
                "name": "Test Journal",
                "code": "TEST",
                "type": "general",
            }
        )
        self.move = self.env["account.move"].create(
            {
                "name": "Test Move",
                "journal_id": journal.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": wage_account.id,
                            "partner_id": self.employee_partner.id,
                            "debit": 100.0,
                            "credit": 0.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "account_id": counterpart_account.id,
                            "partner_id": self.employee_partner.id,
                            "debit": 0.0,
                            "credit": 100.0,
                        },
                    ),
                ],
            }
        )

    def test_employee_partner_payment_line_vals(self):
        """
        Check that the output of _prepare_payment_line_vals
        has the expected partner_bank_id when the partner
        is an employee and the account_group is 'account_group_46'
        """
        move_line = self.move.line_ids[0]
        move_line.account_id.group_id = self.env.ref("l10n_es.account_group_46")

        vals = move_line._prepare_payment_line_vals(self.payment_order)

        self.assertEqual(vals["partner_id"], self.employee_partner.id)
        self.assertEqual(vals["partner_bank_id"], self.employee.bank_account_id.id)

    def test_employee_partner_payment_line_vals_child_account_group(self):
        """
        Check that the output of _prepare_payment_line_vals
        has the expected partner_bank_id when the partner
        is an employee and the account_group is a child of 'account_group_46'
        """
        move_line = self.move.line_ids[0]
        move_line.account_id.group_id = self.env.ref("l10n_es.account_group_465")

        vals = move_line._prepare_payment_line_vals(self.payment_order)

        self.assertEqual(vals["partner_id"], self.employee_partner.id)
        self.assertEqual(vals["partner_bank_id"], self.employee.bank_account_id.id)

    def test_employee_partner_payment_line_vals_other_account_group(self):
        """
        Check that the output of _prepare_payment_line_vals
        does not have the employee's partner_bank_id when
        the account group is not related to 'account_group_46'
        """
        move_line = self.move.line_ids[0]
        move_line.account_id.group_id = self.env.ref("l10n_es.account_group_145")
        vals = move_line._prepare_payment_line_vals(self.payment_order)

        self.assertEqual(vals["partner_id"], self.employee_partner.id)
        self.assertNotEqual(vals["partner_bank_id"], self.employee.bank_account_id.id)

    def test_regular_partner_payment_line_vals(self):
        """
        Check that the output of _prepare_payment_line_vals does not have the employee's
        partner_bank_id when the partner is not an employee
        """
        move_line = self.move.line_ids[0]
        move_line.account_id.group_id = self.env.ref("l10n_es.account_group_46")
        move_line.partner_id = self.regular_partner.id

        vals = move_line._prepare_payment_line_vals(self.payment_order)

        self.assertEqual(vals["partner_id"], self.regular_partner.id)
        self.assertNotEqual(vals["partner_bank_id"], self.employee.bank_account_id.id)

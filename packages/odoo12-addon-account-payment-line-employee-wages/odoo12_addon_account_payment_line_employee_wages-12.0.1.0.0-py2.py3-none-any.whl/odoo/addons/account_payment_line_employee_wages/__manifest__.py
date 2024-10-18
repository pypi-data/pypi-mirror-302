{
    "name": "SomItCoop Odoo Account Payment Line Employees Wage",
    "version": "12.0.1.0.0",
    "depends": [
        "account_payment_order",
        "contacts",
        "hr",
        "l10n_es",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Banking addons",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-accounting",
    "license": "AGPL-3",
    "summary": """
When creating an account_payment_line, chose by default an employee's bank account
if the selected partner is also an employee and the payment is part of its wage.
    """,
    "data": [],
    "application": False,
    "installable": True,
}

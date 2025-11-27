# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = [
        "account.move.line",
    ]

    rma_supplier_line_ids = fields.Many2many(
        comodel_name="rma_supplier_line",
        relation="rel_rma_supplier_line_2_aml",
        column1="account_move_line_id",
        column2="rma_line_id",
    )
    rma_customer_line_ids = fields.Many2many(
        comodel_name="rma_customer_line",
        relation="rel_rma_customer_line_2_aml",
        column1="account_move_line_id",
        column2="rma_line_id",
    )

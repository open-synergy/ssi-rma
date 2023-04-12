# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class RMAPolicy(models.Model):
    _name = "rma_policy"
    _description = "RMA Policy"
    _inherit = [
        "mixin.master_data"
    ]

    rma_type = fields.Selection(
        string="Applicable on RMA Type",
        selection=[
            ("customer", "Customer"),
            ("supplier", "Supplier"),
            ("both", "Both"),
        ],
        required=True,
        default="customer"
    )
    receipt_policy_ok = fields.Boolean(
        string="Available on Receipt Policy",
    )
    delivery_policy_ok = fields.Boolean(
        string="Available on Delivery Policy",
    )
    rma_supplier_policy_ok = fields.Boolean(
        string="Available on RMA to Supplier",
    )
    rule_ids = fields.One2many(
        comodel_name="rma_policy_rule",
        inverse_name="policy_id",
        string="Rules"
    )

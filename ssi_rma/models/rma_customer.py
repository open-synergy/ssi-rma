# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class RMACustomer(models.Model):
    _name = "rma_customer"
    _description = "RMA Customer"
    _inherit = [
        "rma_order_mixin"
    ]

    type = fields.Selection(
        string="Type",
        default="_default_type"
    )
    line_ids = fields.One2many(
        comodel_name="rma_customer_line",
        inverse_name="order_id",
    )

    @api.model
    def _default_type(self):
        value = "customer"
        return value

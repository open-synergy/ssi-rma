# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RMASupplierLine(models.Model):  # pylint: disable=R0903
    _name = "rma_supplier_line"
    _inherit = [
        "rma_line_mixin",
        "rma_supplier_line",
    ]

    purchase_line_id = fields.Many2one(
        related="source_stock_move_id.purchase_line_id",
        store=False,
    )

    def _get_receipt_procurement_data(self):
        _super = super()
        result = _super._get_receipt_procurement_data()
        purchase_line_id = self.purchase_line_id and self.purchase_line_id.id or False
        to_refund = purchase_line_id and True or False  # pylint: disable=R1706
        source_stock_move_id = (
            self.source_stock_move_id and self.source_stock_move_id.id or False
        )
        result.update(
            {
                "purchase_line_id": purchase_line_id,
                "to_refund": to_refund,
                "origin_returned_move_id": source_stock_move_id,
            }
        )
        return result

    def _get_delivery_procurement_data(self):
        _super = super()
        result = _super._get_delivery_procurement_data()
        purchase_line_id = self.purchase_line_id and self.purchase_line_id.id or False

        to_refund = purchase_line_id and True or False  # pylint: disable=R1706
        result.update(
            {
                "purchase_line_id": purchase_line_id,
                "to_refund": to_refund,
            }
        )
        return result

    def _prepare_refund_line(self, move):
        _super = super()
        result = _super._prepare_refund_line(move)
        purchase_line_id = self.purchase_line_id
        if purchase_line_id:
            result.update(
                {
                    "price_unit": purchase_line_id.price_unit,
                    "tax_ids": [(6, 0, purchase_line_id.taxes_id.ids)],
                }
            )
        return result

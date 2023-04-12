# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class RMALineMixin(models.AbstractModel):
    _name = "rma_line_mixin"
    _description = "RMA Line Mixin"
    _abstract = True
    _inherit = [
        "mixin.product_line_price",
    ]

    order_id = fields.Many2one(
        comodel_name="rma_order_mixin",
        string="RMA Order",
        required=True,
        ondelete="cascade"
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=10
    )
    lot_id = fields.Many2one(
        comodel_name="stock.production.lot",
        string="Lot"
    )
    stock_move_ids = fields.Many2many(
        comodel_name="stock.move",
        # relation="rel_rma_order_line_2_stock_move",
        column1="line_id",
        column2="move_id",
        string="Stock Moves"
    )
    qty_to_receive = fields.Float(
        string="Qty to Receive",
        compute="_compute_qty_to_receive",
        store=True
    )
    qty_incoming = fields.Float(
        string="Qty Incoming",
        compute="_compute_qty_incoming",
    )
    qty_received = fields.Float(
        string="Qty Received",
        compute="_compute_qty_received",
        store=True
    )
    qty_to_deliver = fields.Float(
        string="Qty to Deliver",
        compute="_compute_qty_to_deliver",
        store=True
    )
    qty_outgoing = fields.Float(
        string="Qty Outgoing",
        compute="_compute_qty_outgoing",
    )
    qty_delivered = fields.Float(
        string="Qty Delivered",
        compute="_compute_qty_delivered",
        store=True
    )

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
    )
    def _compute_qty_to_receive(self):
        for record in self:
            record.qty_to_receive = record._get_rma_move_qty(("draft","waiting","confirmed","partially_available","assigned"), "in")

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
    )
    def _compute_qty_incoming(self):
        for record in self:
            record.qty_to_receive = record._get_rma_move_qty(("draft","waiting","confirmed","partially_available","assigned"), "in")

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
    )
    def _compute_qty_received(self):
        for record in self:
            record.qty_to_receive = record._get_rma_move_qty(("done"), "in")

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
    )
    def _compute_qty_to_deliver(self):
        for record in self:
            record.qty_to_receive = record._get_rma_move_qty(("done"), "in")

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
    )
    def _compute_qty_outgoing(self):
        for record in self:
            record.qty_to_receive = record._get_rma_move_qty(("draft","waiting","confirmed","partially_available","assigned"), "out")

    @api.depends(
        "stock_move_ids",
        "stock_move_ids.state",
        "stock_move_ids.product_qty",
    )
    def _compute_qty_delivered(self):
        for record in self:
            record.qty_to_receive = record._get_rma_move_qty(("done"), "out")

    def _get_rma_move_qty(self, states, direction):
        for record in self:
            qty = 0.0

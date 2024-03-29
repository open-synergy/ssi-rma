# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class RMAMixin(models.AbstractModel):
    _name = "rma_order_mixin"
    _description = "RMA Mixin"
    _abstract = True
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_partner",
        "mixin.transaction_date_due",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "open_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_open",
        "dom_reject",
        "dom_done",
        "dom_terminate",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    type = fields.Selection(
        string="Type",
        selection=[
            ("customer", "Customer"),
            ("supplier", "Supplier"),
        ],
    )
    reason_id = fields.Many2one(
        comodel_name="rma_reason",
        string="Reason",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    operation_id = fields.Many2one(
        comodel_name="rma_operation",
        string="Operation",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    allowed_route_template_ids = fields.Many2many(
        related="operation_id.allowed_route_template_ids",
        string="Allowed Route Templates",
        store=False,
    )
    route_template_id = fields.Many2one(
        comodel_name="rma_route_template",
        string="Route Template",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    group_id = fields.Many2one(
        comodel_name="procurement.group",
        string="Procurement Group",
        ondelete="restrict",
        readonly=True,
    )
    line_ids = fields.One2many(
        comodel_name="rma_line_mixin",
        inverse_name="order_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    uom_quantity = fields.Float(
        string="UoM Quantity",
        compute="_compute_uom_quantity",
        store=True,
    )
    qty_to_receipt = fields.Float(
        string="Qty To Receipt",
        compute="_compute_qty_to_receipt",
        store=True,
    )
    qty_to_deliver = fields.Float(
        string="Qty To Deliver",
        compute="_compute_qty_to_deliver",
        store=True,
    )
    qty_received = fields.Float(
        string="Qty Received", compute="_compute_qty_received", store=True
    )
    qty_delivered = fields.Float(
        string="Qty Delivered", compute="_compute_qty_delivered", store=True
    )
    need_delivery = fields.Boolean(
        string="Need Delivery",
        compute="_compute_need_delivery",
        store=True,
    )
    percent_delivery = fields.Float(
        string="Percent Delivery",
        compute="_compute_percent_delivery",
        store=True,
    )
    need_reception = fields.Boolean(
        string="Need Reception",
        compute="_compute_need_reception",
        store=True,
    )
    percent_reception = fields.Float(
        string="Percent Reception",
        compute="_compute_percent_reception",
        store=True,
    )
    delivery_complete = fields.Boolean(
        string="Delivery Complete",
        compute="_compute_delivery_complete",
        store=True,
    )
    reception_complete = fields.Boolean(
        string="Reception Complete",
        compute="_compute_reception_complete",
        store=True,
    )
    receipt_ok = fields.Boolean(
        string="Receipt Ok",
        compute="_compute_receipt_ok",
        store=True,
    )
    deliver_ok = fields.Boolean(
        string="Deliver Ok",
        compute="_compute_deliver_ok",
        store=True,
    )
    resolve_ok = fields.Boolean(
        string="Resolve Ok",
        compute="_compute_resolve_ok",
        store=True,
    )

    @api.depends(
        "line_ids",
        "line_ids.delivery_complete",
    )
    def _compute_delivery_complete(self):
        for record in self:
            result = False
            if len(record.line_ids) > 0:
                if len(record.line_ids) == len(
                    record.line_ids.filtered(lambda r: r.delivery_complete)
                ):
                    result = True
            record.delivery_complete = result

    @api.depends(
        "line_ids",
        "line_ids.reception_complete",
    )
    def _compute_reception_complete(self):
        for record in self:
            result = False
            if len(record.line_ids) > 0:
                if len(record.line_ids) == len(
                    record.line_ids.filtered(lambda r: r.reception_complete)
                ):
                    result = True
            record.reception_complete = result

    @api.depends(
        "uom_quantity",
        "qty_delivered",
    )
    def _compute_percent_delivery(self):
        for record in self:
            result = 0.0
            try:
                result = record.qty_delivered / record.uom_quantity
            except ZeroDivisionError:
                result = 0.0
            record.percent_delivery = result

    @api.depends(
        "operation_id",
    )
    def _compute_need_delivery(self):
        for record in self:
            result = False
            if (
                record.operation_id
                and record.operation_id.delivery_policy_id
                and len(record.operation_id.delivery_policy_id.rule_ids) > 0
            ):
                result = True
            record.need_delivery = result

    @api.depends(
        "uom_quantity",
        "qty_received",
    )
    def _compute_percent_reception(self):
        for record in self:
            result = 0.0
            try:
                result = record.qty_received / record.uom_quantity
            except ZeroDivisionError:
                result = 0.0
            record.percent_reception = result

    @api.depends(
        "operation_id",
    )
    def _compute_need_reception(self):
        for record in self:
            result = False
            if (
                record.operation_id
                and record.operation_id.receipt_policy_id
                and len(record.operation_id.receipt_policy_id.rule_ids) > 0
            ):
                result = True
            record.need_reception = result

    def _get_resolve_ok_trigger(self):
        return [
            "delivery_complete",
            "reception_complete",
        ]

    @api.depends(lambda self: self._get_resolve_ok_trigger())
    def _compute_resolve_ok(self):
        for record in self:
            result = True
            for field_name in record._get_resolve_ok_trigger():
                if not getattr(record, field_name):
                    result = False
            record.resolve_ok = result

    @api.depends(
        "line_ids",
        "line_ids.uom_quantity",
    )
    def _compute_uom_quantity(self):
        for record in self:
            result = 0.0
            for line in record.line_ids:
                result = line.uom_quantity
            record.uom_quantity = result

    @api.depends(
        "line_ids",
        "line_ids.qty_received",
    )
    def _compute_qty_received(self):
        for record in self:
            result = 0.0
            for line in record.line_ids:
                result = line.qty_received
            record.qty_received = result

    @api.depends(
        "line_ids",
        "line_ids.qty_delivered",
    )
    def _compute_qty_delivered(self):
        for record in self:
            result = 0.0
            for line in record.line_ids:
                result = line.qty_delivered
            record.qty_delivered = result

    @api.depends(
        "line_ids",
        "line_ids.qty_to_receive",
    )
    def _compute_qty_to_receipt(self):
        for record in self:
            result = 0.0
            for line in record.line_ids:
                result = line.qty_to_receive
            record.qty_to_receipt = result

    @api.depends(
        "line_ids",
        "line_ids.qty_to_deliver",
    )
    def _compute_qty_to_deliver(self):
        for record in self:
            result = 0.0
            for line in record.line_ids:
                result = line.qty_to_deliver
            record.qty_to_deliver = result

    @api.depends(
        "qty_to_receipt",
        "state",
    )
    def _compute_receipt_ok(self):
        for record in self:
            result = False
            if record.qty_to_receipt > 0.0 and record.state == "open":
                result = True
            record.receipt_ok = result

    @api.depends(
        "qty_to_deliver",
        "state",
    )
    def _compute_deliver_ok(self):
        for record in self:
            result = False
            if record.qty_to_deliver > 0.0 and record.state == "open":
                result = True
            record.deliver_ok = result

    @api.onchange("operation_id")
    def onchange_route_template_id(self):
        self.route_template_id = False
        if self.operation_id:
            self.route_template_id = self.operation_id.default_route_template_id.id

    def action_create_reception(self):
        for record in self.sudo():
            record._create_reception()

    def action_create_delivery(self):
        for record in self.sudo():
            record._create_delivery()

    @ssi_decorator.post_open_action()
    def _create_procurement_group(self):
        self.ensure_one()

        if self.group_id:
            return True

        PG = self.env["procurement.group"]
        group = PG.create(self._prepare_create_procurement_group())
        self.write(
            {
                "group_id": group.id,
            }
        )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    def _create_reception(self):
        self.ensure_one()
        for detail in self.line_ids:
            detail._create_reception()

    def _create_delivery(self):
        self.ensure_one()
        for detail in self.line_ids:
            detail._create_delivery()

    def _prepare_create_procurement_group(self):
        self.ensure_one()
        return {
            "name": self.name,
            "partner_id": self.partner_id.id,
        }

    @api.model
    def _get_policy_field(self):
        res = super(RMAMixin, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "cancel_ok",
            "open_ok",
            "terminate_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

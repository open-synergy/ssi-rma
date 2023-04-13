# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class RMAMixin(models.AbstractModel):
    _name = "rma_order_mixin"
    _description = "RMA Mixin"
    _abstract = True
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.partner",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True

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
        "action_done",
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
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    duration_id = fields.Many2one(
        comodel_name="base.duration",
        string="Duration",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date_duration = fields.Date(
        string="Date",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    line_ids = fields.One2many(
        comodel_name="rma_line_mixin",
        inverse_name="order_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("terminate", "Terminated"),
            ("reject", "Reject"),
        ],
    )

    @api.model
    def _get_policy_field(self):
        res = super(RMAMixin, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "open_ok",
            "cancel_ok",
            "terminate_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange("operation_id")
    def onchange_route_template_id(self):
        self.route_template_id = False
        if self.operation_id:
            self.route_template_id = self.operation_id.default_route_template_id.id

# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "RMA",
    "version": "14.0.1.8.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_stock",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_terminate_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_transaction_partner_mixin",
        "ssi_transaction_date_due_mixin",
        "ssi_product_line_price_mixin",
        "ssi_partner_mixin",
        "base_automation",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/rma_customer_policy_template_data.xml",
        "data/rma_supplier_policy_template_data.xml",
        "data/rma_customer_approval_template_data.xml",
        "data/rma_supplier_approval_template_data.xml",
        "data/rma_policy_field_data.xml",
        "data/rma_policy_data.xml",
        "data/location_type_data.xml",
        "data/stock_picking_type_category_data.xml",
        "data/ir_actions_server_data.xml",
        "data/base_automation_data.xml",
        "menu.xml",
        "views/rma_mixin_view.xml",
        "views/rma_customer_view.xml",
        "views/rma_supplier_view.xml",
        "views/rma_operation.xml",
        "views/rma_policy_field_view.xml",
        "views/rma_policy_view.xml",
        "views/rma_reason_views.xml",
        "views/rma_route_template_view.xml",
        "views/customer_rma_in_views.xml",
        "views/customer_rma_out_views.xml",
        "views/supplier_rma_in_views.xml",
        "views/supplier_rma_out_views.xml",
    ],
    "demo": [
        "demo/stock_location_route_demo.xml",
        "demo/rma_route_template_demo.xml",
        "demo/rma_operation_demo.xml",
    ],
    "images": [],
}

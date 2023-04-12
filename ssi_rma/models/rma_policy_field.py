# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class RMAPolicyField(models.Model):
    _name = "rma_policy_field"
    _description = "RMA Policy Field"
    _inherit = [
        "mixin.master_data"
    ]

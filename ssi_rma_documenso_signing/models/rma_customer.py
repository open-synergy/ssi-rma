# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class RMACustomer(models.Model):
    _name = "rma_customer"
    _inherit = [
        "rma_customer",
        "mixin.documenso_signing",
    ]

    _documenso_signing_create_page = True

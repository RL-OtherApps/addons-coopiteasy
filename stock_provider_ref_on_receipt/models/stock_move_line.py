from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    provider_ref = fields.Char(
        string="Provider Reference", compute="_compute_product_code"
    )

    @api.multi
    def _compute_product_code(self):
        for line in self:
            product_supplier = self.env["product.supplierinfo"].search(
                [
                    (
                        "product_tmpl_id",
                        "=",
                        line.product_id.product_tmpl_id.id,
                    )
                ]
            )
            if product_supplier:
                line.provider_ref = product_supplier[0].product_code

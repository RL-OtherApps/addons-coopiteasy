# -*- coding: utf-8 -*-

from openerp import api, models


class StockRecomputeAfterMove(models.TransientModel):
    _name = "stock.recompute.after.move"

    @api.multi
    def recompute(self):
        self.ensure_one()
        stock_move_obj = self.env['stock.move']
        product_obj = self.env['product.product']

        products = product_obj.search([
                            ('finished_product', '=', True)
                            ])
        for product in products:
            moves = stock_move_obj.search([
                                ('state', '=', 'done'),
                                ('product_id', '=', product.id)
                               ], order="date asc")
            qty_after_move = 0
            print ("=========== product = " + product.name + " ============")
            for move in moves:
                if move.location_dest_id.usage in ['inventory', 'production', 'customer']:
                    qty = -move.product_qty
                elif move.location_id.usage in ['inventory', 'production', 'internal']:
                    qty = move.product_qty
                qty_after_move += qty
                print ("moved qty is " + str(qty) + " qty after move "
                       "is " + str(move.quantity_after_move) +
                       " instead of " + str(qty_after_move))
        return True

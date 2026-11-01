# -*- coding: utf-8 -*-
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _prepare_stock_move_vals(self, first_line, order_lines):
        vals = super()._prepare_stock_move_vals(first_line, order_lines)
        # sortie de stock sur le premier emplacement du produit (pas pour les retours)
        if self.location_id.usage == 'internal':
            location_id = [l.location_id.id for l in first_line.product_id.stock_quant_ids if l.location_id.location_id.name == 'Stock' and l.quantity > 0]
            if location_id:
                vals['location_id'] = location_id[0]
        return vals


class StockMove(models.Model):
    _inherit = 'stock.move'

    suggested_location_id = fields.Many2one('stock.location', string="Emplacement par défaut", compute="_compute_suggested_location")

    def _compute_suggested_location(self):
        for move in self:
            if move.picking_id and move.picking_id.location_dest_id:
                move.suggested_location_id = move.picking_id.location_dest_id._get_putaway_strategy(move.product_id)
            else:
                move.suggested_location_id = False

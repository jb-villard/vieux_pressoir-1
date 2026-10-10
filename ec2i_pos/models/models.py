# -*- coding: utf-8 -*-
from odoo import api,fields, models

from itertools import groupby

class StockPicking(models.Model):
    _inherit='stock.picking'
    
    def _prepare_stock_move_vals(self, first_line, order_lines):
        location_id = [l.location_id.id for l in first_line.product_id.stock_quant_ids if l.location_id.location_id.name == 'Stock' and l.quantity > 0]
        
        location = location_id and location_id[0] or self.location_id.id
        
        return {
            'name': first_line.name,
            'product_uom': first_line.product_id.uom_id.id,
            'picking_id': self.id,
            'picking_type_id': self.picking_type_id.id,
            'product_id': first_line.product_id.id,
            'product_uom_qty': abs(sum(order_lines.mapped('qty'))),
            'state': 'draft',
            #'location_id': self.location_id.id,
            'location_id': location,
            'location_dest_id': self.location_dest_id.id, #cc
            'company_id': self.company_id.id,
        }
    
class StockMove(models.Model):
    _inherit='stock.move'
    
    suggested_location_id = fields.Many2one('stock.location', string="Emplacement par défaut", compute="_compute_suggested_location")
    
    def _compute_suggested_location(self,):
        for move in self:
            if move.picking_id and move.picking_id.location_dest_id:
                move.suggested_location_id = move.picking_id.location_dest_id._get_putaway_strategy(move.product_id)
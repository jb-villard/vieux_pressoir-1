# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from collections import defaultdict

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    wk_display_stock = fields.Boolean('Display stock in POS', default=True)
    wk_stock_type = fields.Selection([('available_qty', 'Available Quantity(On hand)'), ('forecasted_qty', 'Forecasted Quantity'), ('virtual_qty', 'Quantity on Hand - Outgoing Qty')], string='Stock Type', default='available_qty')
    wk_continous_sale = fields.Boolean('Allow Order When Out-of-Stock')
    wk_deny_val = fields.Integer('Deny order when product stock is lower than ')
    wk_error_msg = fields.Char(string='Custom message', default="Product out of stock")
    wk_hide_out_of_stock = fields.Boolean(string="Hide Out of Stock products", default=True)

    def wk_pos_fetch_pos_stock(self, product_ids):
        """ Stock of the given product.product ids, as shown in the PoS.

        Only storable products are returned: the others have no stock to display
        and are never blocked nor hidden.

        :return: {product_id: {'qty': float, 'location': str}}
        """
        self.ensure_one()
        # PoS users are not inventory users
        self = self.sudo()
        location = self.picking_type_id.default_location_src_id
        products = self.env['product.product'].browse(product_ids).exists().filtered('is_storable')
        products = products.with_company(self.company_id).with_context(location=location.id)

        # Paid orders whose picking is only created when the session is closed
        # are not in the stock moves yet.
        pending_qty = dict(self.env['pos.order.line']._read_group(
            [
                ('product_id', 'in', products.ids),
                ('order_id.state', '=', 'paid'),
                ('order_id.picking_ids', '=', False),
                ('order_id.session_id.state', '!=', 'closed'),
                ('order_id.session_id.update_stock_at_closing', '=', True),
                ('order_id.config_id.picking_type_id', '=', self.picking_type_id.id),
            ],
            ['product_id'], ['qty:sum'],
        ))

        location_names = defaultdict(list)
        for product, quant_location in self.env['stock.quant']._read_group(
            [
                ('product_id', 'in', products.ids),
                ('company_id', '=', self.company_id.id),
                ('location_id.usage', '=', 'internal'),
                ('quantity', '>', 0),
            ],
            ['product_id', 'location_id'],
        ):
            location_names[product.id].append(quant_location.name)

        result = {}
        for product in products:
            if self.wk_stock_type == 'available_qty':
                qty = product.qty_available
            elif self.wk_stock_type == 'forecasted_qty':
                qty = product.virtual_available
            else:
                qty = product.qty_available - product.outgoing_qty
            result[product.id] = {
                'qty': qty - pending_qty.get(product, 0.0),
                'location': " + ".join(location_names[product.id]),
            }
        return result


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _compute_display_name(self):
        super()._compute_display_name()
        # x_volume_L is a Studio field, it only exists on the customer database
        if 'x_volume_L' not in self._fields:
            return
        for record in self:
            if record.x_volume_L and record.display_name:
                record.display_name = "%s [%s L]" % (record.display_name, record.x_volume_L)

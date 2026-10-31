# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_wk_display_stock = fields.Boolean(related='pos_config_id.wk_display_stock', readonly=False)
    pos_wk_stock_type = fields.Selection(related='pos_config_id.wk_stock_type', readonly=False)
    pos_wk_continous_sale = fields.Boolean(related='pos_config_id.wk_continous_sale', readonly=False)
    pos_wk_deny_val = fields.Integer(related='pos_config_id.wk_deny_val', readonly=False)
    pos_wk_error_msg = fields.Char(related='pos_config_id.wk_error_msg', readonly=False)
    pos_wk_hide_out_of_stock = fields.Boolean(related='pos_config_id.wk_hide_out_of_stock', readonly=False)

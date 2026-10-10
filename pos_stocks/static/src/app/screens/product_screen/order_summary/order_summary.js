/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";

patch(OrderSummary.prototype, {
    _setValue(val) {
        if (this.pos.numpadMode === "quantity" && val !== "remove") {
            let line = this.currentOrder.getSelectedOrderline();
            line = line?.combo_parent_id || line;
            const qty = parseFloat(val) || 0;
            if (line && qty > 0 && qty > line.qty) {
                const error = this.pos.wkStockError(line.product_id, qty, line);
                if (error) {
                    this.dialog.add(AlertDialog, error);
                    this.numberBuffer.reset();
                    return;
                }
            }
        }
        return super._setValue(...arguments);
    },
});

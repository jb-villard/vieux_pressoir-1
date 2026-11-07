import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/components/orderline/orderline";

patch(Orderline.prototype, {
    // Prix unitaire sous la ligne dès que la quantité n'est pas 1, comme sur le ticket.
    // Odoo 19 ne l'affiche à l'écran de vente que pour un prix modifié à la main.
    get lineScreenValues() {
        const vals = super.lineScreenValues;
        const line = this.line;
        if (
            !line.order_id ||
            vals.displayPriceUnit ||
            this.props.basic_receipt ||
            line.combo_parent_id ||
            line.qty === 1
        ) {
            return vals;
        }
        return {
            ...vals,
            displayPriceUnit: `${line.currencyDisplayPriceUnit} / ${line.product_id?.uom_id?.name || ""}`,
        };
    },
});

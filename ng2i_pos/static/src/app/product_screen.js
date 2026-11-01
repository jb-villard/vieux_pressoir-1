import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";

patch(ProductCard, {
    props: { ...ProductCard.props, priceLabel: { type: String, optional: true } },
});

patch(ProductScreen.prototype, {
    // Article sans image : pas d'image générique, la carte affiche le nom en entier
    getProductImage(product) {
        return product.image_128 ? super.getProductImage(product) : false;
    },
    // Prix de vente de la carte : même calcul que la commande en cours (liste de prix, position fiscale)
    getProductPriceLabel(product) {
        const details = product.getTaxDetails({
            overridedValues: {
                pricelist: this.currentOrder?.pricelist_id,
                fiscalPosition: this.currentOrder?.fiscal_position_id,
            },
        });
        const price =
            this.pos.config.iface_tax_included === "total"
                ? details.total_included
                : details.total_excluded;
        return this.env.utils.formatCurrency(price);
    },
});

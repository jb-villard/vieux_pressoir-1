import { patch } from "@web/core/utils/patch";
import { formatFloat } from "@web/core/utils/numbers";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";

// Volume en fin de désignation : « [0,75 L] », vide sans volume (x_volume_L, champ Studio).
// Espace insécable avant L : la valeur et l'unité ne sont pas coupées en fin de ligne.
export function litreSuffix(template) {
    const volume = template?.x_volume_L;
    return volume
        ? ` [${formatFloat(volume, { digits: [16, 3], trailingZeros: false })} L]`
        : "";
}

patch(ProductCard, {
    props: { ...ProductCard.props, priceLabel: { type: String, optional: true } },
});

patch(PosOrderline.prototype, {
    // Nom enregistré sur la ligne : ticket, commande et facture
    setFullProductName() {
        super.setFullProductName();
        this.full_product_name += litreSuffix(this.product_id?.product_tmpl_id);
    },
    // Nom de la ligne à l'écran de vente
    get orderDisplayProductName() {
        const display = super.orderDisplayProductName;
        const suffix = litreSuffix(this.product_id?.product_tmpl_id);
        return display.name ? { ...display, name: display.name + suffix } : display;
    },
});

patch(ProductScreen.prototype, {
    // Nom sur la carte produit
    getProductName(product) {
        return super.getProductName(product) + litreSuffix(product);
    },
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

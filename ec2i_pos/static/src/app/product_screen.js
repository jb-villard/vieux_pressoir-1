import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, {
    // Article sans image : pas d'image générique, la carte affiche le nom en entier
    getProductImage(product) {
        return product.image_128 ? super.getProductImage(product) : false;
    },
});

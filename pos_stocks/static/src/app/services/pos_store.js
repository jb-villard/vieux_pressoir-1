/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { ProductTemplate } from "@point_of_sale/app/models/product_template";

// The models have no access to the store
let posStore;

patch(ProductTemplate.prototype, {
    get canBeDisplayed() {
        const config = posStore?.config;
        if (config?.wk_display_stock && config.wk_hide_out_of_stock) {
            return super.canBeDisplayed && !posStore.wkIsOutOfStock(this);
        }
        return super.canBeDisplayed;
    },
});

patch(PosStore.prototype, {
    async setup() {
        posStore = this;
        // {product.product id: {qty, location}} as known by the server. Products
        // missing from it (services, non storable...) have no stock to follow.
        // Set before super: the server data is loaded during the setup.
        this.wkStock = {};
        await super.setup(...arguments);
    },

    async afterProcessServerData() {
        await super.afterProcessServerData(...arguments);
        await this.wkLoadStock();
    },

    async loadNewProducts() {
        const result = await super.loadNewProducts(...arguments);
        await this.wkLoadStock((result?.["product.product"] || []).map((product) => product.id));
        return result;
    },

    async postSyncAllOrders(orders) {
        await super.postSyncAllOrders(...arguments);
        const productIds = new Set();
        for (const order of orders || []) {
            if (order.finalized) {
                order.lines.forEach((line) => productIds.add(line.product_id?.id));
            }
        }
        if (productIds.size) {
            // The server has just moved the stock of those products
            this.wkLoadStock([...productIds]);
        }
    },

    async wkLoadStock(productIds) {
        if (!this.config.wk_display_stock) {
            return;
        }
        productIds = (
            productIds || this.models["product.product"].getAll().map((product) => product.id)
        ).filter((id) => typeof id === "number");
        if (!productIds.length) {
            return;
        }
        // Offline, the last known quantities are kept
        const stock = await this.data.silentCall("pos.config", "wk_pos_fetch_pos_stock", [
            [this.config.id],
            productIds,
        ]);
        if (stock) {
            this.wkStock = { ...this.wkStock, ...stock };
        }
    },

    /**
     * Quantity held by the orders the server stock does not include yet.
     */
    wkReservedQty(product, excludedLine) {
        let qty = 0;
        for (const order of this.models["pos.order"].getAll()) {
            if (order.state !== "draft" && !(order.state === "paid" && order.isUnsyncedPaid)) {
                continue;
            }
            for (const line of order.lines) {
                if (line.uuid !== excludedLine?.uuid && line.product_id?.id === product.id) {
                    qty += line.qty;
                }
            }
        }
        return qty;
    },

    /**
     * @returns {number|undefined} undefined when the stock of the product is not followed
     */
    wkAvailableQty(product, excludedLine) {
        const stock = this.wkStock[product.id];
        if (!stock) {
            return undefined;
        }
        return stock.qty - this.wkReservedQty(product, excludedLine);
    },

    wkTemplateQty(productTemplate) {
        let qty;
        for (const product of productTemplate.product_variant_ids) {
            const available = this.wkAvailableQty(product);
            if (available !== undefined) {
                qty = (qty || 0) + available;
            }
        }
        return qty;
    },

    wkTemplateQtyStr(productTemplate) {
        const qty = this.wkTemplateQty(productTemplate);
        return qty === undefined ? "" : this.env.utils.formatProductQty(qty, false);
    },

    wkTemplateLocation(productTemplate) {
        const locations = new Set();
        for (const product of productTemplate.product_variant_ids) {
            const location = this.wkStock[product.id]?.location;
            if (location) {
                location.split(" + ").forEach((name) => locations.add(name));
            }
        }
        return [...locations].join(" + ");
    },

    /**
     * Based on the server stock only: a product does not vanish from the screen
     * while its last units are in the cart.
     */
    wkIsOutOfStock(productTemplate) {
        let qty;
        for (const product of productTemplate.product_variant_ids) {
            const stock = this.wkStock[product.id];
            if (stock) {
                qty = (qty || 0) + stock.qty;
            }
        }
        return qty !== undefined && qty <= 0;
    },

    /**
     * @param {number} qty quantity wanted on the line (or of the new line)
     * @param {Object} [line] line being edited, not to be counted twice
     * @returns {false|{title: string, body: string}}
     */
    wkStockError(product, qty, line) {
        const config = this.config;
        if (!config.wk_display_stock || config.wk_continous_sale) {
            return false;
        }
        const available = this.wkAvailableQty(product, line);
        if (available === undefined || available - qty >= config.wk_deny_val) {
            return false;
        }
        return {
            title: _t("Warning !!!!"),
            body: `(${product.display_name})${config.wk_error_msg || ""}.`,
        };
    },

    async addLineToOrder(vals, order, opts = {}, configure = true) {
        const productTemplate =
            typeof vals.product_tmpl_id == "number"
                ? this.models["product.template"].get(vals.product_tmpl_id)
                : vals.product_tmpl_id;
        const variants = productTemplate?.product_variant_ids || [];
        // The variant is known for sure: refuse before any popup
        const product = vals.product_id || (variants.length === 1 && variants[0]);
        const qty = vals.qty ?? (order.preset_id?.is_return ? -1 : 1);
        if (product && typeof product === "object" && qty > 0) {
            const error = this.wkStockError(product, qty);
            if (error) {
                this.dialog.add(AlertDialog, error);
                return;
            }
        }
        const previousQty = new Map(order.lines.map((line) => [line.uuid, line.qty]));
        const line = await super.addLineToOrder(...arguments);
        // Variant picked in the configurator, weighed quantity...
        if (line && line.qty > 0 && line.qty > (previousQty.get(line.uuid) || 0)) {
            const error = this.wkStockError(line.product_id, line.qty, line);
            if (error) {
                if (previousQty.has(line.uuid)) {
                    line.setQuantity(previousQty.get(line.uuid));
                } else {
                    order.removeOrderline(line);
                }
                this.dialog.add(AlertDialog, error);
                return;
            }
        }
        return line;
    },

    get productsToDisplay() {
        // The stock is read through the models: keep the screen subscribed to it
        void this.wkStock;
        return super.productsToDisplay;
    },
});

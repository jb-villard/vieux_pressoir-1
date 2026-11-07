# -*- coding: utf-8 -*-
from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _ng2i_litre_label(self):
        """ Volume du produit pour la désignation : « 0,75 L », vide sans volume.

        x_volume_L (« Volume (L) ») est un champ Studio : il n'existe que dans la
        base du client. Espace insécable avant L, comme en caisse.
        """
        self.ensure_one()
        volume = self['x_volume_L'] if 'x_volume_L' in self._fields else 0.0
        if not volume:
            return ''
        decimal_point = self.env['res.lang']._get_data(code=self.env.lang or 'en_US').decimal_point or '.'
        return '%s L' % ('%.3f' % volume).rstrip('0').rstrip('.').replace('.', decimal_point)

    @api.model
    def _ng2i_load_cave_form_view(self):
        """ Fiche produit : millésime, volume et taux d'alcool sous le code-barres, comme en v14.

        Ce sont des champs Studio, présents seulement dans la base du client : la vue
        est créée ici plutôt qu'en XML pour que le module s'installe aussi sur une base
        vierge. Appelée à chaque installation et mise à jour (data/product_views.xml) ;
        sans ces champs, la vue n'est pas chargée et Odoo la retire en fin de mise à jour.
        """
        names = [name for name in ('x_millesime', 'x_volume_L', 'x_taux_alcool') if name in self._fields]
        if not names:
            return
        self.env['ir.ui.view']._load_records([{
            'xml_id': 'ng2i_pos.product_template_form_view_cave',
            'noupdate': False,
            'values': {
                'name': 'product.template.form.ng2i_pos.cave',
                'model': 'product.template',
                'inherit_id': self.env.ref('product.product_template_only_form_view').id,
                'arch': '<field name="barcode" position="after">%s</field>'
                        % ''.join('<field name="%s"/>' % name for name in names),
            },
        }], update=True)

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        if 'x_volume_L' in self._fields:
            fields.append('x_volume_L')
        return fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _compute_display_name(self):
        # Désignation suivie du volume, comme en v14 : « [REF] NOM [0,75 L] »
        super()._compute_display_name()
        for product in self:
            litre = product.product_tmpl_id._ng2i_litre_label()
            if litre and product.display_name:
                product.display_name = '%s [%s]' % (product.display_name, litre)

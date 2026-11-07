# -*- coding: utf-8 -*-


def migrate(cr, version):
    # La caisse garde produits et réglages dans le navigateur et ne recharge que
    # ce qui a changé : on force un rechargement complet pour qu'elle lise
    # x_volume_L (volume en fin de désignation). Effet à la prochaine ouverture
    # de la caisse depuis le backend.
    cr.execute("UPDATE pos_config SET last_data_change = now() AT TIME ZONE 'UTC'")

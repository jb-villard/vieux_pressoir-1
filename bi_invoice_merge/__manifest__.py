# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Merge Invoices(Customer Invoice/Vendor Bills) Odoo/OpenERP',
    'version': '14.0.0.1',
    'category': 'Accounting',
    'summary': 'Apps for merge invoices Merge customer invoices merge vendor bills merge supplier invoice merge invoice data invoice Merger customer invoice Merge vendor bill merge supplier invoice merge vendor bill merge invoice merge',
    'description': """
     merge invoices, merge data,
     Merge customer invoices, merge vendor bills, merge supplier invoice, merge invoice data,
    invoice Merge,
    customer invoice Merge,vendor bill merge, supplier invoice merge, invoice flow, invoice workflow, invoice setting
     مج الفواتير ودمج البيانات
     دمج فواتير العملاء ، دمج فواتير البائعين ، دمج فاتورة المورد ، دمج بيانات الفاتورة ،
    الفاتورة دمج ، ودمج الفاتورة
    فاتورة العميل دمج ، فواتير بائع دمج ، المورد دمج الفاتورة ، تدفق الفاتورة ، سير العمل الفاتورة ، إعداد الفاتورة
damj alfawatir wadamaj albayanat
     damaj fawatir aleumala' , damj fawatir albayiein , damj faturt almurid , damj bayanat alfatwrt ,
    alfatwrt damj , wadamaj alfatwr
    fatwrt aleamyl damj , fawatir bayie damj , almurid damj alfatwrt , tadafuq alfatwrt , sayr aleamal alfatwrt , 'iiedad alfatwr
    mesclar faturas, mesclar dados,
     Mesclar faturas de clientes, mesclar faturas de fornecedores, mesclar fatura de fornecedor, mesclar dados de faturas,
    Faturar fatura, mesclar fatura
    factura do cliente Fusão, factura do fornecedor, fusão da factura do fornecedor, fluxo da factura, fluxo de trabalho da factura, definição da factura
fusionar facturas, fusionar datos,
     Fusionar facturas de clientes, combinar facturas de proveedores, combinar facturas de proveedores, fusionar datos de facturas,
    factura fusionar, fusionar factura
    Combinación de factura de cliente, fusión de factura de proveedor, combinación de factura de proveedor, flujo de factura, flujo de trabajo de factura, configuración de factura

fusionner des factures, fusionner des données,
     Fusionner les factures des clients, fusionner les factures des fournisseurs, fusionner les factures des fournisseurs, fusionner les données des factures,
    Fusionner la facture, fusionner la facture
    fusion de facture client, fusion de factures fournisseur, fusion de factures fournisseur, flux de factures, workflow de facture, paramétrage de facture
Rechnungen zusammenführen, Daten zusammenführen,
     Kundenrechnungen zusammenführen, Lieferantenrechnungen zusammenführen, Lieferantenrechnung zusammenführen, Rechnungsdaten zusammenführen,
    Rechnung Zusammenführen, Rechnung zusammenführen
    Kundenrechnung Zusammenführen, Zusammenführen von Lieferantenrechnungen, Zusammenführen von Lieferantenrechnungen, Rechnungsfluss, Rechnungsworkflow, Rechnungseinstellung
""",
    'author': 'BrowseInfo',
    "price": 39,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.in',
    'depends': ['sale_management','account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/invoice_merge_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "images":["static/description/Banner.png"],
    'live_test_url': 'https://youtu.be/Ju36O2YzI2U',
}

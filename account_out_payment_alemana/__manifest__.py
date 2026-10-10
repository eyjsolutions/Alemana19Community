# -*- encoding: utf-8 -*-
{
	'name': 'Reporte Cobros',
	'category': 'Accounting',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['account_base_alemana','point_of_sale','popup_it'],
	'version': '1.0',
	'description':"""
	Reporte 
	""",
	'auto_install': True,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'wizards/account_out_payment_wizard.xml'],
	'installable': True,
	'license': 'LGPL-3'
}

# -*- encoding: utf-8 -*-
{
	'name': 'Account Base Alemana',
	'category': 'Accounting',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['company_branch_address','account_fields_it'],
	'version': '1.0',
	'description':"""
		Tabla tienda con cuentas
	""",
	'auto_install': True,
	'demo': [],
	"data": [    
		"security/ir.model.access.csv",        
        "views/account_local_alemana.xml"
        
    ],
	'installable': True,
	'license': 'LGPL-3'
}

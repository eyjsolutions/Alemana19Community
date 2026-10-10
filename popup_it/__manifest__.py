# -*- encoding: utf-8 -*-
{
	'name': 'Popup IT',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua, Sebastian Moises Loraico Lopez',
	'depends': ['base','web'],
	'version': '1.0',
	'description':"""
	Modulo para manejar mensajes de respuesta y documentos en reportes
	""",
	'auto_install': False,
	'demo': [],
	"data": [
		"security/security.xml",
        "security/ir.model.access.csv",        
        "views/popup_it.xml",
        "views/res_users_views.xml"
    ],
	'assets': {
		'web.assets_backend': [
			'popup_it/static/src/components/res_user_group_ids_field/*',
			'popup_it/static/src/components/popup_message_widget/*',
		],
	},
	'installable': True,
	'license': 'LGPL-3'
}

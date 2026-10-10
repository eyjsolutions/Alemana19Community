# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PopupIt(models.TransientModel):
	_name = 'popup.it'
	_description = 'POPUP IT'

	name = fields.Char()
	message = fields.Text(string='Resultado: ')
	output_name = fields.Char(string='Nombre del Archivo')
	output_file = fields.Binary(string='Archivo',readonly=True)
	
	def get_message(self,message):
		wizard = self.create({'name':'Mensaje','message':message})
		return {
			'res_id':wizard.id,
			'view_type':'form',
			'view_mode':'form',
			'res_model':'popup.it',
			'views':[[self.env.ref('popup_it.popup_it_form').id,'form']],
			'type':'ir.actions.act_window',
			'target':'new'
		}

	def get_file(self,output_name,output_file,visible=False):
		wizard = self.create({'output_name':output_name,'output_file':output_file})
		if visible:
			return {
				"type":"ir.actions.act_window",
				"res_model":"popup.it",
				"views":[[self.env.ref('popup_it.popup_file_it_form').id,"form"]],
				"res_id":wizard.id,
				"target":"new",
			}
		else:
			return {
				'type': 'ir.actions.act_url',
				'url': f"/web/content/?model={wizard._name}&id={wizard.id}&field=output_file&filename_field=output_name&download=true",
				'target': 'self',
			}
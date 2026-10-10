# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountLocalAlemana(models.Model):
	_name = 'account.local.alemana'
	_description = 'Account Local Alemana'

	@api.depends('company_branch_address_id')
	def compute_name(self):
		for i in self:
			i.name = i.company_branch_address_id.name
			
	name = fields.Char(string='Nombre',compute='compute_name')
	company_branch_address_id = fields.Many2one('res.company.branch.address',string='Tienda')
	account_id = fields.Many2one('account.account',string='Cuenta')
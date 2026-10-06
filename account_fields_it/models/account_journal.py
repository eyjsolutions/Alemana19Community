# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class AccountJournal(models.Model):
	_inherit = 'account.journal'

	register_sunat = fields.Selection([('1','Compras'),
								('2','Ventas'),
								('3','Honorarios'),
								('4','Retenciones'),
								('5','Percepciones'),
								('6','No Deducibles')],string='Registro Sunat')
	voucher_edit = fields.Boolean(string=u'Editar Número Asiento', default=False)
	check_surrender = fields.Boolean(string=u'Se usa para Rendiciones',default=False)
	check_retention = fields.Boolean(string=u'Se usa para Pagos Multiples',default=False)
	account_multipayment_id = fields.Many2one('account.account',string='Cuenta para PM',check_company=True)
	multipayment_precentage = fields.Float(string='Porcentaje PM',default=0)

	limit_amount = fields.Float(string=_('Limite Maximo'),copy =False,)

	partner_id = fields.Many2one(
		string=_('Encargado'),
		comodel_name='res.partner',
		domain="[('is_employee','=',True)]",
	)
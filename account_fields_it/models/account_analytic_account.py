# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountAnalyticAccount(models.Model):
	_inherit = 'account.analytic.account'

	a_debit = fields.Many2one('account.account',string='Amarre al Debe',check_company=True)
	a_credit = fields.Many2one('account.account',string='Amarre al Haber',check_company=True)

class AccountAnalyticPlan(models.Model):
	_inherit = 'account.analytic.plan'

	code = fields.Char(string=u'Código')
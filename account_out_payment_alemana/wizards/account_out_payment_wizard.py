# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
from io import BytesIO
from datetime import *
import base64
import subprocess
import sys

def install(package):
	subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
	import openpyxl
except:
	install('openpyxl==3.0.5')

class AccountOutPaymentWizard(models.TransientModel):
	_name = 'account.out.payment.wizard'
	_description = 'Account Out Payment Wizard'

	name = fields.Char()
	company_id = fields.Many2one('res.company',string=u'Compañia',required=True, default=lambda self: self.env.company,readonly=True)
	date_start = fields.Date(string='Fecha de Inicio')
	date_end = fields.Date(string='Fecha de Fin')
	
	def _get_sql(self):

		sql = """SELECT
			(pos_p.payment_date::timestamp - interval '5' hour)::date as date,
			lldt.code as td_sunat,
			am.nro_comp,
			rp.name as partner,
			ppm.name->>'es_PE' as metodo_pago,
			rcba.name as tienda,
			pos_p.amount
			from account_move am 
			LEFT JOIN pos_order pos on am.id = pos.account_move
			LEFT JOIN pos_payment pos_p on pos_p.pos_order_id = pos.id
			LEFT JOIN l10n_latam_document_type lldt ON lldt.id = am.l10n_latam_document_type_id
			LEFT JOIN res_partner rp ON rp.id = am.partner_id
			LEFT JOIN pos_payment_method ppm on ppm.id = pos_p.payment_method_id
			LEFT JOIN res_company_branch_address rcba on rcba.id = am.company_branch_address_id
			where am.state = 'posted' and am.move_type in ('out_invoice','out_refund')
			and ((pos_p.payment_date::timestamp - interval '5' hour)::date between '%s' and '%s') and am.company_id = %d
		""" % (self.date_from.strftime('%Y/%m/%d') if self.show_by == 'date' else self.period_from_id.date_start.strftime('%Y/%m/%d'),
			self.date_to.strftime('%Y/%m/%d') if self.show_by == 'date' else self.period_to_id.date_end.strftime('%Y/%m/%d'),
			self.company_id.id)
		return sql

	def get_report(self):
		ReportBase = self.env['report.base']
		workbook = ReportBase.get_excel_sql_export(self._get_sql(),self.get_header())
		return self.env['popup.it'].get_file('Libro Diario.xlsx',workbook)

	def get_header(self):
		HEADERS = ['FECHA PAGO','TD','NRO COMP','CLIENTE','METODO DE PAGO','CAJA(TIENDA)','MONTO']
		return HEADERS
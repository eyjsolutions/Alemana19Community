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

	def get_excel_sql_export(self,sql,header=None):
		self.env.cr.execute(sql)
		res = self.env.cr.fetchall()
		colnames = header
		if not colnames:
			colnames = [
				desc[0] for desc in self.env.cr.description
			]
		res.insert(0, colnames)

		wb = openpyxl.Workbook()
		ws = wb.active
		row_position = 1
		col_position = 1
		for index, row in enumerate(res, row_position):
			for col, val in enumerate(row, col_position):
				ws.cell(row=index, column=col).value = val
		output = BytesIO()
		wb.save(output)
		output.getvalue()
		output_datas = base64.b64encode(output.getvalue())
		output.close()
		return output_datas
	
	def _get_sql(self):

		sql = """SELECT
			(pos_p.payment_date::timestamp - interval '5' hour)::date as date,
			lldt.code as td_sunat,
			am.nro_comp,
			rp.name as partner,
			ppm.name->>'es_PE' as metodo_pago,
			rcba.name as tienda,
			pos_p.amount,
			(aa.code_store->>(%d)::character varying)::varchar  as cuenta
			from account_move am 
			LEFT JOIN pos_order pos on am.id = pos.account_move
			LEFT JOIN pos_payment pos_p on pos_p.pos_order_id = pos.id
			LEFT JOIN l10n_latam_document_type lldt ON lldt.id = am.l10n_latam_document_type_id
			LEFT JOIN res_partner rp ON rp.id = am.partner_id
			LEFT JOIN pos_payment_method ppm on ppm.id = pos_p.payment_method_id
			LEFT JOIN res_company_branch_address rcba on rcba.id = am.company_branch_address_id
			LEFT JOIN account_local_alemana ala on ala.company_branch_address_id = am.company_branch_address_id
			LEFT JOIN account_account aa on aa.id = ala.account_id
			where am.state = 'posted' and am.move_type in ('out_invoice','out_refund')
			and ((pos_p.payment_date::timestamp - interval '5' hour)::date between '%s' and '%s') and am.company_id = %d
		""" % (self.company_id.id,self.date_start.strftime('%Y/%m/%d'),
			self.date_end.strftime('%Y/%m/%d'),
			self.company_id.id)
		return sql

	def get_report(self):
		workbook = self.get_excel_sql_export(self._get_sql(),self.get_header())
		return self.env['popup.it'].get_file('Informe Cobros.xlsx',workbook)

	def get_header(self):
		HEADERS = ['FECHA PAGO','TD','NRO COMP','CLIENTE','METODO DE PAGO','CAJA(TIENDA)','MONTO','CUENTA']
		return HEADERS
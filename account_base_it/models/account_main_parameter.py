# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

####LEYENDA####
#nc = National Currency
#fc = Foreign Currency
#ed = Exchange Difference
#dt = Document Type
#wa = Without Address

class AccountMainParameter(models.Model):
	_name = 'account.main.parameter'
	_description = 'Account Main Parameter'

	name = fields.Char(default='Parametros Principales')
	use_bo = fields.Boolean(string='Permitir pagos de facturas en cuotas',default=True)
	company_id = fields.Many2one('res.company',string=u'Compañía',default=lambda self: self.env.company)

	####CUENTAS####
	
	customer_advance_account_nc = fields.Many2one('account.account',check_company=True,string=u'Cuenta Anticipo Cliente M.N.',domain="[('active', '=', True)]")
	customer_advance_account_fc = fields.Many2one('account.account',check_company=True,string=u'Cuenta Anticipo Cliente M.E.',domain="[('active', '=', True)]")
	supplier_advance_account_nc = fields.Many2one('account.account',check_company=True,string=u'Cuenta Anticipo Proveedor M.N.',domain="[('active', '=', True)]")
	supplier_advance_account_fc = fields.Many2one('account.account',check_company=True,string=u'Cuenta Anticipo Proveedor M.E.',domain="[('active', '=', True)]")
	detractions_account = fields.Many2one('account.account',check_company=True,string=u'Cuenta Detracciones Proveedor',domain="[('active', '=', True)]")
	customer_account_detractions = fields.Many2one('account.account',check_company=True,string=u'Cuenta Detracciones Clientes',domain="[('active', '=', True)]")
	free_transer_account_id = fields.Many2one('account.account',check_company=True,string=u'Cuenta Gasto Transferencias Gratuitas',domain="[('active', '=', True)]")
	rounding_gain_account = fields.Many2one('account.account',check_company=True,string=u'Cuenta Ganancia por Redondeo',domain="[('active', '=', True)]")
	rounding_loss_account = fields.Many2one('account.account',check_company=True,string=u'Cuenta Gasto por Redondeo',domain="[('active', '=', True)]")
	customer_letter_account_nc = fields.Many2one('account.account',check_company=True,string=u'Cuenta Letra por Cobrar M.N.',domain="[('active', '=', True)]")
	customer_letter_account_fc = fields.Many2one('account.account',check_company=True,string=u'Cuenta Letra por Cobrar M.E.',domain="[('active', '=', True)]")
	supplier_letter_account_nc = fields.Many2one('account.account',check_company=True,string=u'Cuenta Letra por Pagar M.N.',domain="[('active', '=', True)]")
	supplier_letter_account_fc = fields.Many2one('account.account',check_company=True,string=u'Cuenta Letra por Pagar M.E.',domain="[('active', '=', True)]")
	balance_sheet_account = fields.Many2one('account.account',check_company=True,string='Cuenta Utilidad Cierre',domain="[('active', '=', True)]")
	lost_sheet_account = fields.Many2one('account.account',check_company=True,string='Cuenta Perdida Cierre',domain="[('active', '=', True)]")
	lost_result_account = fields.Many2one('account.account',check_company=True,string='Cuenta Resultados Acumulados Perdida',domain="[('active', '=', True)]")
	profit_result_account = fields.Many2one('account.account',check_company=True,string='Cuenta Resultados Acumulados Utilidad',domain="[('active', '=', True)]")
	retention_account_id = fields.Many2one('account.account',check_company=True,string='Cuenta de Retenciones',domain="[('active', '=', True)]")

	####DIARIOS####
	
	detraction_journal = fields.Many2one('account.journal',string=u'Diario Detracciones')
	credit_journal = fields.Many2one('account.journal',string=u'Diario de Aplicaciones de Notas de Credito')
	destination_journal = fields.Many2one('account.journal',string=u'Diario Asientos Automaticos')
	free_transfer_journal_id = fields.Many2one('account.journal',string=u'Diario Transf. Gratuita')
	opening_close_journal_ids = fields.Many2many('account.journal',string=u'Diarios Apertura/Cierre')
	stock_journal_id = fields.Many2one('account.journal',string='Diario de Existencias')
	retention_bo_journal_id = fields.Many2one('account.journal',string='Diario de Comprobante de Retenciones')
	journal_financial_expense_id = fields.Many2one('account.journal',string='Diario de Reversiones Compras')

	####SUNAT####

	exportation_document = fields.Many2one('l10n_latam.document.type',string=u'Documento de Exportación (DUA)')
	proff_payment_wa = fields.Many2one('l10n_latam.document.type',string=u'Comprobante de Pago No Domiciliado')
	debit_note_wa = fields.Many2one('l10n_latam.document.type',string=u'Nota Debito No Domiciliado')
	credit_note_wa = fields.Many2one('l10n_latam.document.type',string=u'Nota Credito No Domiciliado')
	cancelation_partner = fields.Many2one('res.partner',string=u'Partner Documentos Anulados')
	cancelation_product = fields.Many2one('product.product',string=u'Producto para Anulaciones')
	advance_product = fields.Many2one('product.product',string=u'Producto para Anticipos')
	sale_ticket_partner = fields.Many2one('res.partner',string=u'Partner Boletas de Venta')
	dt_national_credit_note = fields.Many2one('l10n_latam.document.type',string=u'Nota de Crédito Nacional')
	dt_national_debit_note = fields.Many2one('l10n_latam.document.type',string=u'Nota de Débito Nacional')
	td_recibos_hon = fields.Many2one('l10n_latam.document.type',string=u'Recibo de Honorarios')
	free_transer_tax_ids = fields.Many2many('account.tax','free_transer_tax_main_parameter_rel','account_main_parameter_id','free_transer_tax_id',string=u'Impuestos Transf. Gratuita')
	cash_account_prefix = fields.Char(string=u'Prefijo Cuentas Caja',help=u'LOS PREFIJOS DEBEN SER DE TRES DÍGITOS Y DEBEN IR SEPARADOS POR COMA, ADEMÁS ENTRE COMILLA')
	bank_account_prefix = fields.Char(string=u'Prefijo Cuentas Banco',help=u'LOS PREFIJOS DEBEN SER DE TRES DÍGITOS Y DEBEN IR SEPARADOS POR COMA, ADEMÁS ENTRE COMILLA')
	tax_account = fields.Many2one('account.account.tag',string=u'Etiqueta para Percepciones')
	dt_perception = fields.Many2one('l10n_latam.document.type',string=u'Tipo de Documento Percepciones')
	retention_precentage = fields.Float(string='Porcentaje de Retenciones',default=0)
	others_document_type = fields.Many2one('l10n_latam.document.type',string=u'Tipo Documento Otros')
	retention_document_type = fields.Many2one('l10n_latam.document.type',string=u'Tipo Documento Retenciones')
	vario_partner_id = fields.Many2one('res.partner',string=u'Partner Varios')
	product_financial_expense_id = fields.Many2one('product.product',string='Gastos Financieros')

	####REPORTES####

	dir_create_file = fields.Char(string=u'Directorio para Reportes')
	fiscal_year_id = fields.Many2one('account.fiscal.year',string=u'Año Fiscal predeterminado')
	invoice_payment_term = fields.Many2one('account.payment.term', string='Terminos de Pago')
	
	####CONFIGURACIONES CONTABLES####

	exchange_difference = fields.Boolean(string='Diferencia de Cambio por Analisis Documento', default=False)
	payment_method_id = fields.Many2one(string='Metodo de Pago', comodel_name='account.payment.method')


	@api.constrains('company_id')
	def _check_unique_parameter(self):
		self.env.cr.execute("""select id from account_main_parameter where company_id = %d""" % (self.company_id.id))
		res = self.env.cr.dictfetchall()
		if len(res) > 1:
			raise UserError(u"Ya existen Parametros Principales para esta Compañía")


class AccountFiscalYearUit(models.Model):
	_name = 'account.fiscal.year.uit'
	_description = 'Account Fiscal Year UIT'

	name = fields.Char(default='UIT')
	fiscal_year_id = fields.Many2one('account.fiscal.year',string=u'Año Fiscal')
	uit = fields.Float(string=u'UIT',digits=(12,2))

	@api.constrains('fiscal_year_id')
	def _check_unique_fiscal_year_id(self):
		self.env.cr.execute("""select id from account_fiscal_year_uit where fiscal_year_id = %d""" % (self.fiscal_year_id.id))
		res = self.env.cr.dictfetchall()
		if len(res) > 1:
			raise UserError(u"Ya existe UIT para este año Fiscal")

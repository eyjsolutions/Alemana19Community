# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = 'product.category'


    property_stock_account_input_categ_id = fields.Many2one(
        string=_('Cuenta de entrada de existencias'),
        comodel_name='account.account',
        check_company=True,
        domain="[('active', '=', True)]"
    )

    property_stock_account_output_categ_id = fields.Many2one(
        string=_('Cuenta de salida de existencias'),
        comodel_name='account.account',
        check_company=True,
        domain="[('active', '=', True)]"
    )
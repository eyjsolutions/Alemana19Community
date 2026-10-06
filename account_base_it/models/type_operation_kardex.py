# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class TypeOperationKardex(models.Model):
    _name = 'type.operation.kardex'
    _description = 'TypeOperationKardex'

    name = fields.Char('Nombre')
    code = fields.Char('Código')

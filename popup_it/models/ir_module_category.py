# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class IrModuleCategory(models.Model):
    _inherit = 'ir.module.category'

    group_ids = fields.One2many(
        string=_('Grupos'),
        comodel_name='res.groups',
        inverse_name='category_id',
        copy=False,
    )
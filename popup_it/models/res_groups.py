# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResGroups(models.Model):
    _inherit = 'res.groups'


    @api.model
    @tools.ormcache(cache='groups')
    def _get_view_group_hierarchy(self):
        return {
            'groups': {
                group.id: {
                    'id': group.id,
                    'name': group.name,
                    'comment': group.comment,
                    'privilege_id': group.privilege_id.id,
                    'disjoint_ids': group.disjoint_ids.ids,
                    'implied_ids': group.implied_ids.ids,
                    'all_implied_ids': group.all_implied_ids.ids,
                    'all_implied_by_ids': group.all_implied_by_ids.ids,
                    'category_id': group.category_id.id,
                }
                for group in self.search([])
            },
            'privileges': {
                privilege.id: {
                    'id': privilege.id,
                    'name': privilege.name,
                    'category_id': privilege.category_id.id,
                    'description': privilege.description,
                    'placeholder': privilege.placeholder,
                    'group_ids': [group.id for group in privilege.group_ids.sorted(lambda g: (len(g.all_implied_ids & privilege.group_ids) if g.privilege_id else 0, g.sequence, g.id))]
                }
                for privilege in self.env['res.groups.privilege'].search([])
            },
            'categories': [
                {
                    'id': category.id,
                    'name': category.name,
                    'privilege_ids': category.privilege_ids.sorted(lambda p: p.sequence).filtered(lambda p: p.group_ids).ids,
                    'group_ids': category.group_ids.ids,
                } for category in self.env['ir.module.category'].search(['|', ('privilege_ids.group_ids', '!=', False), ('group_ids', '!=', False)])
            ]
        }

    category_id = fields.Many2one(
        string=('Categoria'),
        comodel_name='ir.module.category',
        copy=False,
    )
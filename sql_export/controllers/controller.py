from odoo import http
from odoo.http import request

class SqlExportController(http.Controller):

    @http.route('/sql_export/get_dynamic_fields', type='json', auth='user')
    def get_dynamic_fields(self, sql_export_id):
        
        export = request.env['sql.export'].browse(int(sql_export_id)).exists()
        if not export:
            return {'fields': []}
            
        fields_data = []
        
        for field in export.field_ids:
            field_info = {
                'name': field.name,
                'string': field.field_description,
                'ttype': field.ttype,
                'required': field.required,
                'relation': field.relation if field.ttype in ['many2one', 'many2many', 'one2many'] else False,
            }
            
            if field.ttype == 'selection' and field.selection:
                selection = field.selection
                if isinstance(selection, str):
                    try:
                        selection = eval(selection)
                    except:
                        selection = []
                field_info['selection'] = selection
                
            fields_data.append(field_info)
        
        return {'fields': fields_data}

    @http.route('/sql_export/get_field_options', type='json', auth='user')
    def get_field_options(self, field_name, ttype, relation=None, selection=None):
       
        try:
            if ttype == 'selection' and selection:
                
                options = []
                for key, value in selection:
                    options.append({'id': key, 'display_name': value})
                return {'options': options}
                
            elif ttype in ['many2one', 'many2many'] and relation:
                
                Model = request.env[relation]
                records = Model.search([], limit=100)  # Límite para no sobrecargar
                options = [{'id': rec.id, 'display_name': rec.display_name} for rec in records]
                return {'options': options}
                
            else:
                return {'options': []}
                
        except Exception as e:
            return {'options': [], 'error': str(e)}

    @http.route('/sql_export/execute_export', type='json', auth='user')
    def execute_export(self, sql_export_id, field_values):
        export = request.env['sql.export'].browse(int(sql_export_id)).exists()
        if not export:
            return {'success': False, 'error': 'Exportación no encontrada'}
        
        try:
            variable_dict = self._prepare_variables(export, field_values)
            
            method_name = f"{export.file_format}_get_data_from_query"
            if hasattr(export, method_name):
                data = getattr(export, method_name)(variable_dict)
            else:
                return {'success': False, 'error': f'Método {method_name} no encontrado'}
                
            extension = export._get_file_extension()
            
            return {
                'success': True,
                'file_name': f"{export.name}.{extension}",
                'file_data': data
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/sql_export/preview_sql', type='json', auth='user')
    def preview_sql(self, sql_export_id, field_values):
        export = request.env['sql.export'].browse(int(sql_export_id)).exists()
        if not export:
            return {'success': False, 'error': 'Exportación no encontrada'}
        
        try:
            variable_dict = self._prepare_variables(export, field_values)
            res = export._execute_sql_request(params=variable_dict)
            
            preview_lines = []
            for i, row in enumerate(res[:100]):
                preview_lines.append(f"Fila {i+1}: {row}")
            
            return {
                'success': True,
                'preview_data': "\n".join(preview_lines) if preview_lines else "No se encontraron resultados"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _prepare_variables(self, export, field_values):
        variable_dict = {}
        
        for field in export.field_ids:
            value = field_values.get(field.name)
            if field.ttype == "many2one" and value:
                variable_dict[field.name] = value
            elif field.ttype == "many2many" and value:
                variable_dict[field.name] = tuple(value)
            elif value is not None:
                variable_dict[field.name] = value
            else:
                variable_dict[field.name] = None
        
        if "%(company_id)s" in export.query:
            variable_dict["company_id"] = request.env.company.id
        if "%(user_id)s" in export.query:
            variable_dict["user_id"] = request.env.user.id
            
        return variable_dict
/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { rpc } from '@web/core/network/rpc';

export class SqlExportWizard extends Component {
    static template = "sql_export.SqlExportWizard";
    static components = { Dialog };
    
    setup() {
        this.rpc = rpc;
        this.notification = useService("notification");
        this.action = useService("action");
        
        this.state = useState({
            sqlExportId: this._getSqlExportId(),
            hasDynamicFields: false,
            dynamicFields: [],
            fieldValues: {},
            fileReady: false,
            fileName: "",
            fileData: null,
            exporting: false,
            // Nuevo estado para datos de búsqueda
            fieldDomainData: {}
        });
        
        this.onFieldChange = this.onFieldChange.bind(this);
        this.exportSql = this.exportSql.bind(this);
        this.previewSql = this.previewSql.bind(this);
        this.downloadFile = this.downloadFile.bind(this);
        this.loadFieldOptions = this.loadFieldOptions.bind(this);
        this.onMany2OneChange = this.onMany2OneChange.bind(this);
        this.onMany2ManyChange = this.onMany2ManyChange.bind(this);
        onWillStart(() => this.loadDynamicFields());
    }

     onMany2OneChange(fieldName, ev) {
        const value = ev.target.value ? parseInt(ev.target.value) : '';
        this.onFieldChange(fieldName, value);
    }
    
    onMany2ManyChange(fieldName, ev) {
        const selectedValues = Array.from(ev.target.selectedOptions).map(opt => parseInt(opt.value));
        this.onFieldChange(fieldName, selectedValues);
    }
    
    _getSqlExportId() {
        if (this.props.action?.params?.sqlExportId) {
            return this.props.action.params.sqlExportId;
        }
        if (this.props.params?.sqlExportId) {
            return this.props.params.sqlExportId;
        }
        if (this.props.sqlExportId) {
            return this.props.sqlExportId;
        }
        console.error("No se pudo encontrar sqlExportId. Estructura completa:", this.props);
        return null;
    }
    
    async loadDynamicFields() {
        if (!this.state.sqlExportId) {
            this.notification.add(
                "Error: No se encontró el ID de exportación SQL", 
                { type: 'danger' }
            );
            return;
        }
        
        try {
            const result = await this.rpc("/sql_export/get_dynamic_fields", {
                sql_export_id: this.state.sqlExportId
            });
            
            if (result.fields?.length > 0) {
                const validFields = result.fields.filter(field => field?.name);
                
                if (validFields.length > 0) {
                    this.state.hasDynamicFields = true;
                    this.state.dynamicFields = validFields;
                    
                    // Inicializar valores y cargar opciones para campos relacionales
                    for (const field of validFields) {
                        if (field.ttype === 'boolean') {
                            this.state.fieldValues[field.name] = false;
                        } else if (field.ttype === 'integer' || field.ttype === 'float') {
                            this.state.fieldValues[field.name] = 0;
                        } else if (field.ttype === 'many2many' || field.ttype === 'one2many') {
                            this.state.fieldValues[field.name] = [];
                        } else {
                            this.state.fieldValues[field.name] = '';
                        }
                        
                        // Cargar opciones para campos que lo necesitan
                        if (['many2one', 'many2many', 'one2many', 'selection', 'reference'].includes(field.ttype)) {
                            await this.loadFieldOptions(field);
                        }
                    }
                } else {
                    this.state.hasDynamicFields = false;
                }
            } else {
                this.state.hasDynamicFields = false;
            }
        } catch (error) {
            console.error("Error loading dynamic fields:", error);
            this.notification.add(
                "Error cargando campos dinámicos: " + error.message, 
                { type: 'danger' }
            );
            this.state.hasDynamicFields = false;
        }
    }
    
    async loadFieldOptions(field) {
        try {
            const result = await this.rpc("/sql_export/get_field_options", {
                field_name: field.name,
                ttype: field.ttype,
                relation: field.relation,
                selection: field.selection
            });
            
            this.state.fieldDomainData[field.name] = result.options || [];
        } catch (error) {
            console.error(`Error loading options for field ${field.name}:`, error);
            this.state.fieldDomainData[field.name] = [];
        }
    }
    
    onFieldChange(fieldName, value) {
        this.state.fieldValues[fieldName] = value;
    }
    
    // Resto del código se mantiene igual...
    async exportSql() {
        if (!this.state.sqlExportId) {
            this.notification.add("Error: No se encontró el ID de exportación SQL", { type: 'danger' });
            return;
        }
        
        if (this.state.hasDynamicFields) {
            for (const field of this.state.dynamicFields) {
                if (field.required && (!this.state.fieldValues[field.name] || this.state.fieldValues[field.name] === '')) {
                    this.notification.add(`El campo ${field.string} es requerido`, { type: 'danger' });
                    return;
                }
            }
        }
        
        this.state.exporting = true;
        
        try {
            const result = await this.rpc("/sql_export/execute_export", {
                sql_export_id: this.state.sqlExportId,
                field_values: this.state.fieldValues
            });
            
            if (result.success) {
                this.state.fileReady = true;
                this.state.fileName = result.file_name;
                this.state.fileData = result.file_data;
                this.notification.add("Exportación generada correctamente", { type: 'success' });
            } else {
                this.notification.add(result.error || "Error en la exportación", { type: 'danger' });
            }
        } catch (error) {
            console.error("Export error:", error);
            this.notification.add("Error ejecutando exportación: " + error.message, { type: 'danger' });
        } finally {
            this.state.exporting = false;
        }
    }
    
    async previewSql() {
        if (!this.state.sqlExportId) {
            this.notification.add("Error: No se encontró el ID de exportación SQL", { type: 'danger' });
            return;
        }
        
        if (this.state.hasDynamicFields) {
            for (const field of this.state.dynamicFields) {
                if (field.required && (!this.state.fieldValues[field.name] || this.state.fieldValues[field.name] === '')) {
                    this.notification.add(`El campo ${field.string} es requerido`, { type: 'danger' });
                    return;
                }
            }
        }
        
        try {
            const result = await this.rpc("/sql_export/preview_sql", {
                sql_export_id: this.state.sqlExportId,
                field_values: this.state.fieldValues
            });
            
            if (result.success) {
                this.notification.add(
                    `Previsualización (primeros 100 registros):\n${result.preview_data}`,
                    { 
                        type: 'info', 
                        sticky: true,
                        title: "Previsualización SQL"
                    }
                );
            } else {
                this.notification.add(result.error || "Error en previsualización", { type: 'danger' });
            }
        } catch (error) {
            console.error("Preview error:", error);
            this.notification.add("Error en previsualización: " + error.message, { type: 'danger' });
        }
    }
    
    downloadFile() {
        if (this.state.fileData) {
            const link = document.createElement('a');
            link.href = `data:application/octet-stream;base64,${this.state.fileData}`;
            link.download = this.state.fileName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

SqlExportWizard.props = {
    action: { type: Object, optional: true },
    params: { type: Object, optional: true },
    close: Function,
};
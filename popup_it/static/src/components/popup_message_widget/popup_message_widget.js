/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

/**
 * Widget estilizado para mostrar mensajes de éxito/error/info
 * con animaciones tipo Material Design
 */
class PopupMessageWidget extends Component {
    static template = "popup_it.PopupMessageWidget";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.state = useState({
            messageType: this.detectMessageType(this.props.record.data.message || ''),
        });
    }

    detectMessageType(message) {
        const lowerMessage = message.toLowerCase();
        if (lowerMessage.includes('error') || lowerMessage.includes('fallido') || 
            lowerMessage.includes('incorrecto') || lowerMessage.includes('problema')) {
            return 'error';
        } else if (lowerMessage.includes('éxito') || lowerMessage.includes('exitoso') || 
                   lowerMessage.includes('correcto') || lowerMessage.includes('completado') ||
                   lowerMessage.includes('success')) {
            return 'success';
        } else if (lowerMessage.includes('advertencia') || lowerMessage.includes('warning') ||
                   lowerMessage.includes('atención')) {
            return 'warning';
        }
        return 'info';
    }

    get messageType() {
        return this.state.messageType;
    }

    get icon() {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };
        return icons[this.messageType] || icons.info;
    }

    get title() {
        const titles = {
            success: '¡Éxito!',
            error: '¡Error!',
            warning: '¡Advertencia!',
            info: 'Información'
        };
        return titles[this.messageType] || titles.info;
    }

    get message() {
        return this.props.record.data.message || '';
    }
}

registry.category("fields").add("popup_message_widget", {
    component: PopupMessageWidget,
});

/**
 * Widget estilizado para mostrar archivos descargables
 */
class PopupFileWidget extends Component {
    static template = "popup_it.PopupFileWidget";
    static props = {
        ...standardFieldProps,
    };

    get fileName() {
        return this.props.record.data.output_name || 'archivo.txt';
    }

    get fileData() {
        return this.props.record.data.output_file;
    }

    get hasFile() {
        const data = this.props.record.data.output_file;
        return data && data.length > 0;
    }

    downloadFile() {
        if (!this.hasFile) {
            console.error('No hay archivo disponible para descargar');
            return;
        }

        const recordId = this.props.record.resId;
        const fieldName = 'output_file';
        const model = this.props.record.resModel;
        
        const downloadUrl = `/web/content?model=${model}&id=${recordId}&field=${fieldName}&filename_field=output_name&download=true`;
        
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = this.fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

registry.category("fields").add("popup_file_widget", {
    component: PopupFileWidget,
});
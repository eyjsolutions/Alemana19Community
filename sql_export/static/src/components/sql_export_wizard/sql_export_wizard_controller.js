/** @odoo-module **/

import { registry } from "@web/core/registry";
import { SqlExportWizard } from "./sql_export_wizard";

registry.category("actions").add("sql_export_wizard", SqlExportWizard);
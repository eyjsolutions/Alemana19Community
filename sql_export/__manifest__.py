# Copyright (C) 2015 Akretion (<http://www.akretion.com>)
# @author: Florian da Costa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "SQL Export",
    "author": "ITGRUPO, Sebastian Moises Loraico Lopez",
    "license": "AGPL-3",
    "category": "Generic Modules/Others",
    "summary": "Export data in csv file with SQL requests",
    "depends": [
        "sql_request_abstract",
        "spreadsheet_dashboard",
        "web"
    ],
    "data": [
        "security/sql_export_security.xml",
        "security/ir.model.access.csv",
        "views/sql_export_view.xml",
       
    
    ],
    "assets": {
        "web.assets_backend": [
            "sql_export/static/src/components/sql_export_wizard/sql_export_wizard.xml",
            "sql_export/static/src/components/sql_export_wizard/sql_export_wizard_controller.js",
            "sql_export/static/src/components/sql_export_wizard/sql_export_wizard.js",
           
        ],
    },
    "installable": True,
}

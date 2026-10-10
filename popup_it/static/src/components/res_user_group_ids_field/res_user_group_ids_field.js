import { _t } from "@web/core/l10n/translation";
import { x2ManyCommands } from "@web/core/orm_service";
import { registry } from "@web/core/registry";
import { deepCopy } from "@web/core/utils/objects";
import { parseXML } from "@web/core/utils/xml";
import { Record } from "@web/model/record";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { FormArchParser } from "@web/views/form/form_arch_parser";
import { FormRenderer } from "@web/views/form/form_renderer";

import { Component, onWillRender, toRaw, useChildSubEnv } from "@odoo/owl";

/**
 * Widget personalizado para visualizar grupos con categorías
 * Si un grupo tiene category_id pero NO tiene privilege_id, se muestra como checkbox
 * dentro de su categoría correspondiente.
 */
class CustomResUserGroupIdsField extends Component {
    static template = "popup_it.ResUserGroupIdsField";
    static components = { Record, FormRenderer };
    static props = { ...standardFieldProps };

    setup() {
        const { groups, privileges, categories } = toRaw(
            this.props.record.data.view_group_hierarchy
        );

        // Procesar grupos sin privilegios pero CON categoría
        const groupsWithCategoryNoPrivilege = Object.values(groups)           
            .filter((group) => !group.privilege_id && group.category_id)
            .reduce((acc, group) => {
                if (!acc[group.category_id]) {
                    acc[group.category_id] = [];
                }
                acc[group.category_id].push(group);
                return acc;
            }, {});
         console.log(groupsWithCategoryNoPrivilege);
        // Agregar estos grupos a sus categorías existentes como "checkboxGroups"
        for (const category of categories) {
            if (groupsWithCategoryNoPrivilege[category.id]) {
                category.checkboxGroups = groupsWithCategoryNoPrivilege[category.id]
                    .map((group) => ({
                        description: group.comment,
                        groupId: group.id,
                        id: "group_" + group.id,
                        name: group.name,
                    }))
                    .sort((g1, g2) => g1.name.localeCompare(g2.name));
            } else {
                category.checkboxGroups = [];
            }
        }

        // Generate the "other" category (for privileges that do not belong to any category)
        const privilegesWithoutCategory = Object.values(privileges)
            .filter((privilege) => !privilege.category_id)
            .sort((privilege) => privilege.sequence);
        
        if (privilegesWithoutCategory.length) {
            categories.push({
                id: "other",
                name: _t("Other"),
                privilege_ids: privilegesWithoutCategory.map((privilege) => privilege.id),
                checkboxGroups: [],
            });
        }

        // Generate the extra rights category (for groups without privilege AND without category)
        const extraGroups = Object.values(groups)
            .filter((group) => !group.privilege_id && !group.category_id);
        
        this.extraCategory = extraGroups.length ? {
            id: "extra",
            name: _t("Extra Rights"),
            privileges: extraGroups
                .map((group) => {
                    const privilege = {
                        description: group.comment,
                        groupId: group.id,
                        id: "group_" + group.id,
                        name: group.name,
                    };
                    privilege.groupFieldName = this.getFieldName(privilege);
                    return privilege;
                })
                .sort((p1, p2) => p1.name.localeCompare(p2.name)),
        } : null;

        // Generate selection (for privileges) and boolean (for checkbox groups and extra rights) fields
        this._fields = {};
        const booleanFieldToGroupId = {};
        
        for (const category of categories) {
            category.privileges = [];
            
            // Procesar privilegios normales (selection fields)
            for (const privilegeId of category.privilege_ids) {
                const privilege = privileges[privilegeId];
                category.privileges.push(privilege);
                const helpLines = privilege.description ? [privilege.description] : [];
                for (const gid of privilege.group_ids) {
                    if (groups[gid].comment) {
                        helpLines.push(`- ${groups[gid].name}: ${groups[gid].comment}`);
                    }
                }
                this._fields[this.getFieldName(privilege)] = {
                    help: helpLines.join("\n"),
                    selection: privilege.group_ids.map((gId) => [gId, groups[gId].name]),
                    string: privilege.name,
                    type: "selection",
                };
            }

            // Procesar grupos checkbox de esta categoría
            for (const checkboxGroup of category.checkboxGroups) {
                checkboxGroup.groupFieldName = this.getFieldName(checkboxGroup);
                this._fields[checkboxGroup.groupFieldName] = {
                    help: checkboxGroup.description,
                    string: checkboxGroup.name,
                    type: "boolean",
                };
                booleanFieldToGroupId[checkboxGroup.groupFieldName] = checkboxGroup.groupId;
            }
        }

        // Procesar extra rights
        if (this.extraCategory) {
            for (const privilege of this.extraCategory.privileges) {
                this._fields[privilege.groupFieldName] = {
                    help: privilege.description,
                    string: privilege.name,
                    type: "boolean",
                };
                booleanFieldToGroupId[privilege.groupFieldName] = privilege.groupId;
            }
        }

        this.fields = deepCopy(this._fields);

        // Generate archInfo to provide to the FormRenderer
        const models = { main: { fields: this._fields } };
        const arch = `
            <t>
                <group>
                    ${categories.map((category) => this.getCategoryArch(category)).join("")}
                </group>
                ${odoo.debug && this.extraCategory ? this.getExtraGroupsArch() : ""}
            </t>`;
        this.archInfo = new FormArchParser().parse(parseXML(arch), models, "main");

        this.info = {
            booleanFieldToGroupId,
            groups: {},
            privileges,
        };
        
        useChildSubEnv({
            resUserGroupsInfo: this.info,
        });

        onWillRender(() => {
            const selectedIds = new Set(this.props.record.data[this.props.name].currentIds);
            
            for (const group of Object.values(groups)) {
                const selected = selectedIds.has(group.id);
                this.info.groups[group.id] = {
                    name: group.name,
                    id: group.id,
                    privilege_id: group.privilege_id,
                    comment: group.comment,
                    impliedByIds: group.all_implied_by_ids.filter(
                        (gid) => gid !== group.id && selectedIds.has(gid)
                    ),
                    implyIds: selected
                        ? group.all_implied_ids.filter((gid) => gid !== group.id)
                        : [],
                    selected,
                };
            }
            
            for (const group of Object.values(groups)) {
                let disjointIds = [];
                const { selected, impliedByIds } = this.info.groups[group.id];
                if (selected || impliedByIds.length) {
                    disjointIds = group.disjoint_ids.filter(
                        (gid) =>
                            this.info.groups[gid].selected ||
                            this.info.groups[gid].impliedByIds.length
                    );
                }
                this.info.groups[group.id].disjointIds = disjointIds;
            }

            // Remove lower level groups from selection fields where a higher level group is implied
            for (const fieldName in this.fields) {
                if (this.fields[fieldName].type === "selection") {
                    const options = this._fields[fieldName].selection;
                    this.fields[fieldName].selection = options;
                    for (let i = options.length - 1; i > 0; i--) {
                        const group = this.info.groups[options[i][0]];
                        const isImplied = group.impliedByIds.some(
                            (gid) => this.info.groups[gid].privilege_id !== group.privilege_id
                        );
                        if (isImplied) {
                            this.fields[fieldName].selection = options.slice(i);
                            break;
                        }
                    }
                }
            }

            // Generate values for the dynamically generated selection and boolean fields
            this.values = {};
            this.shadowedGroupIds = [];
            
            // Valores para selection fields (privilegios)
            for (const category of categories) {
                for (const privilege of category.privileges) {
                    let groupId =
                        privilege.group_ids.findLast((gId) => selectedIds.has(gId)) || false;
                    const fieldName = this.getFieldName(privilege);
                    const options = this.fields[fieldName].selection;
                    if (groupId && !options.some((option) => option[0] === groupId)) {
                        this.shadowedGroupIds.push(groupId);
                        groupId = false;
                    }
                    this.values[fieldName] = groupId;
                }

                // Valores para checkbox groups de la categoría
                for (const checkboxGroup of category.checkboxGroups) {
                    this.values[checkboxGroup.groupFieldName] = selectedIds.has(checkboxGroup.groupId);
                }
            }
            
            // Valores para extra rights
            if (this.extraCategory) {
                for (const privilege of this.extraCategory.privileges) {
                    this.values[privilege.groupFieldName] = selectedIds.has(privilege.groupId);
                }
            }
        });

        this.hooks = {
            onRecordChanged: this.onRecordChanged.bind(this),
        };
    }

    getExtraGroupsArch() {
        return `
            <group string="${this.extraCategory.name}" class="o_extra_rights_group">
                <group>
                    ${this.extraCategory.privileges
                        .filter((cat, index) => index % 2 === 0)
                        .map((privilege) => this.getPrivilegeArch(privilege))
                        .join("")}
                </group>
                <group>
                    ${this.extraCategory.privileges
                        .filter((cat, index) => index % 2 === 1)
                        .map((privilege) => this.getPrivilegeArch(privilege))
                        .join("")}
                </group>
            </group>`;
    }

    getFieldName(privilege) {
        return `field_${privilege.id}`;
    }

    getPrivilegeArch(privilege) {
        const fieldName = this.getFieldName(privilege);
        return `<field name="${fieldName}" widget="res_user_group_ids_privilege"/>`;
    }

    getCategoryArch(category) {
        const privilegesArch = category.privileges
            .map((privilege) => this.getPrivilegeArch(privilege))
            .join("");
        
        const checkboxGroupsArch = category.checkboxGroups
            .map((checkboxGroup) => this.getPrivilegeArch(checkboxGroup))
            .join("");

        return `
            <group string="${category.name}">
                ${privilegesArch}
                ${checkboxGroupsArch}
            </group>`;
    }

    onRecordChanged(_, values) {
        let selectedGroupIds = Object.entries(values)
            .filter(([fieldName, gid]) => this.fields[fieldName].type === "selection" && gid)
            .map(([_, gid]) => gid);
        
        // Keep shadowed groups
        const { groups, privileges } = this.info;
        const shadowedGroupIds = this.shadowedGroupIds.filter(
            (gid) => !values[this.getFieldName(privileges[groups[gid].privilege_id])]
        );
        selectedGroupIds = selectedGroupIds.concat(shadowedGroupIds);
        
        // Add checkbox groups (both in categories and extra rights)
        for (const [fieldName, value] of Object.entries(values)) {
            if (this.fields[fieldName]?.type === "boolean" && value) {
                const groupId = this.info.booleanFieldToGroupId[fieldName];
                if (groupId) {
                    selectedGroupIds.push(groupId);
                }
            }
        }
        
        return this.props.record.update({
            [this.props.name]: [x2ManyCommands.set(selectedGroupIds)],
        });
    }
}

const customResUserGroupIdsField = {
    component: CustomResUserGroupIdsField,
    fieldDependencies: [{ name: "view_group_hierarchy", type: "json", readonly: true }],
    additionalClasses: ["w-100"],
};

registry.category("fields").add("custom_res_user_group_ids", customResUserGroupIdsField);
-- SE EJECUTA MANUALMENTE --

INSERT INTO account_account_tag (
    name,
    applicability,
    active,
    country_id,
    record_shop,
    record_sale,
    record_fees,
    sequence
)
VALUES
    ('{"en_US":"BASE1","es_PE":"BASE1","es_419":"BASE1"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), '1',  NULL, NULL,  1),
    ('{"en_US":"BASE2","es_PE":"BASE2","es_419":"BASE2"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), '2',  NULL, NULL,  2),
    ('{"en_US":"BASE3","es_PE":"BASE3","es_419":"BASE3"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), '3',  NULL, NULL,  3),
    ('{"en_US":"CNG","es_PE":"CNG","es_419":"CNG"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), '4',  NULL, NULL,  4),
    ('{"en_US":"ISC-C","es_PE":"ISC-C","es_419":"ISC-C"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), '5',  NULL, NULL,  5),
    ('{"en_US":"OTROS-C","es_PE":"OTROS-C","es_419":"OTROS-C"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), '6',  NULL, NULL,  6),
    ('{"en_US":"IGV1","es_PE":"IGV1","es_419":"IGV1"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), '7',  NULL, NULL,  7),
    ('{"en_US":"IGV2","es_PE":"IGV2","es_419":"IGV2"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), '8',  NULL, NULL,  8),
    ('{"en_US":"IGV3","es_PE":"IGV3","es_419":"IGV3"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), '9',  NULL, NULL,  9),
    ('{"en_US":"EXP","es_PE":"EXP","es_419":"EXP"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), NULL, '1',  NULL, 10),
    ('{"en_US":"VENTA-G","es_PE":"VENTA-G","es_419":"VENTA-G"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), NULL, '2',  NULL, 11),
    ('{"en_US":"INAF","es_PE":"INAF","es_419":"INAF"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), NULL, '3',  NULL, 12),
    ('{"en_US":"EXO","es_PE":"EXO","es_419":"EXO"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), NULL, '4',  NULL, 13),
    ('{"en_US":"ISC-V","es_PE":"ISC-V","es_419":"ISC-V"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), NULL, '5',  NULL, 14),
    ('{"en_US":"OTROS-V","es_PE":"OTROS-V","es_419":"OTROS-V"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), NULL, '6',  NULL, 15),
    ('{"en_US":"IGV-V","es_PE":"IGV-V","es_419":"IGV-V"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), NULL, '7',  NULL, 16),
    ('{"en_US":"RENTA 4TA","es_PE":"RENTA 4TA","es_419":"RENTA 4TA"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), NULL, NULL, '1', 17),
    ('{"en_US":"RET 4TA","es_PE":"RET 4TA","es_419":"RET 4TA"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), NULL, NULL, '2', 18),
    ('{"en_US":"PER-C","es_PE":"PER-C","es_419":"PER-C"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), NULL, NULL, NULL, 19),
    ('{"en_US":"ICBPER-C","es_PE":"ICBPER-C","es_419":"ICBPER-C"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), '10', NULL, NULL, 20),
    ('{"en_US":"ICBPER-V","es_PE":"ICBPER-V","es_419":"ICBPER-V"}'::jsonb, 'taxes', TRUE, (SELECT rp.country_id FROM res_company rc LEFT JOIN res_partner rp ON rp.id = rc.partner_id LIMIT 1), NULL, '8',  NULL, 21);

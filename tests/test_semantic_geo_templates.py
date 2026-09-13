from geo.templates.template_registry import TEMPLATES, TemplateId, get_template, validate_template


def test_all_seven_templates_are_registered():
    assert set(TEMPLATES) == set(TemplateId)
    assert len(TEMPLATES) == 7


def test_all_templates_require_continuous_camera_truth_lock_and_geo_qa():
    for template in TEMPLATES.values():
        validate_template(template)
        assert template.requires_continuous_camera is True
        assert template.requires_truth_lock is True
        assert template.requires_geo_qa is True
        assert template.requires_verified_geo_anchor is True


def test_disputed_border_enables_disputed_territory_gate():
    template = get_template(TemplateId.DISPUTED_BORDER)
    assert template.disputed_territory_gate is True
    assert "disputed_geometry" in template.required_geo_relations


def test_military_base_reveal_requires_military_truth_lock():
    template = get_template(TemplateId.MILITARY_BASE_REVEAL)
    assert template.military_event_truth_lock is True
    assert "verified_site_anchor" in template.required_geo_relations


def test_submarine_cable_requires_both_landing_points_and_route():
    template = get_template(TemplateId.SUBMARINE_CABLE_ROUTE)
    assert {"landing_point_a", "route", "landing_point_b"}.issubset(template.required_geo_relations)


def test_resource_corridor_uses_relation_motion():
    template = get_template(TemplateId.RESOURCE_CORRIDOR)
    assert "RELATION_MOTION" in template.preferred_motion_families


def test_strait_reveal_is_context_to_target_motion():
    template = get_template(TemplateId.STRAIT_REVEAL)
    assert template.preferred_motion_families[:2] == ("CONTEXTUAL_REVEAL", "TARGET_MOTION")


def test_templates_do_not_encode_unsupported_claims():
    for template in TEMPLATES.values():
        text = template.purpose.lower()
        assert "prove" not in text
        assert "attack" not in text
        assert "surround" not in text

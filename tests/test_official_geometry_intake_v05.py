from pathlib import Path


def read_text(path: str) -> str:
    return (Path(__file__).parents[1] / path).read_text(encoding="utf-8")


def test_all_four_official_sources_are_selected():
    text = read_text("geo/asset_registry/official_geometry_intake_v05.yaml")
    assert "authority: IBGE" in text
    assert "authority: IGAC" in text
    assert "authority: Instituto Geografico Nacional / IDEP" in text
    assert "authority: Instituto Geografico Militar" in text
    assert text.count("geometry_loaded: false") == 4


def test_bundle_stays_blocked_until_hashes_and_geometry_are_loaded():
    text = read_text("geo/asset_registry/official_geometry_intake_v05.yaml")
    assert "status: BLOCK" in text
    assert "pre_render_geo_truth: BLOCK" in text
    assert "publication_ready: false" in text
    assert text.count("raw_file_sha256: null") == 4
    assert text.count("normalized_geometry_sha256: null") == 4


def test_colombia_uses_official_polygon_source_not_restricted_border_line():
    text = read_text("geo/asset_registry/official_geometry_intake_v05.yaml")
    assert "OFFICIAL_POLYGON_SOURCE_SELECTED" in text
    assert "dissolving the official department polygons" in text


def test_ecuador_uses_igm_official_vector_source():
    text = read_text("geo/asset_registry/official_geometry_intake_v05.yaml")
    assert "selected_layer: Limite Internacional" in text
    assert "source_format: KML" in text
    assert "Instituto Geografico Militar" in text

import pytest

from sensor_fault_detection.settings import Settings


def test_api_registers_safe_routes():
    pytest.importorskip("fastapi")
    from sensor_fault_detection.api import create_app

    app = create_app(Settings())
    paths = {route.path for route in app.routes}
    assert {"/health", "/train", "/predict"} <= paths

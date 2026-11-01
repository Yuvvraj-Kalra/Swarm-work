"""Unit tests for the pure status/warning logic (run with: colcon test)."""
from drone_monitoring.telemetry_monitor import evaluate_status
from drone_monitoring.warning_publisher import build_warnings


def test_normal():
    assert evaluate_status(12.0, 80.0, 40.0) == 'NORMAL'


def test_waiting():
    assert evaluate_status(None, 80.0, 40.0) == 'WAITING FOR SENSOR DATA'


def test_single_conditions():
    assert evaluate_status(12.0, 15.0, 40.0) == 'LOW BATTERY'
    assert evaluate_status(12.0, 80.0, 65.0) == 'OVERHEATING'
    assert evaluate_status(35.0, 80.0, 40.0) == 'ALTITUDE LIMIT EXCEEDED'


def test_multiple_conditions():
    assert evaluate_status(12.0, 15.0, 65.0) == 'LOW BATTERY, OVERHEATING'


def test_warnings():
    assert build_warnings('NORMAL') == ['No active warnings']
    assert build_warnings('WAITING FOR SENSOR DATA') == ['Waiting for telemetry']
    assert len(build_warnings('LOW BATTERY, OVERHEATING')) == 2

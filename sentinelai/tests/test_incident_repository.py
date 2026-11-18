from sentinelai.models.incident import Finding, IncidentReport, Severity
from sentinelai.repositories.incident_repository import IncidentRepository


def test_save_and_read(tmp_path):
    repository = IncidentRepository(tmp_path / 'test.sqlite3')
    report = IncidentReport(
        scenario_id='INC-001',
        title='Intentos de inicio de sesión sospechosos',
        summary='Se detectó una secuencia de autenticaciones fallidas y una exitosa.',
        severity=Severity.HIGH,
        confidence=0.85,
        findings=[Finding(description='Cinco intentos fallidos consecutivos', event_ids=['EVT-001'])],
        recommendations=['Revisar sesiones administrativas'],
    )
    saved_id = repository.save(report)
    restored = repository.get(saved_id)
    assert restored == report
    assert len(repository.list_by_scenario('INC-001')) == 1

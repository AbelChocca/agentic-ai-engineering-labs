import sqlite3
from contextlib import closing
from uuid import UUID

from sentinelai.config.settings import get_settings
from sentinelai.models.incident import IncidentReport


class IncidentRepository:
    def __init__(self, db_path=None):
        self.db_path = db_path or get_settings().database_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_database(self):
        with closing(self._connect()) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS incident_reports (
                    id TEXT PRIMARY KEY,
                    scenario_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    status TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_incidents_scenario
                ON incident_reports(scenario_id, created_at)
            ''')
            conn.commit()

    def save(self, report: IncidentReport) -> UUID:
        with closing(self._connect()) as conn:
            conn.execute('''
                INSERT INTO incident_reports (
                    id, scenario_id, title, severity, status,
                    confidence, created_at, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(report.id), report.scenario_id, report.title,
                report.severity.value, report.status.value,
                report.confidence, report.created_at.isoformat(),
                report.model_dump_json(),
            ))
            conn.commit()
        return report.id

    def get(self, report_id: str | UUID) -> IncidentReport | None:
        with closing(self._connect()) as conn:
            row = conn.execute(
                'SELECT payload_json FROM incident_reports WHERE id = ?',
                (str(report_id),),
            ).fetchone()
        return IncidentReport.model_validate_json(row['payload_json']) if row else None

    def list_by_scenario(self, scenario_id: str) -> list[IncidentReport]:
        with closing(self._connect()) as conn:
            rows = conn.execute('''
                SELECT payload_json FROM incident_reports
                WHERE scenario_id = ? ORDER BY created_at DESC
            ''', (scenario_id,)).fetchall()
        return [IncidentReport.model_validate_json(row['payload_json']) for row in rows]

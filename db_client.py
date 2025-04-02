import re
import asyncpg
import json
from typing import Optional

class SafePostgresClient:
    def __init__(self, max_read_rows: int = 10000):
        self.max_read_rows = max_read_rows
        self.conn: Optional[asyncpg.Connection] = None

    async def connect(self, dsn: str):
        self.conn = await asyncpg.connect(dsn)

    def _is_destructive(self, query: str) -> bool:
        return bool(re.search(r'\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE)\b', query, re.IGNORECASE))

    async def _explain_query(self, query: str) -> int:
        result = await self.conn.fetchrow(f"EXPLAIN (FORMAT JSON) {query}")
        plan = json.loads(result['QUERY PLAN'])
        return int(plan[0]['Plan']['Plan Rows'])

    async def safe_execute(self, query: str) -> tuple[str, list]:
        if self._is_destructive(query):
            raise PermissionError("Destructive queries require confirmation. Add --confirm to proceed.")

        estimated_rows = await self._explain_query(query)
        if estimated_rows > self.max_read_rows:
            raise Warning(f"Query estimates scanning {estimated_rows} rows. Use LIMIT or add --confirm.")

        result = await self.conn.fetch(query)
        return query, [dict(row) for row in result]

    async def close(self):
        await self.conn.close()

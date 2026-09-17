from __future__ import annotations

import argparse
import os
from pathlib import Path

from app.product import ProductService
from app.product_api import serve_product
from app.store import IncidentStore

p = argparse.ArgumentParser(description="AI DevOps Engineer v3.13 local product runtime")
p.add_argument("--vault", type=Path, default=Path(".."))
p.add_argument("--host", default=os.getenv("RUNTIME_HOST", "0.0.0.0"))
p.add_argument("--port", type=int, default=int(os.getenv("RUNTIME_PORT", "8080")))
p.add_argument("--database-url", default=os.getenv("DATABASE_URL", ""))
a = p.parse_args()
store = IncidentStore(a.database_url)
service = ProductService(a.vault.resolve(), store)
serve_product(service, a.host, a.port)

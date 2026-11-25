"""Ponto de entrada ASGI para deploy do PlanoIA na Vercel."""

from pathlib import Path
import sys
from urllib.parse import parse_qsl, urlencode

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.main import app as fastapi_app  # noqa: E402


class VercelPathMiddleware:
    """Restaura o caminho original da rota quando a Vercel reescreve para /api/index."""

    def __init__(self, asgi_app):
        self.asgi_app = asgi_app

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http":
            raw_qs = scope.get("query_string", b"").decode("latin-1")
            params = parse_qsl(raw_qs, keep_blank_values=True)
            target_path = None
            remaining = []
            for k, v in params:
                if k == "__path" and target_path is None:
                    target_path = v
                else:
                    remaining.append((k, v))

            if target_path and scope.get("path") in ("/api/index", "/api/index.py", "/"):
                scope = dict(scope)
                scope["path"] = target_path
                scope["raw_path"] = target_path.encode("utf-8")
                scope["query_string"] = urlencode(remaining).encode("latin-1")

        await self.asgi_app(scope, receive, send)


app = VercelPathMiddleware(fastapi_app)

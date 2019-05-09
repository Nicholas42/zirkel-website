from app import build_app
from app.cli import register as cli_register
from app.models import User

app = build_app()
cli_register(app)

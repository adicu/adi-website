from app.routes.blog import blog
from app.routes.client import client

# Silence flake8 by referencing otherwise unused imports
__all__ = ['blog', 'client']

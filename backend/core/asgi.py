import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 1. Initialize Django ASGI
django_app = get_asgi_application()

# 2. Initialize FastAPI
fastapi_app = FastAPI(title="LexSovereign AI API")

# 3. Create the Gateway
async def application(scope, receive, send):
    if scope['type'] == 'http' and scope['path'].startswith('/api/v1'):
        await fastapi_app(scope, receive, send)
    else:
        await django_app(scope, receive, send)
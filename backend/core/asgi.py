import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 1. Initialize Django ASGI
django_app = get_asgi_application()

# 2. Initialize FastAPI with ROOT_PATH
# This tells FastAPI: "Hey, you are actually living inside /api/v1"
fastapi_app = FastAPI(title="LexSovereign AI API",
    root_path="/api/v1",  # CRITICAL: This fixes the openapi.json 404
)

# 3. Add the test route
@fastapi_app.get("/test")
async def test():
    return {"status": "FastAPI is linked and running!"}

# 4. The Gateway
async def application(scope, receive, send):
    if scope['type'] == 'http' and scope['path'].startswith('/api/v1'):
        # Pass the request to FastAPI
        await fastapi_app(scope, receive, send)
    else:
        # Pass everything else to Django
        await django_app(scope, receive, send)
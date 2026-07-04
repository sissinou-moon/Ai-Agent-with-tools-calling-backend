from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        request.state.request_id = str(uuid4()) # GENERATE REQUEST ID

        response = await call_next(request) # WITHOUT THIS LINE THE REQUEST NEVER REACHES THE ROUTE

        response.headers["X-Request-ID"] = request.state.request_id # ADD HEADER

        return response
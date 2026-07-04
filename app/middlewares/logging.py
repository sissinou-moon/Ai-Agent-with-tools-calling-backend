import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app")


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        ip = request.client.host
        ua = request.headers.get("user-agent")

        request.state.ip = request.client.host
        request.state.user_agent = request.headers.get("user-agent")

        start_time = time.perf_counter()

        response = await call_next(request)

        duration = round(time.perf_counter() - start_time, 4)

        logger.info(
            f"[{request.state.request_id}] "
            f"{request.method} "
            f"{request.url.path} "
            f"{response.status_code} "
            f"{duration}s"
            f"{ip} "
            f"{ua}"
        )

        return response
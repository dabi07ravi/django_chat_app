import logging
import uuid
from rest_framework.views import exception_handler
from rest_framework.response import Response

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # ✅ Known errors (DRF / custom exceptions)
    if response is not None:
        return response

    # 🔥 Unknown errors (log everything)
    error_id = str(uuid.uuid4())

    request = context.get("request")
    view = context.get("view")

    logger.error(
        f"""
        ERROR ID: {error_id}
        VIEW: {view.__class__.__name__ if view else 'N/A'}
        METHOD: {request.method if request else 'N/A'}
        PATH: {request.path if request else 'N/A'}
        ERROR: {str(exc)}
        """,
        exc_info=True
    )

    return Response({
        "success": False,
        "message": "Internal server error",
        "code": "SERVER_ERROR",
        "error_id": error_id
    }, status=500)
from typing import Optional, Union, List, Dict, Any
from fastapi.responses import JSONResponse

from app.response import Response


class HTTPResponse:
    def __init__(
        self,
        status_code: Optional[int] = None,
        data: Optional[Union[List[Any], Dict[str, Any]]] = None,
        message: Optional[str] = None,
    ):
        self.status_code = status_code
        self.data = data or {}  # Default to an empty dict or list
        self.message = message or ""  # Default message to empty string if None
        self.error = status_code and status_code > 300  # Simplified error check

    def return_response(self):
        response_content = {
            "message": self.message,
            "error": self.error,
            "success": not self.error,
            "data": self.data,
        }

        if self.status_code and self.status_code > 300:
            return JSONResponse(status_code=self.status_code, content=response_content)

        return Response(
            error=self.error,
            data=self.data,
            message=self.message,
            success=not self.error,
            status_code=self.status_code,
        )

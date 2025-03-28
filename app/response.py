from typing import Optional, Union, Any, List, Dict

from pydantic import BaseModel


class Response(BaseModel):
    error: bool = False
    data: Optional[Union[List[Any], Dict[str, Any]]] = None
    success: bool = True
    message: Optional[str] = ""
    status_code: int = 200

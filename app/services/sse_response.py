import orjson
import os
from typing import Optional


class SSE_Response:
    def __init__(
        self,
        message: str,
        status: str = "processing",
        output_path: Optional[str] = None,
        method_id: Optional[str] = None,
        method_name: Optional[str] = None,
        method_type: Optional[str] = None,
        result_type: Optional[str] = None,
        score: Optional[float] = None
    ):
        self.status = status
        self.message = message
        self.output_path = output_path.replace(
            os.sep, "/") if output_path else None
        self.method_id = method_id
        self.method_name = method_name
        self.method_type = method_type
        self.result_type = result_type
        self.score = score

    def to_dict(self) -> dict:
        data = {
            "status": self.status,
            "message": self.message,
            "data": {}
        }
        if self.output_path:
            data["data"]["output"] = {
                "path": self.output_path,
                "method_type": self.method_type
            }
            if self.score is not None:
                data["data"]["output"]["score"] = float(self.score)

        if self.method_id:
            data["data"]["id"] = self.method_id
        if self.method_name:
            data["data"]["name"] = self.method_name
        if self.result_type:
            data["data"]["result_type"] = self.result_type

        return data

    def to_json(self) -> str:
        return orjson.dumps(self.to_dict()).decode("utf-8")

    def to_sse(self) -> str:
        return f"data: {self.to_json()}\n\n"


class SSE_Error_Response:
    def __init__(self, message: str, error_code: int = 400):
        self.status = "error"
        self.message = message
        self.error_code = error_code

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "message": self.message,
            "error_code": self.error_code,
        }

    def to_json(self) -> str:
        return orjson.dumps(self.to_dict()).decode("utf-8")

    def to_sse(self) -> str:
        return f"data: {self.to_json()}\n\n"

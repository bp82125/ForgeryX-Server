import os
import orjson
import asyncio

from app.services.sse_response import SSE_Response, SSE_Error_Response


async def get_example_outputs(result_json_path):
    print(result_json_path)
    if not os.path.exists(result_json_path):
        yield SSE_Error_Response("Error: UUID not found", status="error").to_sse()
        return

    try:
        with open(result_json_path, "rb") as f:
            results = orjson.loads(f.read())
    except orjson.JSONDecodeError:
        yield SSE_Error_Response("Error: Corrupted results.json file", status="error").to_sse()
        return

    for result_str in results:
        try:
            result = orjson.loads(result_str)
            data = result.get("data", {})
            output = data.get("output", {})

            yield SSE_Response(
                message=result.get("message", ""),
                status=result.get("status", "processing"),
                output_path=output.get("path"),
                method_id=data.get("id"),
                method_name=data.get("name"),
                method_type=output.get("method_type"),
                result_type=data.get("result_type"),
                score=output.get("score"),
                metadata=data.get("metadata"),
            ).to_sse()

            await asyncio.sleep(0.8)

        except orjson.JSONDecodeError:
            yield SSE_Error_Response("Error: Malformed entry in results.json", status="error").to_sse()
            continue

    yield SSE_Response("Quá trình xử lý kết thúc", status="finished").to_sse()

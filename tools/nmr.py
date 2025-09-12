import httpx
from httpx import Timeout
DEFAULT_TIMEOUT = Timeout(120.0, connect=300.0)

from structs.nmr import (
    SearchParam,
    PredictParam,
    ReversePredictParam,
    InputNMR,
    Result,
    TaskSubmit,
    transform_predict_param,
    transform_reverse_predict_param,
    transform_search_param
)
from structs.base import RES

async def NMR_search(data:SearchParam)-> RES[list[Result]]:
    try:
        payload = TaskSubmit(input_data=transform_search_param(data))
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            url = "http://101.126.67.113:8090/sync_nmr_service_mcp"

            payload = payload.model_dump(exclude_none=True)
            response = await client.post(url, json=payload)
            response.raise_for_status()
            res_raw = response.json()
            res = RES[list[Result]](**res_raw['data']['result'])
            return res
    except Exception as e:
        return RES(code=-1, msg=f"nmr search error: {e}")


async def NMR_predict(data:PredictParam)->RES[list[Result]]:
    try:
        payload = TaskSubmit(input_data=transform_predict_param(data))
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            url = "http://101.126.67.113:8090/sync_nmr_service_mcp"

            payload = payload.model_dump(exclude_none=True)
            response = await client.post(url, json=payload)
            response.raise_for_status()
            res_raw = response.json()
            res = RES[list[Result]](**res_raw['data']['result'])
            return res
    except Exception as e:
        return RES(code=-1, msg=f"nmr predict error: {e}")


async def NMR_reverse_predict(data:ReversePredictParam) ->RES[list[Result]]:
    try:
        payload = TaskSubmit(input_data=transform_reverse_predict_param(data))
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            url = "http://101.126.67.113:8090/sync_nmr_service_mcp"

            payload = payload.model_dump(exclude_none=True)
            response = await client.post(url, json=payload)
            response.raise_for_status()
            res_raw = response.json()
            res = RES[list[Result]](**res_raw['data']['result'])
            return res
    except Exception as e:
        return RES(code=-1, msg=f"nmr reverse_predict error: {e}")

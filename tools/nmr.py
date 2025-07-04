import httpx
from httpx import Timeout
DEFAULT_TIMEOUT = Timeout(60.0, connect=300.0)

from structs.nmr import (
    SearchInput,
    PredictInput,
    PredictInputMCP,
    ReversePredictInput,
    InputNMR,
    Result,
)
from structs.base import RES

async def NMR_search(data:SearchInput)-> RES[list[Result]]:
    try:
        payload = InputNMR(search=data)
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            url = "http://101.126.67.113:8090/nmr_predict_service"

            payload = payload.model_dump(exclude_none=True)
            response = await client.post(url, json=payload)
            response.raise_for_status()
            res_raw = response.json()
            res = RES[list[Result]](**res_raw)
            return res
    except Exception as e:
        return RES(code=-1, msg=f"nmr search error: {e}")


async def NMR_predict(data:PredictInputMCP)->RES[list[Result]]:
    try:
        _data = PredictInput(
            smiles_list=[data.smiles_list],
            H_shifts=data.H_shifts,
            C_shifts=data.C_shifts,
            H_split=data.H_split,
        )
        payload = InputNMR(predict=_data)
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            url = "http://101.126.67.113:8090/nmr_predict_service"

            payload = payload.model_dump(exclude_none=True)
            response = await client.post(url, json=payload)
            response.raise_for_status()
            res_raw = response.json()
            res = RES[list[Result]](**res_raw)
            return res
    except Exception as e:
        return RES(code=-1, msg=f"nmr search error: {e}")


async def NMR_reverse_predict(data:ReversePredictInput) ->RES[list[Result]]:
    try:
        payload = InputNMR(reverse_predict=data)
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            url = "http://101.126.67.113:8090/nmr_predict_service"

            payload = payload.model_dump(exclude_none=True)
            response = await client.post(url, json=payload)
            response.raise_for_status()
            res_raw = response.json()
            res = RES[list[Result]](**res_raw)
            return res
    except Exception as e:
        return RES(code=-1, msg=f"nmr search error: {e}")

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
from tools.chem_tools import draw_mol_with_nmr
from rdkit import Chem

def add_svg(res:Result)->Result:
    res.svg = draw_mol_with_nmr(
        mol_list=[Chem.MolFromSmiles(res.smiles_with_atom_order, sanitize=False)],
        shifts_list=[res.atoms_shift],
        nmr_type=['H', 'C'],
        size=(300, 300),
        fontscale=0.6,
    )
    return res
    
def transform_result(res:RES[list[Result]])->RES[list[Result]]:
    res.data = [add_svg(_res) for _res in res.data]
    return res

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
            res = transform_result(res)
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
            res = transform_result(res)
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
            res = transform_result(res)
            return res
    except Exception as e:
        return RES(code=-1, msg=f"nmr reverse_predict error: {e}")

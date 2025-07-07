import sys, time
print(sys.path)

from tools.base import (
    ADMET_predict,
    Pharmacokinetics_predict,
    ToxScan_predict,
    InputData,
    InputPK,
    RES
)
from tools.nmr import NMR_search, NMR_predict,NMR_reverse_predict,SearchInput,PredictInput,ReversePredictInput,InputNMR,Result,TaskSubmit
import asyncio

input_data = InputData(smiles="CN1C=NC2=C1C(=O)N(C(=O)N2C)C")
input_pk = InputPK(smiles="CN1C=NC2=C1C(=O)N(C(=O)N2C)C")

async def test():
    start = time.time()
    tasks = [
        #NMR_search(SearchInput(C_shifts=[19.1, 19.4, 23.5, 62.7, 126.3, 126.5, 127.0, 128.36, 128.41, 130.2, 130.8, 134.8, 135.98, 136.02, 138.9])),
        #NMR_predict(PredictInput(smiles_list=["CN1C=NC2=C1C(=O)N(C(=O)N2C)C"])),
        NMR_reverse_predict(ReversePredictInput(C_shifts=[19.1, 19.4, 23.5, 62.7, 126.3, 126.5, 127.0, 128.36, 128.41, 130.2, 130.8, 134.8, 135.98, 136.02, 138.9])),
    ]
    res_list:list[RES] = await asyncio.gather(*tasks)
    print(f"time: {time.time() - start}")
    for res in res_list:
        print(res)

if __name__ == "__main__":
    asyncio.run(test())


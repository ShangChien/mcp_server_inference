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
import asyncio

input_data = InputData(smiles="CN1C=NC2=C1C(=O)N(C(=O)N2C)C")
input_pk = InputPK(smiles="CN1C=NC2=C1C(=O)N(C(=O)N2C)C")

async def test():
    start = time.time()
    tasks = [
        # ADMET_predict(input_data),
        Pharmacokinetics_predict(input_pk),
        # ToxScan_predict(input_data)
    ]
    res_list:list[RES] = await asyncio.gather(*tasks)
    print(f"time: {time.time() - start}")
    for res in res_list:
        print(res)

if __name__ == "__main__":
    asyncio.run(test())


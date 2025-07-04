from fastmcp import FastMCP
from tools.base import (
    ADMET_predict,
    Pharmacokinetics_predict,
    ToxScan_predict,
    InputData,
    RES,
    AdmetInnerData,
    InputPK,
    PKResult,
    ToxResult
)
from tools.nmr import (
    NMR_search,
    NMR_predict,
    NMR_reverse_predict,
    SearchInput,
    PredictInputMCP,
    ReversePredictInput,
    InputNMR,
    Result,
)
from structs.admet import description as admet_description
from structs.pk import description as pk_description

mcp = FastMCP("Demo 🚀")

@mcp.resource("data://ADMET_reference", name="ADMET Reference Data")
async def admet_meta():
    return {
        "name": "ADMET",
        "description": "ADMET is a collection of 20 molecular descriptors that are commonly used to predict the pharmacokinetic and pharmacodynamic properties of drugs.",
        "properties": admet_description
    }


@mcp.resource("data://Pharmacokinetics_reference", name="Pharmacokinetics Reference Data")
async def pk_meta():
    return {
        "name": "Pharmacokinetics",
        "description": "Pharmacokinetics is a collection of 10 molecular descriptors that are commonly used to predict the pharmacokinetic and pharmacodynamic properties of drugs.",
        "properties": pk_description
    }


# @mcp.tool(
#     name="ADMET_Service", 
#     description="Predict the ADMET properties of a molecule. Absorption, Distribution, Metabolism, Excretion and Toxicity Prediction for Molecules"
# )
# async def ADMET_predict_tool(data: InputData) -> RES[AdmetInnerData]:
#     return await ADMET_predict(data)


# @mcp.tool(
#     name="Pharmacokinetics_Service",
#     description="Predict the Pharmacokinetics properties of a molecule. Pharmacokinetic Metabolism Curve Prediction, Prediction of Drug Concentration Changes over Time."
# )
# async def Pharmacokinetics_predict_tool(data: InputPK) -> RES[PKResult]:
#     return await Pharmacokinetics_predict(data)


# @mcp.tool(
#     name="ToxScan_predict",
#     description="Predict the ToxScan properties of a molecule. Safety Evaluation of Drugs, Chemicals or Environmental Pollutants.",
# )
# async def ToxScan_predict_tool(data: InputData) -> RES[ToxResult]:
#     return await ToxScan_predict(data)

@mcp.tool(
    name="NMR_search",
    description="Search for molecule using NMR-characteristics(H_shifts or C_shifts).",
)
async def NMR_search_tool(data: SearchInput) -> RES[list[Result]]:
    return await NMR_search(data)

@mcp.tool(
    name="NMR_predict",
    description="Predict the NMR-characteristics(H_shifts or C_shifts) of a molecule(smiles).",
)
async def NMR_predict_tool(data: PredictInputMCP) -> RES[list[Result]]:
    return await NMR_predict(data)

@mcp.tool(
    name="NMR_reverse_predict",
    description="Predict the molecule(smiles) according NMR-characteristics(H_shifts or C_shifts).",
)
async def NMR_reverse_predict_tool(data: ReversePredictInput) -> RES[list[Result]]:
    return await NMR_reverse_predict(data)


if __name__ == "__main__":
    mcp.run(transport='sse',host="0.0.0.0",port=5003)

# NMR MCP Server 文档说明

## 工具概述

本服务提供三个主要的NMR相关工具，用于分子结构的搜索、预测和逆向预测。

```python
@mcp.tool(
    name="NMR_search",
    description="""Database search for molecules based on NMR spectroscopic data. For more accurate but slower reverse prediction, use NMR_reverse_predict tool.
    
    This tool performs molecular structure database searching using Nuclear Magnetic Resonance (NMR) spectroscopic data.
    Input 1H/13C NMR chemical shifts to find matching molecular structures from database. Allows constraints on elemental composition.
    
    Input:
        SearchParam

    Returns: List of candidate molecules with SMILES, predicted NMR data, and spectral similarity scores
    """,)
async def NMR_search_tool(data: SearchParam) -> RES[list[Result]]:
    return await NMR_search(data)

@mcp.tool(
    name="NMR_predict",
    description="""Predict NMR spectroscopic properties for molecular structures.
    
    This tool calculates simulated 1H and 13C NMR chemical shifts for given molecular structures.
    Input SMILES strings to simulate NMR spectra and validate structural assignments. Allows comparison of reference NMR spectra with predicted spectra for similarity scoring.
    
    Input:
        PredictParam
    
    Returns: List of molecules with predicted NMR chemical shifts and spectral similarity scores
    """,
)
async def NMR_predict_tool(data: PredictParam) -> RES[list[Result]]:
    return await NMR_predict(data)

@mcp.tool(
    name="NMR_reverse_predict",
    description="""Reverse NMR analysis to propose molecular structures using molecular optimization. For fast database searching, use NMR_search tool.

    This tool generates candidate molecular structures from Nuclear Magnetic Resonance (NMR) spectroscopic data.
    Input 1H/13C NMR chemical shifts to identify compounds and determine structures. Allows constraints on elemental composition and molecular formula.

    Input:
        ReversePredictParam
    
    Returns: List of candidate molecules with SMILES, predicted NMR data, and spectral similarity scores
    """,
)
async def NMR_reverse_predict_tool(data: ReversePredictParam) -> RES[list[Result]]:
    return await NMR_reverse_predict(data)
```

## 变量类型定义

### 输入类型

```python
class SearchParam(BaseModel):
    H_shifts: list[float]|None = Field(None, description="List of proton (1H) NMR chemical shifts in ppm. For each NMR signal, take the average chemical shift if it's a range (e.g., 7.68-7.60 → 7.64), then repeat this value according to the number of protons (integration). Finally, sort all values in ascending order. Example: [2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 7.64] from '1H NMR: 7.68-7.60 (m, 1H), 2.1 (s, 6H)'")
    C_shifts: list[float]|None = Field(None, description="List of carbon-13 (13C) NMR chemical shifts in ppm, sorted in ascending order. Example: [30.0, 205.0] from '13C NMR (CDCl3, 100 MHz) 205.0, 30.0.'")
    allowed_elements: list[str]|None = Field(None, description="Allowed chemical elements for molecular composition. Example: ['C', 'H', 'O', 'N']")
    topk: int = Field(10, description="Number of top results to return (default: 10)")

class PredictParam(BaseModel):
    smiles_list: list[str] = Field(..., description="List of SMILES strings for molecules to predict NMR spectra")
    H_shifts: list[float]|None = Field(None, description="List of proton (1H) NMR chemical shifts in ppm. For each NMR signal, take the average chemical shift if it's a range (e.g., 7.68-7.60 → 7.64), then repeat this value according to the number of protons (integration). Finally, sort all values in ascending order. Example: [2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 7.64] from '1H NMR: 7.68-7.60 (m, 1H), 2.1 (s, 6H)'")
    C_shifts: list[float]|None = Field(None, description="List of carbon-13 (13C) NMR chemical shifts in ppm, sorted in ascending order. Example: [30.0, 205.0] from '13C NMR (CDCl3, 100 MHz) 205.0, 30.0.'")


class ReversePredictParam(BaseModel):
    H_shifts: list[float]|None = Field(None, description="List of proton (1H) NMR chemical shifts in ppm. For each NMR signal, take the average chemical shift if it's a range (e.g., 7.68-7.60 → 7.64), then repeat this value according to the number of protons (integration). Finally, sort all values in ascending order. Example: [2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 7.64] from '1H NMR: 7.68-7.60 (m, 1H), 2.1 (s, 6H)'")
    C_shifts: list[float]|None = Field(None, description="List of carbon-13 (13C) NMR chemical shifts in ppm, sorted in ascending order. Example: [30.0, 205.0] from '13C NMR (CDCl3, 100 MHz) 205.0, 30.0.'")
    allowed_elements: list[str]|None = Field(None, description="Allowed chemical elements for molecular composition. Example: ['C', 'H', 'O', 'N']")
    formula: str|None = Field(None, description="Molecular formula constraint for the target molecule. Example: 'C6H12O6'")
    topk: int = Field(10, description="Number of top results to return (default: 10)")
```

### 输出类型

```python
class Result(BaseModel):
    smiles: str
    smiles_with_atom_order: str
    atoms_shift: list[float]
    atoms_element: list[int]
    atoms_equi_class: list[int]
    H_score: float
    C_score: float
    score: float
```

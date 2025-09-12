# NMR MCP Server 文档说明


### 1. NMR_search_tool

```python
@mcp.tool(
    name="NMR_search",
    description="Search for molecules using NMR-characteristics(H_shifts or C_shifts).",
)
async def NMR_search_tool(data: SearchParam) -> RES[list[Result]]:
    return await NMR_search(data)
```

**功能描述**: 使用 NMR 特征(H位移或C位移)搜索分子。

**输入参数**:
- `data`: SearchParam 类型，包含搜索所需的 NMR 特征数据。

**返回结果**:
- 包含多个 Result 对象的列表，每个 Result 对象表示一个搜索到的分子及其相关信息。

### 2. NMR_predict_tool

```python
@mcp.tool(
    name="NMR_predict",
    description="Predict the NMR-characteristics(H_shifts or C_shifts) of a molecule(smiles).",
)
async def NMR_predict_tool(data: PredictParam) -> RES[list[Result]]:
    return await NMR_predict(data)
```

**功能描述**: 预测分子(SMILES 表示)的 NMR 特征(H位移或C位移)。

**输入参数**:
- `data`: PredictParam 类型，包含待预测分子的 SMILES 字符串及可选的 NMR 特征数据。

**返回结果**:
- 包含多个 Result 对象的列表，每个 Result 对象表示一个分子及其预测的 NMR 特征信息。

### 3. NMR_reverse_predict_tool

```python
@mcp.tool(
    name="NMR_reverse_predict",
    description="Predict the molecule(smiles) according NMR-characteristics(H_shifts or C_shifts).",
)
async def NMR_reverse_predict_tool(data: ReversePredictParam) -> RES[list[Result]]:
    return await NMR_reverse_predict(data)
```

**功能描述**: 根据 NMR 特征(H位移或C位移)预测分子结构(SMILES 表示)。

**输入参数**:
- `data`: ReversePredictParam 类型，包含 NMR 特征数据及可选的约束条件和候选分子列表。

**返回结果**:
- 包含多个 Result 对象的列表，每个 Result 对象表示一个预测的分子及其相关信息。

## 变量类型定义

### 输入类型

```python
class SearchParam(BaseModel):
    H_shifts: list[float]|None = Field(None, description="List of proton NMR chemical shifts in ppm")
    C_shifts: list[float]|None = Field(None, description="List of carbon-13 NMR chemical shifts in ppm")
    allowed_elements: list[str]|None = Field(None, description="Allowed chemical elements for molecular composition")
    topk: int = Field(10, description="Number of top results to return")

class PredictParam(BaseModel):
    smiles_list: list[str] = Field(..., description="List of SMILES strings for molecules to predict NMR spectra")
    H_shifts: list[float]|None = Field(None, description="Reference proton NMR chemical shifts in ppm, repeated according to proton multiplicity")
    C_shifts: list[float]|None = Field(None, description="Reference list of carbon-13 NMR chemical shifts in ppm")

class ReversePredictParam(BaseModel):
    H_shifts: list[float] | None = Field(None, description="List of proton NMR chemical shifts in ppm, repeated according to proton multiplicity")
    C_shifts: list[float] | None = Field(None, description="List of carbon-13 NMR chemical shifts in ppm")
    allowed_elements: list[str] | None = Field(None, description="Allowed chemical elements for molecular composition")
    formula: str | None = Field(None, description="Molecular formula constraint")
    topk: int = Field(10, description="Number of top results to return")
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

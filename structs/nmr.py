from pydantic import BaseModel, Field
from typing import Union, Optional, Generic, TypeVar, Literal


class ConfigBase(BaseModel):
    sigma_h: int = 1
    sigma_c: int = 10
    use_H_split: bool = False
    split_coef: float = 0.8

class ConfigSolver(ConfigBase):
    max_iter: int = 2
    num_search: int = 1000
    num_pool: int = 1000
    num_filter_pair: int = 200000
    num_filter_mol: int = 1000
    num_mutate_mol: int = 100
    topk: int = 1000
    use_stereo: bool = False
    optional_halogens: list[str] = ['F', 'Cl', 'Br', 'I']
    max_cycle_length: int = 6
    invalid_patterns: list[str] = ['[O][O]', '[R]=[R]=[R]', '[r3,r4]=[r3,r4]', '[O][F,Cl,Br,I]']
    include_active_hs: Literal['yes', 'no', 'both'] = 'yes'


class SearchParam(BaseModel):
    H_shifts: list[float]|None = Field(None, description="List of proton (1H) NMR chemical shifts in ppm. For each NMR signal, take the average chemical shift if it's a range (e.g., 7.68-7.60 → 7.64), then repeat this value according to the number of protons (integration). Finally, sort all values in ascending order. Example: [2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 7.64] from '1H NMR: 7.68-7.60 (m, 1H), 2.1 (s, 6H)'")
    C_shifts: list[float]|None = Field(None, description="List of carbon-13 (13C) NMR chemical shifts in ppm, sorted in ascending order. Example: [30.0, 205.0] from '13C NMR (CDCl3, 100 MHz) 205.0, 30.0.'")
    allowed_elements: list[str]|None = Field(None, description="Allowed chemical elements for molecular composition. Example: ['C', 'H', 'O', 'N']")
    topk: int = Field(10, description="Number of top results to return (default: 10)")
    
class SearchInput(BaseModel):
    H_split: list[str]|None = None
    H_shifts: list[float]|None = None
    C_shifts: list[float]|None = None
    num_search: int = 1000
    topk: int = 10
    allowed_elements: list[str]|None = ['C', 'H', 'O', 'N', 'F', 'Cl', 'Br', 'I', 'P', 'S', 'Si', 'B']
    

class PredictParam(BaseModel):
    smiles_list: list[str] = Field(..., description="List of SMILES strings for molecules to predict NMR spectra")
    H_shifts: list[float]|None = Field(None, description="List of proton (1H) NMR chemical shifts in ppm. For each NMR signal, take the average chemical shift if it's a range (e.g., 7.68-7.60 → 7.64), then repeat this value according to the number of protons (integration). Finally, sort all values in ascending order. Example: [2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 7.64] from '1H NMR: 7.68-7.60 (m, 1H), 2.1 (s, 6H)'")
    C_shifts: list[float]|None = Field(None, description="List of carbon-13 (13C) NMR chemical shifts in ppm, sorted in ascending order. Example: [30.0, 205.0] from '13C NMR (CDCl3, 100 MHz) 205.0, 30.0.'")
    
class PredictInput(BaseModel):
    smiles_list: list[str]
    H_shifts: list[float]|None = None
    C_shifts: list[float]|None = None
    H_split: list[str]|None = None
    
class ReversePredictParam(BaseModel):
    H_shifts: list[float]|None = Field(None, description="List of proton (1H) NMR chemical shifts in ppm. For each NMR signal, take the average chemical shift if it's a range (e.g., 7.68-7.60 → 7.64), then repeat this value according to the number of protons (integration). Finally, sort all values in ascending order. Example: [2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 7.64] from '1H NMR: 7.68-7.60 (m, 1H), 2.1 (s, 6H)'")
    C_shifts: list[float]|None = Field(None, description="List of carbon-13 (13C) NMR chemical shifts in ppm, sorted in ascending order. Example: [30.0, 205.0] from '13C NMR (CDCl3, 100 MHz) 205.0, 30.0.'")
    allowed_elements: list[str]|None = Field(None, description="Allowed chemical elements for molecular composition. Example: ['C', 'H', 'O', 'N']")
    formula: str|None = Field(None, description="Molecular formula constraint for the target molecule. Example: 'C6H12O6'")
    topk: int = Field(10, description="Number of top results to return (default: 10)")

class Constraint(BaseModel):
    formula: str | None = None
    H_split: list[str] | None = None
    allowed_elements: list[str] | None = None
    elements: list[str] | None = None

class ReversePredictInput(BaseModel):
    H_split: list[str] | None = None
    H_shifts: list[float] | None = None
    C_shifts: list[float] | None = None
    constraints: Constraint | None = None
    candidates: list[str] | None = None

# default_config = ConfigSolver()
class InputNMR(BaseModel):
    search: SearchInput | None = None
    predict: PredictInput | None = None
    reverse_predict: ReversePredictInput | None = None
    config: ConfigSolver = ConfigSolver()

class Result(BaseModel):
    smiles: str
    smiles_with_atom_order: str
    atoms_shift: list[float]
    atoms_element: list[int]
    atoms_equi_class: list[int]
    H_score: float
    C_score: float
    score: float
    svg:str=None

class TaskSubmit(BaseModel):
    name: str = ''
    input_data: InputNMR


def transform_search_param(param: SearchParam) -> InputNMR:
    return InputNMR(search=SearchInput(**param.model_dump(exclude_unset=True)))


def transform_predict_param(param: PredictParam) -> InputNMR:
    return InputNMR(predict=PredictInput(**param.model_dump(exclude_unset=True)))


def transform_reverse_predict_param(param: ReversePredictParam) -> InputNMR:
    return InputNMR(reverse_predict=ReversePredictInput(
        H_shifts=param.H_shifts,
        C_shifts=param.C_shifts,
        constraints=Constraint(formula=param.formula, allowed_elements=param.allowed_elements),
    ),
        config=ConfigSolver(topk=param.topk)
    )

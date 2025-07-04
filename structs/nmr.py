from pydantic import BaseModel
from typing import Union, Optional, Generic, TypeVar, Literal


# class ConfigBase(BaseModel):
#     sigma_h: int = 1
#     sigma_c: int = 10
#     use_H_split: bool = False
#     split_coef: float = 0.8

# class ConfigSolver(ConfigBase):
#     max_iter: int = 2
#     num_search: int = 1000
#     num_pool: int = 1000
#     num_filter_pair: int = 200000
#     num_filter_mol: int = 1000
#     num_mutate_mol: int = 1000
#     topk: int = 1000
#     use_stereo: bool = False
#     optional_halogens: list[str] = ['F', 'Cl', 'Br', 'I']
#     max_cycle_length: int = 6
#     bad_pattern: list[str] = ['[O][O]', '[R]=[R]=[R]', '[r3,r4]=[r3,r4]']

class SearchInput(BaseModel):
    H_split: list[str]|None = None
    H_shifts: list[float]|None = None 
    C_shifts: list[float]|None = None 
    num_search: int = 1000
    topk: int = 10
    allowed_elements: list[str]|None = None

class PredictInput(BaseModel):
    smiles_list:list[str]
    H_shifts:list[float]|None=None
    C_shifts:list[float]|None=None
    H_split:list[str]|None=None

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
    search:SearchInput|None=None
    predict:PredictInput|None=None
    reverse_predict:ReversePredictInput|None=None
    # config:ConfigBase = default_config

class Result(BaseModel):
    smiles:str
    atoms_shift:list[float]
    atoms_element:list[int]
    atoms_equi_class:list[int]
    H_score:float
    C_score:float
    score:float

class TaskSubmit(BaseModel):
    name: str =''
    input_data: InputNMR



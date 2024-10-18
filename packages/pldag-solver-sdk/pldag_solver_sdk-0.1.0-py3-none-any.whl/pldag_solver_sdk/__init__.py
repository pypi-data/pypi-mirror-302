import requests
import numpy as np

from dataclasses import dataclass
from pldag import PLDAG
from typing import Dict, List, Optional
from enum import Enum

class SolverType(str, Enum):
    DEFAULT = "default"

@dataclass
class SolutionResponse:

    solution:   Optional[Dict[str, int]]    = None
    error:      Optional[str]               = None

@dataclass
class Solver:
    
    url: str

    def _sparse_polyhedron(self, matrix: np.ndarray) -> tuple:
        rows, cols = np.nonzero(matrix)
        vals = matrix[rows, cols]
        return rows.tolist(), cols.tolist(), vals.tolist()

    def solve(
        self, 
        model: PLDAG, 
        objectives: List[Dict[str, int]], 
        assume: Dict[str, complex] = {}, 
        solver: SolverType = SolverType.DEFAULT,
        maximize: bool = True,
    ) -> List[SolutionResponse]:
        A, b = model.to_polyhedron(**assume)
        A_rows, A_cols, A_vals = self._sparse_polyhedron(A)
        response = requests.post(
            f"{self.url}/model/solve-one/linear",
            json={
                "model": {
                    "polyhedron": {
                        "A": {
                            "rows": A_rows,
                            "cols": A_cols,
                            "vals": A_vals,
                            "shape": {"nrows": A.shape[0], "ncols": A.shape[1]}
                        },
                        "b": b.tolist()
                    },
                    "columns": model.columns.tolist(),
                    "rows": [],
                    "intvars": model.integer_primitives.tolist()
                },
                "direction": "maximize" if maximize else "minimize",
                "objectives": objectives,
                
            }
        )
        if response.status_code != 200:
            raise Exception(response.text)
        
        return list(
            map(
                lambda x: SolutionResponse(**x),
                response.json().get("solutions", [])
            )
        )
from pydantic import BaseModel
from typing import List

from halerium_utilities.board.schemas.node import Node
from halerium_utilities.board.schemas.edge import Edge
from halerium_utilities.board.schemas.workflow import Workflow


class Board(BaseModel):
    version: str
    nodes: List[Node]
    edges: List[Edge]
    workflows: List[Workflow]

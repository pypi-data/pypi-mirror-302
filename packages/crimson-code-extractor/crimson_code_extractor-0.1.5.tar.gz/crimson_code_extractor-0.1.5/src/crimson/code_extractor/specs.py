from typing import Optional, List, Literal
from pydantic import BaseModel


class ArgSpec(BaseModel):
    name: str
    type: Literal["positional", "vararg", "kwonlyarg", "kwarg"]
    annotation: Optional[str] = None
    default: Optional[str] = None


# if not given, annotation is Any
class ReturnSpec(BaseModel):
    literal: str


class FuncSpec(BaseModel):
    name: str
    doc: Optional[str]
    arg_specs: Optional[List[ArgSpec]] = None
    return_specs: Optional[List[ReturnSpec]] = None
    return_annotation: Optional[str] = None
